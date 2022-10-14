import os
import time
from functools import reduce

import pandas as pd
import requests
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from tqdm import tqdm


def german_data_to_csv():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('datasets/german.data', sep=' ')
    df.info()
    print(df)

    df['checking_account'] = df['checking_account'].map(
        {'A11': '<0', 'A12': '0<=x<200', 'A13': '>=200', 'A14': 'None'}).astype(str)
    df['credit_history'] = df['credit_history'].map(
        {'A30': 'no_credits_taken', 'A31': 'all_credits_paid_bank',
         'A32': 'existing_credits_paid', 'A33': 'delay_in_past', 'A34': 'critical'}).astype(str)
    df['purpose'] = df['purpose'].map(
        {'A40': 'car_new', 'A41': 'car_used', 'A42': 'furniture/equipment', 'A43': 'radio/tv',
         'A44': 'domestic_appliances', 'A45': 'repairs', 'A46': 'education', 'A47': 'vacation', 'A48': 'retraining',
         'A49': 'business', 'A410': 'others'}).astype(str)
    df['savings_account'] = df['savings_account'].map(
        {'A61': '<100', 'A62': '100<=x<500', 'A63': '500<=x<1000', 'A64': '>=1000', 'A65': 'unknown'}).astype(str)
    df['present_employment_since'] = df['present_employment_since'].map(
        {'A71': 'unemployed', 'A72': '<1', 'A73': '1<=x<4', 'A74': '4<=x<7', 'A75': '>=7'}).astype(str)
    df['personal_status_sex'] = df['personal_status_sex'].map(
        {'A91': 'male_divorced/separated', 'A92': 'female_divorced/separated/married', 'A93': 'male_single',
         'A94': 'male_married/widowed', 'A95': 'female_single'}).astype(str)
    df['other_debtors_guarantors'] = df['other_debtors_guarantors'].map(
        {'A101': 'None', 'A102': 'co-applicant', 'A103': 'guarantor'}).astype(str)
    df['property'] = df['property'].map(
        {'A121': 'real_estate', 'A122': 'savings_insurance', 'A123': 'car_other', 'A124': 'unknown'}).astype(str)
    df['installment_plans'] = df['installment_plans'].map(
        {'A141': 'bank', 'A142': 'stores', 'A143': 'None'}).astype(str)
    df['housing'] = df['housing'].map(
        {'A151': 'rent', 'A152': 'own', 'A153': 'for_free'}).astype(str)
    df['job'] = df['job'].map(
        {'A171': 'unemployed', 'A172': 'unskilled', 'A173': 'skilled', 'A174': 'management'}).astype(str)
    df['telephone'] = df['telephone'].map(
        {'A191': 'none', 'A192': 'yes'}).astype(str)
    df['foreign'] = df['foreign'].map(
        {'A201': 'yes', 'A202': 'no'}).astype(str)
    df['risk'] = df['risk'].map(
        {1: 'good', 2: 'bad'}).astype(str)

    print(df)
    df.to_csv('datasets/german_credit_data.csv')


