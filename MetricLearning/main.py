import argparse

from datamodel import data_provider
from lib import GoogleNet_Model, Loss_ops, nn_Ops, Embedding_Visualization, HDML, evaluation
import copy
from tqdm import tqdm
from tensorflow.contrib import layers
from FLAGS import *

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='Dataset ingestion')
parser.add_argument('-l', '--loss', dest='Loss',
                    help='Loss Function', default='Triplet')
parser.add_argument('-d', '--dataset', dest='dataset',
                    help='dataset type', default='cars196')
parser.add_argument('-a', '--hdml', dest='HDML',
                    help='Apply HDML', default='False', type=str2bool)

# create a saver
# check system time
_time = time.strftime('%m-%d-%H-%M', time.localtime(time.time()))
LOGDIR = FLAGS.log_save_path + FLAGS.dataSet + '/' + FLAGS.LossType + '/' + _time + '/'

def initialize(args):
    # Create the stream of datas from dataset
    streams = data_provider.get_streams(FLAGS.batch_size, args.dataset, method, crop_size=FLAGS.default_image_size)

    regularizer = layers.l2_regularizer(FLAGS.Regular_factor)

    if FLAGS. SaveVal:
        nn_Ops.create_path(_time)
    summary_writer = tf.summary.FileWriter(LOGDIR)

    return streams, summary_writer

def placeholders():
    x_raw = tf.placeholder(tf.float32, shape=[None, FLAGS.default_image_size, FLAGS.default_image_size, 3])
    label_raw = tf.placeholder(tf.int32, shape=[None, 1])
    with tf.name_scope('istraining'):
        is_Training = tf.placeholder(tf.bool)
    with tf.name_scope('learning_rate'):
        lr = tf.placeholder(tf.float32)

    return x_raw, label_raw, is_Training, lr

def configClassifier(args, x_raw, is_Training):
    with tf.variable_scope('Classifier'):
        google_net_model = GoogleNet_Model.GoogleNet_Model()
        embedding = google_net_model.forward(x_raw)

        embedding_y_origin = 0
        if args.HDML:
            embedding_y_origin = embedding

        # Batch Normalization layer 1
        embedding = nn_Ops.bn_block(
            embedding, normal=FLAGS.normalize, is_Training=is_Training, name='BN1')

        # FC layer 1
        embedding_z = nn_Ops.fc_block(
            embedding, in_d=1024, out_d=FLAGS.embedding_size,
            name='fc1', is_bn=False, is_relu=False, is_Training=is_Training)

        # Embedding Visualization
        assignment, embedding_var = Embedding_Visualization.embedding_assign(
            batch_size=256, embedding=embedding_z,
            embedding_size=FLAGS.embedding_size, name='Embedding_of_fc1')

        return embedding_y_origin, embedding_z

def configLoss(args, label_raw, embedding_z):
    # conventional Loss function
    with tf.name_scope('Loss'):
        def exclude_batch_norm(name):
            return 'batch_normalization' not in name and 'Generator' not in name and 'Loss' not in name

        wdLoss = FLAGS.Regular_factor * tf.add_n(
            [tf.nn.l2_loss(v) for v in tf.trainable_variables() if exclude_batch_norm(v.name)]
        )
        # Get the Label
        label = tf.reduce_mean(label_raw, axis=1, keep_dims=False)
        J_m = Loss_ops.Loss(embedding_z, label, FLAGS.LossType) + wdLoss

    return wdLoss, label, J_m

def configHDML(args, is_Training, embedding_y_origin, label, J_m):
    with tf.name_scope('Javg'):
        Javg = tf.placeholder(tf.float32)
    with tf.name_scope('Jgen'):
        Jgen = tf.placeholder(tf.float32)

    #Augmentor
    embedding_z_quta = HDML.Pulling(args.Loss, embedding_z, Javg)

    embedding_z_concate = tf.concat([embedding_z, embedding_z_quta], axis=0)

    params = (is_Training, embedding_y_origin, label, J_m, Javg, Jgen, embedding_z_quta, embedding_z_concate)

    if args.Loss =="Triplet":
        return configHDMLTriplet(params)
    elif args.Loss == "NPairLoss":
        return configHDMLNPair(params)

