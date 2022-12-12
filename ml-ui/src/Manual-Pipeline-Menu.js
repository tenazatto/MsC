import * as React from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Snackbar from '@mui/material/Snackbar';
import Button from '@mui/material/Button';
import PlayArrowRoundedIcon from '@mui/icons-material/PlayArrowRounded';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';

import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import Select from '@mui/material/Select';

import {
  setPipelineResults,
  selectPipelineResults
} from './store';
import store from './store';
import axios from 'axios';


function ManualPipelineMenu(props) {
  const [validPlanningVisible, setValidPlanningVisible] = React.useState(false);
  const [biasReductionStep, setBiasReductionStep] = React.useState('pre');
  const [trainAlgorithm, setTrainAlgorithm] = React.useState('Algorithms.LOGISTIC_REGRESSION');
  const [reductionBiasAlgorithm, setReductionBiasAlgorithm] = React.useState('UnbiasDataAlgorithms.REWEIGHING');
  const [dataset, setDataset] = React.useState('Datasets.GERMAN_CREDIT');
  const [protectedAtt, setProtectedAtt] = React.useState('Preprocessors.AGE');
  const [stepPipeline, setStepPipeline] = React.useState(0);

  const [expandedAccordion, setExpandedAccordion] = React.useState(false);

  const [trainAlgorithmMessage, setTrainAlgorithmMessage] = React.useState('Algoritmo de treinamento sem redução de viés');
  const [reductionBiasAlgorithmMessage, setReductionBiasAlgorithmMessage] = React.useState('Algoritmo de redução de viés no pré-processamento');

  const steps = [
    'Parametrização',
    'Execução',
    'Resultado',
  ];
  
  let pipelineResults = useSelector(selectPipelineResults);

  const handleRadio = (event) => {
    setBiasReductionStep(event.target.value);

    if (event.target.value === 'pre') {
      setTrainAlgorithm('Algorithms.LOGISTIC_REGRESSION');
      setReductionBiasAlgorithm('UnbiasDataAlgorithms.REWEIGHING');
      setTrainAlgorithmMessage('Algoritmo de treinamento sem redução de viés');
      setReductionBiasAlgorithmMessage('Algoritmo de redução de viés no pré-processamento');
    } else if (event.target.value === 'in') {
      setTrainAlgorithm('UnbiasInProcAlgorithms.PREJUDICE_REMOVER');
      setTrainAlgorithmMessage('Algoritmo de treinamento com redução de viés');
    } else if (event.target.value === 'post') {
      setTrainAlgorithm('Algorithms.LOGISTIC_REGRESSION');
      setReductionBiasAlgorithm('UnbiasPostProcAlgorithms.EQUALIZED_ODDS');
      setTrainAlgorithmMessage('Algoritmo de treinamento sem redução de viés');
      setReductionBiasAlgorithmMessage('Algoritmo de redução de viés no pós-processamento');
    } else {
      setTrainAlgorithm('Algorithms.LOGISTIC_REGRESSION');
      setTrainAlgorithmMessage('Algoritmo de treinamento sem redução de viés');
    }
  }

  const handleTrainAlgorithmChange = (event) => {
    setTrainAlgorithm(event.target.value);
  }

  const handleReductionBiasAlgorithmChange = (event) => {
    setReductionBiasAlgorithm(event.target.value);
  }

  const handleDatasetChange = (event) => {
    setDataset(event.target.value);

    if (event.target.value === 'Datasets.ADULT_INCOME') {
      setProtectedAtt('Preprocessors.SEX');
    } else if (event.target.value === 'Datasets.GERMAN_CREDIT') {
      setProtectedAtt('Preprocessors.AGE');
    } else {
      setProtectedAtt('Preprocessors.INCOME');
    }
  }

  const handleProtectedAttChange = (event) => {
    setProtectedAtt(event.target.value);
  }

  const handleCloseSuccessToast = () => {
    setValidPlanningVisible(false);
  }

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpandedAccordion(isExpanded ? panel : false);
  }

  const executeManualPipeline = (event) => {
    event.preventDefault();

    setStepPipeline(1)

    let data = undefined

    if (biasReductionStep === 'pre') {
      data = {
        dataset: dataset,
        preprocessor: protectedAtt,
        preproc_algorithm: reductionBiasAlgorithm,
        inproc_algorithm: trainAlgorithm,
        postproc_algorithm: 'UnbiasPostProcAlgorithms.NOTHING'
      }
    } else if (biasReductionStep === 'post') {
      data = {
        dataset: dataset,
        preprocessor: protectedAtt,
        preproc_algorithm: 'UnbiasDataAlgorithms.NOTHING',
        inproc_algorithm: trainAlgorithm,
        postproc_algorithm: reductionBiasAlgorithm
      }
    } else {
      data = {
        dataset: dataset,
        preprocessor: protectedAtt,
        preproc_algorithm: 'UnbiasDataAlgorithms.NOTHING',
        inproc_algorithm: trainAlgorithm,
        postproc_algorithm: 'UnbiasPostProcAlgorithms.NOTHING'
      }
    }

    axios.post('http://localhost:8080/pipeline/manual/single', data)
         .then((response) =>{
            setStepPipeline(2)
            store.dispatch(setPipelineResults(response.data));
         });

    setValidPlanningVisible(true);
  }

  return (
    <form onSubmit={executeManualPipeline}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block'}}>Pipeline Manual</h2>
          {stepPipeline < 1 ? <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<PlayArrowRoundedIcon />}>Executar</Button>: ''}
        </span>

        <Box sx={{ display: 'flex', justifyContent: 'center'}}>
          <Stepper sx={{width: '70%', textAlign: 'center'}} activeStep={stepPipeline}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </Box>

        {stepPipeline === 0 ?
        <Box sx={{textAlign: 'center'}}>
          <Box sx={{marginLeft: ((document.getElementsByTagName("form")[0].clientWidth-550)/2) + 'px'}}>
            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '15px', fontSize: '14px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px', marginLeft: '50px'}}>Conjunto de dados: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '35px' }}>
                <Select
                  sx={{fontSize: '14px'}}
                  value={dataset}
                  onChange={handleDatasetChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Datasets.ADULT_INCOME'}>Adult Income Dataset</MenuItem>
                  <MenuItem value={'Datasets.GERMAN_CREDIT'}>German Credit Dataset</MenuItem>
                  <MenuItem value={'Datasets.LENDINGCLUB'}>Lendingclub Dataset</MenuItem>
                </Select>
                <FormHelperText>Conjunto de dados a ser treinado</FormHelperText>
              </FormControl>
            </Box>

            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '15px', fontSize: '14px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px', marginLeft: '50px'}}>Atributo Protegido: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '35px' }}>
                {dataset === 'Datasets.ADULT_INCOME' ?
                <Select
                  sx={{fontSize: '14px'}}
                  value={protectedAtt}
                  onChange={handleProtectedAttChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Preprocessors.SEX'}>Sexo (Masculino/Feminino)</MenuItem>
                </Select>
                : dataset === 'Datasets.GERMAN_CREDIT' ?
                <Select
                  sx={{fontSize: '14px'}}
                  value={protectedAtt}
                  onChange={handleProtectedAttChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Preprocessors.AGE'}>Idade (-25 anos/+25 anos)</MenuItem>
                  <MenuItem value={'Preprocessors.FOREIGN'}>Nacionalidade (Local/Estrangeiro)</MenuItem>
                </Select>
                :
                <Select
                  sx={{fontSize: '14px'}}
                  value={protectedAtt}
                  onChange={handleProtectedAttChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Preprocessors.INCOME'}>Renda (-1 Salário Mínimo/1+ Salários Mínimos)</MenuItem>
                </Select>
                }
                <FormHelperText>Atributo protegido para medir justiça</FormHelperText>
              </FormControl>
            </Box>
          </Box>
          
          <FormControl sx={{marginTop: '10px'}}>
            <FormLabel sx={{fontSize: '14px'}} id="bias-reduction-label">Redução de viés será aplicada em qual etapa do Pipeline?</FormLabel>
            <RadioGroup
              row
              aria-labelledby="bias-reduction-label"
              name="bias-reduction-step"
              value={biasReductionStep}
              onChange={handleRadio}
            >
              <FormControlLabel sx={{fontSize: '10px'}} value="pre" control={<Radio />} label="Pré-Processamento/Dados" />
              <FormControlLabel sx={{fontSize: '10px'}} value="in" control={<Radio />} label="Processamento/Treinamento" />
              <FormControlLabel sx={{fontSize: '10px'}} value="post" control={<Radio />} label="Pós-Processamento/Avaliação" />
              <FormControlLabel sx={{fontSize: '10px'}} value="nothing" control={<Radio />} label="Nenhum (Executar treinamento convencional)"/>
            </RadioGroup>
          </FormControl>

          <Box sx={{marginLeft: ((document.getElementsByTagName("form")[0].clientWidth-550)/2) + 'px'}}>
            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '15px', fontSize: '14px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px'}}>Algoritmo de treinamento: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '35px' }}>
                {biasReductionStep !== 'in' ?
                <Select
                  sx={{fontSize: '14px'}}
                  value={trainAlgorithm}
                  onChange={handleTrainAlgorithmChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Algorithms.LOGISTIC_REGRESSION'}>Logistic Regression</MenuItem>
                  <MenuItem value={'Algorithms.RANDOM_FOREST'}>Random Forest</MenuItem>
                  <MenuItem value={'Algorithms.GRADIENT_BOOST'}>Gradient Boost</MenuItem>
                  <MenuItem value={'Algorithms.NAIVE_BAYES'}>Naive Bayes</MenuItem>
                  <MenuItem value={'Algorithms.SUPPORT_VECTOR_MACHINES'}>Support Vector Machines</MenuItem>
                </Select>
                :
                <Select
                  sx={{fontSize: '14px'}}
                  value={trainAlgorithm}
                  onChange={handleTrainAlgorithmChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'UnbiasInProcAlgorithms.PREJUDICE_REMOVER'}>Prejudice Remover</MenuItem>
                  <MenuItem value={'UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING'}>Adversarial Debiasing</MenuItem>
                  <MenuItem value={'UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION'}>Exponentiated Gradient Reduction</MenuItem>
                  <MenuItem value={'UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS'}>Rich Subgroup Fairness</MenuItem>
                  <MenuItem value={'UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER'}>Meta Fair Classifier</MenuItem>
                  <MenuItem value={'UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION'}>Grid Search Reduction</MenuItem>
                </Select>}
                <FormHelperText>{trainAlgorithmMessage}</FormHelperText>
              </FormControl>
            </Box>

            {(biasReductionStep === 'pre' || biasReductionStep === 'post') ?
            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '15px', fontSize: '14px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px'}}>Algoritmo de redução de viés: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '15px' }}>
                {biasReductionStep === 'pre' ?
                <Select
                  sx={{fontSize: '14px'}}
                  value={reductionBiasAlgorithm}
                  onChange={handleReductionBiasAlgorithmChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'UnbiasDataAlgorithms.REWEIGHING'}>Reweighing</MenuItem>
                  <MenuItem value={'UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER'}>Disparate Impact Remover</MenuItem>
                  <MenuItem value={'UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING'}>Optimized Preprocessing</MenuItem>
                  <MenuItem value={'UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS'}>Learning Fair Representations</MenuItem>
                </Select>
                :
                <Select
                  sx={{fontSize: '14px'}}
                  value={reductionBiasAlgorithm}
                  onChange={handleReductionBiasAlgorithmChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'UnbiasPostProcAlgorithms.EQUALIZED_ODDS'}>Equalized Odds</MenuItem>
                  <MenuItem value={'UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS'}>Calibrated Equalized Odds</MenuItem>
                  <MenuItem value={'UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION'}>Reject Option Classification</MenuItem>
                </Select>
                }
                <FormHelperText>{reductionBiasAlgorithmMessage}</FormHelperText>
              </FormControl>
            </Box>
            : ''}
          </Box>
        </Box>
        : stepPipeline === 1 ? <Box sx={{textAlign: 'center'}}>Executando Pipeline...</Box> 
        : <Box sx={{marginTop: '20px'}}>
            <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
              <Box sx={{textAlign: 'center', width: '84%'}}>
                <Accordion expanded={expandedAccordion === 'execution'} onChange={handleAccordionChange('execution')}>
                  <AccordionSummary
                    sx={{backgroundColor: '#00ddff'}}
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1bh-content"
                    id="panel1bh-header"
                  >
                    <Typography sx={{ width: '33%', flexShrink: 0 }}>
                      Execução
                    </Typography>
                    <Typography sx={{ color: 'text.secondary' }}>Parâmetros utilizados e estatísticas da execução</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>
                      <table>
                        <tbody>
                          <tr>
                            <td>Checksum do conjunto de dados</td>
                            <td style={{fontSize: '13px'}}>{pipelineResults.data_checksum}</td>
                          </tr>
                          <tr>
                            <td>Conjunto de dados utilizado</td>
                            <td>{pipelineResults.dataset}</td>
                          </tr>
                          <tr>
                            <td>Atributo protegido</td>
                            <td>{pipelineResults.preprocessor}</td>
                          </tr>
                          <tr>
                            <td>Algoritmo de redução de viés no dado</td>
                            <td>{pipelineResults.unbias_data_algorithm}</td>
                          </tr>
                          <tr>
                            <td>Algoritmo de treinamento (redução de viés: {pipelineResults.unbias_data_algorithm === 'UnbiasDataAlgorithms.NOTHING' 
                                                                            && pipelineResults.unbias_postproc_algorithm === 'UnbiasDataAlgorithms.NOTHING' ? 
                                                                            'Não' : 'Sim'})</td>
                            <td>{pipelineResults.inproc_algorithm}</td>
                          </tr>
                          <tr>
                            <td>Algoritmo de redução de viés no pós-processamento</td>
                            <td>{pipelineResults.unbias_postproc_algorithm}</td>
                          </tr>
                          <tr>
                            <td>Data de início da execução</td>
                            <td>{pipelineResults.date_start}</td>
                          </tr>
                          <tr>
                            <td>Data de fim da execução</td>
                            <td>{pipelineResults.date_end}</td>
                          </tr>
                          <tr>
                            <td>Tempo de Execução</td>
                            <td>{pipelineResults.execution_time_ms + ' ms'}</td>
                          </tr>
                        </tbody>
                      </table>
                    </Typography>
                  </AccordionDetails>
                </Accordion>
                <Accordion expanded={expandedAccordion === 'performance-metrics'} onChange={handleAccordionChange('performance-metrics')}>
                  <AccordionSummary
                    sx={{backgroundColor: '#00ddff'}}
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel2bh-content"
                    id="panel2bh-header"
                  >
                    <Typography sx={{ width: '33%', flexShrink: 0 }}>
                      Métricas de Performance
                    </Typography>
                    <Typography sx={{ color: 'text.secondary' }}>Métricas relacionadas a performance do modelo</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>
                      <table>
                        <tbody>
                          {pipelineResults.performance_metrics.accuracy ?
                          <tr>
                            <td>Acurácia</td>
                            <td>{pipelineResults.performance_metrics.accuracy.value}</td>
                          </tr> : ''}
                          {pipelineResults.performance_metrics.precision ?
                          <tr>
                            <td>Precisão</td>
                            <td>{pipelineResults.performance_metrics.precision.value}</td>
                          </tr> : ''}
                          {pipelineResults.performance_metrics.recall ?
                          <tr>
                            <td>Recall</td>
                            <td>{pipelineResults.performance_metrics.recall.value}</td>
                          </tr> : ''}
                          {pipelineResults.performance_metrics.f1_score ?
                          <tr>
                            <td>F1-Score</td>
                            <td>{pipelineResults.performance_metrics.f1_score.value}</td>
                          </tr> : ''}
                          {pipelineResults.performance_metrics.auc ?
                          <tr>
                            <td>AUC (Area Under the ROC Curve)</td>
                            <td>{pipelineResults.performance_metrics.auc.value}</td>
                          </tr> : ''}
                        </tbody>
                      </table>
                    </Typography>
                  </AccordionDetails>
                </Accordion>
                <Accordion expanded={expandedAccordion === 'fairness-metrics'} onChange={handleAccordionChange('fairness-metrics')}>
                  <AccordionSummary
                    sx={{backgroundColor: '#00ddff'}}
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel3bh-content"
                    id="panel3bh-header"
                  >
                    <Typography sx={{ width: '33%', flexShrink: 0 }}>
                      Métricas de Fairness
                    </Typography>
                    <Typography sx={{ color: 'text.secondary' }}>Métricas relacionadas a justiça do modelo</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>
                      <table>
                        <tbody>
                          {pipelineResults.fairness_metrics.statistical_parity_difference ?
                          <tr>
                            <td>Statistical Parity Difference</td>
                            <td>{pipelineResults.fairness_metrics.statistical_parity_difference.value}</td>
                          </tr> : ''}
                          {pipelineResults.fairness_metrics.disparate_impact ?
                          <tr>
                            <td>Disparate Impact</td>
                            <td>{pipelineResults.fairness_metrics.disparate_impact.value}</td>
                          </tr> : ''}
                          {pipelineResults.fairness_metrics.average_abs_odds_difference ?
                          <tr>
                            <td>Average Odds Difference</td>
                            <td>{pipelineResults.fairness_metrics.average_abs_odds_difference.value}</td>
                          </tr> : ''}
                          {pipelineResults.fairness_metrics.equal_opportunity_difference ?
                          <tr>
                            <td>Equal Opportunity Difference</td>
                            <td>{pipelineResults.fairness_metrics.equal_opportunity_difference.value}</td>
                          </tr> : ''}
                          {pipelineResults.fairness_metrics.theil_index ?
                          <tr>
                            <td>Theil Index</td>
                            <td>{pipelineResults.fairness_metrics.theil_index.value}</td>
                          </tr> : ''}
                        </tbody>
                      </table>
                    </Typography>
                  </AccordionDetails>
                </Accordion>
                <Accordion expanded={expandedAccordion === 'score'} onChange={handleAccordionChange('score')}>
                  <AccordionSummary
                    sx={{backgroundColor: '#00ddff'}}
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel4bh-content"
                    id="panel4bh-header"
                  >
                    <Typography sx={{ width: '33%', flexShrink: 0 }}>
                      Pontuação
                    </Typography>
                    <Typography sx={{ color: 'text.secondary' }}>Pontuação dada de acordo com os pesos e métricas utilizadas para a execução</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>
                      <table>
                        <tbody>
                          <tr>
                            <td>Pontuação das métricas de performance</td>
                            <td>{pipelineResults.scores.performance_score}</td>
                          </tr>
                          <tr>
                          <td>Pontuação das métricas de fairness</td>
                            <td>{pipelineResults.scores.fairness_score}</td>
                          </tr>
                          <tr>
                          <td>Pontuação geral</td>
                            <td>{pipelineResults.scores.group_score}</td>
                          </tr>
                        </tbody>
                      </table>
                    </Typography>
                  </AccordionDetails>
                </Accordion>
              </Box>
            </Box>
          </Box>}

        <Snackbar open={validPlanningVisible} autoHideDuration={6000} onClose={handleCloseSuccessToast}>
          <Alert onClose={handleCloseSuccessToast} severity="success">
            <AlertTitle><strong>Sucesso!</strong></AlertTitle>
            Execução será realizada em alguns segundos
          </Alert>
        </Snackbar>
      </Box>
    </form>
  );
}

export default ManualPipelineMenu;