def lending_club_data_to_csv():
    # Se o link para download não estiver mais disponível, acessar o link:
    # https://www.kaggle.com/datasets/wordsforthewise/lending-club
    # Baixar os Datasets, colocar em outro link e substituir os valores de accepted_url e rejected_url
    # Decisão de baixar os Datasets se deve a dois fatos:
    # - Os arquivos compactados somados possuem 600Mb de tamanho e o Git não lida tão bem com arquivos binários
    #
    # - Os arquivos CSV somados possuem 3Gb de tamanho
    SAMPLE_PERCENTAGE = 100
    QTD_COLUMNS_SELECTED = 20

    only_valid_status = lambda str: str == 'Fully Paid' or str == 'Charged Off'

    string_columns = ['id', 'member_id', 'title', 'url', 'desc']
    one_value_columns = ['pymnt_plan', 'out_prncp', 'out_prncp_inv', 'next_pymnt_d', 'hardship_flag', 'policy_code']
    output_label_columns = ['loan_status']
    protected_attribute_columns = ['annual_inc']
    columns_to_ignore = []
    columns_to_ignore.extend(string_columns)
    columns_to_ignore.extend(one_value_columns)

    label_feature_columns = ['term', 'grade', 'sub_grade', 'emp_title', 'emp_length', 'home_ownership',
                             'verification_status', 'issue_d', 'purpose', 'zip_code', 'addr_state',
                             'earliest_cr_line', 'initial_list_status', 'last_pymnt_d', 'last_credit_pull_d',
                             'application_type', 'verification_status_joint', 'sec_app_earliest_cr_line',
                             'hardship_type', 'hardship_reason', 'hardship_status', 'hardship_start_date',
                             'hardship_end_date', 'payment_plan_start_date', 'hardship_loan_status',
                             'disbursement_method', 'debt_settlement_flag', 'debt_settlement_flag_date',
                             'settlement_status', 'settlement_date']

    t0 = time.time()
    print('Fazendo Download dos datasets')
    if not os.path.isfile('datasets/accepted.tar.gz') and not os.path.isfile('datasets/accepted_2007_to_2018Q4.csv'):
        accepted_url = 'https://drive.google.com/uc?id=1stB1tEZJgx0Wl94EpeQaqKkH6rFOZnBs&export=download' \
                       '&confirm=t&uuid=baa1684a-fc2a-461b-b3c4-fd6f07016c3a'
        download_file(accepted_url, 'datasets', 'accepted.tar.gz')

    if not os.path.isfile('datasets/rejected.tar.gz') and not os.path.isfile('datasets/rejected_2007_to_2018Q4.csv'):
        rejected_url = 'https://drive.google.com/uc?id=1ZWXn0clcdQPsr60TcXItKGh6LjmA_buM&export=download' \
                       '&confirm=t&uuid=d470e210-bcc1-4840-b932-5d2391793325'
        download_file(rejected_url, 'datasets', 'rejected.tar.gz')
        df_rejected = pd.read_csv('datasets/rejected.tar.gz', compression='gzip', header=0, sep=',', dtype='str')

    print('Descomprimindo')
    df_accepted = pd.read_csv('datasets/accepted.tar.gz', compression='gzip', header=0, sep=',', dtype='str')

    print('Filtrando linhas e removendo colunas')
    df_variables = df_accepted.drop(columns=columns_to_ignore) \
        .loc[df_accepted['loan_status'].apply(only_valid_status)].fillna('0.0') \
        .sample(frac=SAMPLE_PERCENTAGE/100)
    df_output = pd.DataFrame()
    df_output.insert(0, 'loan_status', df_variables['loan_status'])
    df_variables = df_variables.drop(columns=output_label_columns)
    df_final = df_variables.copy()
    df_output_final = df_output.copy()

    print('Categorizando features')
    labels = [(col, df_variables[col].astype('category').cat.categories) for col in label_feature_columns]
    labels_encoded = {col: {cat: (n if '0.0' in category else n+1)
                            for n, cat in enumerate(category)}
                      for col, category in labels}

    df_output['loan_status'] = df_output['loan_status'].map({'Fully Paid': 1, 'Charged Off': 0})
    for label_column in label_feature_columns:
        df_variables[label_column] = df_variables[label_column].map(labels_encoded[label_column])

    print('Selecionando features')
    features_selected = SelectKBest(score_func=mutual_info_classif, k=QTD_COLUMNS_SELECTED)
    features_selected.fit_transform(df_variables, df_output)

    t1 = time.time()
    print('Obtendo estatísticas')
    print(f'Tempo de execução: {t1-t0} segundos')
    func_sum = lambda a, b: a+b
    features_selected_importance = reduce(func_sum, features_selected.scores_[features_selected.get_support()]) \
                                   / reduce(func_sum, features_selected.scores_)
    print(f'Importância das features selecionadas: {features_selected_importance*100}%')
    for protected_attribute in protected_attribute_columns:
        print(f'Importância da feature {protected_attribute}: '
              f'{features_selected.scores_[df_variables.get_loc(protected_attribute)] * 100}%')
    selected_column_indices = features_selected.get_support(indices=True)
    print(f'Features selecionadas: {df_variables.iloc[:, selected_column_indices].columns}')
    print('Produzindo CSV do dataset filtrado')
    df_final = df_final.iloc[:, selected_column_indices]
    for protected_attribute in protected_attribute_columns:
        if protected_attribute not in df_final.columns:
            df_final.insert(len(df_final.columns), protected_attribute, df_variables[protected_attribute])
    for output_label_column in output_label_columns:
        df_final.insert(len(df_final.columns), output_label_column, df_output_final[output_label_column])

    print(df_final)
    df_final.to_csv('datasets/lendingclub_dataset.csv', index=False)


def download_file(url, file_path, file_name):
    response = requests.get(url, stream=True)

    complete_file_path = file_path + '/' + file_name
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(complete_file_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