def HDMLGenerators(is_Training, embedding_z_concate):
    # generator fc3
    embedding_y_concate = nn_Ops.fc_block(
        embedding_z_concate, in_d=FLAGS.embedding_size, out_d=512,
        name='generator1', is_bn=True, is_relu=True, is_Training=is_Training
    )

    # generator fc4
    embedding_y_concate = nn_Ops.fc_block(
        embedding_y_concate, in_d=512, out_d=1024,
        name='generator2', is_bn=False, is_relu=False, is_Training=is_Training
    )

    return embedding_y_concate

def configHDMLTriplet(params):
    is_Training, embedding_y_origin, label, J_m, Javg, Jgen, embedding_z_quta, embedding_z_concate = params

    # Generator
    with tf.variable_scope('Generator'):
        embedding_y_concate = HDMLGenerators(is_Training, embedding_z_concate)

        embedding_yp, embedding_yq = tf.split(embedding_y_concate, 2, axis=0)

    with tf.variable_scope('Classifier'):
        embedding_z_quta = nn_Ops.bn_block(
            embedding_yq, normal=FLAGS.normalize, is_Training=is_Training, name='BN1', reuse=True)

        embedding_z_quta = nn_Ops.fc_block(
            embedding_z_quta, in_d=1024, out_d=FLAGS.embedding_size,
            name='fc1', is_bn=False, is_relu=False, reuse=True, is_Training=is_Training
        )


    with tf.name_scope('Loss'):
        J_syn = (1. - tf.exp(-FLAGS.beta / Jgen)) * Loss_ops.Loss(embedding_z_quta, label, _lossType=FLAGS.LossType)
        J_m = (tf.exp(-FLAGS.beta/Jgen))*J_m
        J_metric = J_m + J_syn

        cross_entropy, W_fc, b_fc = HDML.cross_entropy(embedding=embedding_y_origin, label=label)


        J_recon = (1 - FLAGS._lambda) * tf.reduce_sum(tf.square(embedding_yp - embedding_y_origin))
        Logits_q = tf.matmul(embedding_yq, W_fc) + b_fc
        J_soft = FLAGS.Softmax_factor * FLAGS._lambda * tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label, logits=Logits_q))

        J_gen = J_recon + J_soft

    return J_m, Javg, Jgen, J_metric, J_gen, J_syn, cross_entropy, J_recon, J_soft

def configHDMLNPair(params):
    is_Training, embedding_y_origin, label, J_m, Javg, Jgen, embedding_z_quta, embedding_z_concate = params

    # Generator
    with tf.variable_scope('Generator'):
        embedding_y_concate = HDMLGenerators(is_Training, embedding_z_concate)

        embedding_yp, embedding_yq = HDML.npairSplit(embedding_y_concate)

    with tf.variable_scope('Classifier'):
        embedding_z_quta = nn_Ops.bn_block(
            embedding_yq, normal=FLAGS.normalize, is_Training=is_Training, name='BN1', reuse=True)

        embedding_z_quta = nn_Ops.fc_block(
            embedding_z_quta, in_d=1024, out_d=FLAGS.embedding_size,
            name='fc1', is_bn=False, is_relu=False, reuse=True, is_Training=is_Training
        )

        embedding_zq_anc = tf.slice(
            input_=embedding_z_quta, begin=[0, 0], size=[int(FLAGS.batch_size / 2), int(FLAGS.embedding_size)])
        embedding_zq_negtile = tf.slice(
            input_=embedding_z_quta, begin=[int(FLAGS.batch_size / 2), 0],
            size=[int(np.square(FLAGS.batch_size / 2)), int(FLAGS.embedding_size)]
        )

    with tf.name_scope('Loss'):
        J_syn = (1. - tf.exp(-FLAGS.beta / Jgen)) * Loss_ops.new_npair_loss(
            labels=label,
            embedding_anchor=embedding_zq_anc,
            embedding_positive=embedding_zq_negtile,
            equal_shape=False, reg_lambda=FLAGS.loss_l2_reg)
        J_m = (tf.exp(-FLAGS.beta / Jgen)) * J_m
        J_metric = J_m + J_syn

        cross_entropy, W_fc, b_fc = HDML.cross_entropy(embedding=embedding_y_origin, label=label)

        embedding_yq_anc = tf.slice(
            input_=embedding_yq, begin=[0, 0], size=[int(FLAGS.batch_size / 2), 1024])
        embedding_yq_negtile = tf.slice(
            input_=embedding_yq, begin=[int(FLAGS.batch_size / 2), 0],
            size=[int(np.square(FLAGS.batch_size / 2)), 1024]
        )
        J_recon = (1 - FLAGS._lambda) * tf.reduce_sum(tf.square(embedding_yp - embedding_y_origin))
        J_soft = HDML.genSoftmax(
            embedding_anc=embedding_yq_anc, embedding_neg=embedding_yq_negtile,
            W_fc=W_fc, b_fc=b_fc, label=label
        )
        J_gen = J_recon + J_soft

    return J_m, Javg, Jgen, J_metric, J_gen, J_syn, cross_entropy, J_recon, J_soft

def configTrainSteps(args, J_m, J_metric, J_gen, cross_entropy):
    if args.HDML:
        c_train_step = nn_Ops.training(loss=J_metric, lr=lr, var_scope='Classifier')
        g_train_step = nn_Ops.training(loss=J_gen, lr=FLAGS.lr_gen, var_scope='Generator')
        s_train_step = nn_Ops.training(loss=cross_entropy, lr=FLAGS.s_lr, var_scope='Softmax_classifier')

        return (c_train_step, g_train_step, s_train_step)
    else:
        train_step = nn_Ops.training(loss=J_m, lr=lr)

        return (train_step)

def configTfSession(args, streams, summary_writer, train_steps, losses):
    stream_train, stream_train_eval, stream_test = streams
    wdLoss, J_m, Javg, Jgen, J_metric, J_gen, J_syn, cross_entropy, J_recon, J_soft = losses

    with tf.Session(config=config) as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()

        # learning rate
        _lr = FLAGS.init_learning_rate

        # Restore a checkpoint
        if FLAGS.load_formalVal:
            saver.restore(sess, FLAGS.log_save_path + FLAGS.dataSet + '/' + FLAGS.LossType + '/' + FLAGS.formerTimer)

        # Training
        epoch_iterator = stream_train.get_epoch_iterator()

        # collectors
        J_m_loss = nn_Ops.data_collector(tag='Jm', init=1e+6)
        J_syn_loss = nn_Ops.data_collector(tag='J_syn', init=1e+6)
        J_metric_loss = nn_Ops.data_collector(tag='J_metric', init=1e+6)
        J_soft_loss = nn_Ops.data_collector(tag='J_soft', init=1e+6)
        J_recon_loss = nn_Ops.data_collector(tag='J_recon', init=1e+6)
        J_gen_loss = nn_Ops.data_collector(tag='J_gen', init=1e+6)
        cross_entropy_loss = nn_Ops.data_collector(tag='cross_entropy', init=1e+6)
        wd_Loss = nn_Ops.data_collector(tag='weight_decay', init=1e+6)
        max_nmi = 0
        step = 0

        bp_epoch = FLAGS.init_batch_per_epoch
        with tqdm(total=FLAGS.max_steps) as pbar:
            for batch in copy.copy(epoch_iterator):
                # get images and labels from batch
                x_batch_data, Label_raw = nn_Ops.batch_data(batch)
                pbar.update(1)
                if not args.HDML:
                    train_step = train_steps
                    train, J_m_var, wd_Loss_var = sess.run([train_step, J_m, wdLoss],
                                                           feed_dict={x_raw: x_batch_data, label_raw: Label_raw,
                                                                      is_Training: True, lr: _lr})
                    J_m_loss.update(var=J_m_var)
                    wd_Loss.update(var=wd_Loss_var)

                else:
                    c_train_step, g_train_step, s_train_step = train_steps
                    c_train, g_train, s_train, wd_Loss_var, J_metric_var, J_m_var, \
                    J_syn_var, J_recon_var, J_soft_var, J_gen_var, cross_en_var = sess.run(
                        [c_train_step, g_train_step, s_train_step, wdLoss,
                         J_metric, J_m, J_syn, J_recon, J_soft, J_gen, cross_entropy],
                        feed_dict={x_raw: x_batch_data,
                                   label_raw: Label_raw,
                                   is_Training: True, lr: _lr, Javg: J_m_loss.read(), Jgen: J_gen_loss.read()})
                    wd_Loss.update(var=wd_Loss_var)
                    J_metric_loss.update(var=J_metric_var)
                    J_m_loss.update(var=J_m_var)
                    J_syn_loss.update(var=J_syn_var)
                    J_recon_loss.update(var=J_recon_var)
                    J_soft_loss.update(var=J_soft_var)
                    J_gen_loss.update(var=J_gen_var)
                    cross_entropy_loss.update(cross_en_var)
                step += 1
                # print('learning rate %f' % _lr)

                # evaluation
                if step % bp_epoch == 0:
                    print('only eval eval')
                    # nmi_tr, f1_tr, recalls_tr = evaluation.Evaluation(
                    #     stream_train_eval, image_mean, sess, x_raw, label_raw, is_Training, embedding_z, 98, neighbours)
                    nmi_te, f1_te, recalls_te = evaluation.Evaluation(
                        stream_test, image_mean, sess, x_raw, label_raw, is_Training, embedding_z, 98, neighbours)

                    # Summary
                    eval_summary = tf.Summary()
                    # eval_summary.value.add(tag='train nmi', simple_value=nmi_tr)
                    # eval_summary.value.add(tag='train f1', simple_value=f1_tr)
                    # for i in range(0, np.shape(neighbours)[0]):
                    #     eval_summary.value.add(tag='Recall@%d train' % neighbours[i], simple_value=recalls_tr[i])
                    eval_summary.value.add(tag='test nmi', simple_value=nmi_te)
                    eval_summary.value.add(tag='test f1', simple_value=f1_te)
                    for i in range(0, np.shape(neighbours)[0]):
                        eval_summary.value.add(tag='Recall@%d test' % neighbours[i], simple_value=recalls_te[i])
                    J_m_loss.write_to_tfboard(eval_summary)
                    wd_Loss.write_to_tfboard(eval_summary)
                    eval_summary.value.add(tag='learning_rate', simple_value=_lr)
                    if args.HDML:
                        J_syn_loss.write_to_tfboard(eval_summary)
                        J_metric_loss.write_to_tfboard(eval_summary)
                        J_soft_loss.write_to_tfboard(eval_summary)
                        J_recon_loss.write_to_tfboard(eval_summary)
                        J_gen_loss.write_to_tfboard(eval_summary)
                        cross_entropy_loss.write_to_tfboard(eval_summary)
                    summary_writer.add_summary(eval_summary, step)
                    print('Summary written')
                    if nmi_te > max_nmi:
                        max_nmi = nmi_te
                        print("Saved")
                        saver.save(sess, os.path.join(LOGDIR, "model.ckpt"))
                    summary_writer.flush()
                    if step in [5632, 6848]:
                        _lr = _lr * 0.5

                    if step >= 5000:
                        bp_epoch = FLAGS.batch_per_epoch
                    if step >= FLAGS.max_steps:
                        os._exit()

if __name__ == '__main__':
    args = parser.parse_args()

    streams, summary_writer = initialize(args)
    x_raw, label_raw, is_Training, lr = placeholders()
    embedding_y_origin, embedding_z = configClassifier(args, x_raw, is_Training)
    wdLoss, label, J_m = configLoss(args, label_raw, embedding_z)
    J_m, Javg, Jgen, J_metric, J_gen, J_syn, cross_entropy, J_recon, J_soft = \
        configHDML(args, is_Training, embedding_y_origin, label, J_m) if args.HDML else J_m, 0, 0, 0, 0, 0, 0, 0, 0
    train_steps = configTrainSteps(args, J_m, J_metric, J_gen, cross_entropy)
    losses = (wdLoss, J_m, Javg, Jgen, J_metric, J_gen, J_syn, cross_entropy, J_recon, J_soft)
    configTfSession(args, streams, summary_writer, train_steps, losses)

    tf.app.run()