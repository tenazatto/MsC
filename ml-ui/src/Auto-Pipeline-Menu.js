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
  selectPipelineResults,
  setPipelineResultsAuto,
  selectPipelineResultsAuto
} from './store';
import store from './store';
import axios from 'axios';

function AutoPipelineMenu(props) {
  const [validPlanningVisible, setValidPlanningVisible] = React.useState(false);
  const [dataset, setDataset] = React.useState('Datasets.GERMAN_CREDIT');
  const [stepPipeline, setStepPipeline] = React.useState(0);
  const [chosenPipeline, setChosenPipeline] = React.useState(0);
  const [expandedAccordion, setExpandedAccordion] = React.useState(false);

  const steps = [
    'Parametrização',
    'Análise',
    'Opções',
    'Execução',
    'Resultado',
  ];

  let pipelineResultsAuto = useSelector(selectPipelineResultsAuto);
  let finalPipelineResults = useSelector(selectPipelineResults);

  const handleDatasetChange = (event) => {
    setDataset(event.target.value);
  }

  const handleRadio = (event) => {
    setChosenPipeline(event.target.value);
  }

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpandedAccordion(isExpanded ? panel : false);
  }

  const handleCloseSuccessToast = () => {
    setValidPlanningVisible(false);
  }

  const executeAutoPipeline = (event) => {
    event.preventDefault();

    if (stepPipeline === 0) {
      setStepPipeline(1)
    
      let data = {
        params: {
          dataset: dataset,
          num_pipelines: 5
        }
      }

      axios.get('http://localhost:8080/pipeline/auto/plans', data)
            .then((response) =>{
              setStepPipeline(2)
              store.dispatch(setPipelineResultsAuto(response.data));
            });
    }

    if (stepPipeline === 2) {
      setStepPipeline(3)
    
      let data = {
        dataset: pipelineResultsAuto.pipelines[chosenPipeline].dataset,
        preprocessor: pipelineResultsAuto.pipelines[chosenPipeline].preprocessor,
        preproc_algorithm: pipelineResultsAuto.pipelines[chosenPipeline].unbias_data_algorithm,
        inproc_algorithm: pipelineResultsAuto.pipelines[chosenPipeline].inproc_algorithm,
        postproc_algorithm: pipelineResultsAuto.pipelines[chosenPipeline].unbias_postproc_algorithm
      }

      axios.post('http://localhost:8080/pipeline/auto/single', data)
            .then((response) =>{
              setStepPipeline(4)
              store.dispatch(setPipelineResults(response.data));
            });
    }

    setValidPlanningVisible(true);
  }

  return (
    <form onSubmit={executeAutoPipeline}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block'}}>Pipeline Autônomo</h2>
          {(stepPipeline === 0 || stepPipeline === 2) ? <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<PlayArrowRoundedIcon />}>{stepPipeline === 0 ? 'Análise' : 'Executar'}</Button>: ''}
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
        <Box>
          <Box sx={{marginLeft: ((document.getElementsByTagName("form")[0].clientWidth-550)/2) + 'px', textAlign: 'Center'}}>
            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '20px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px', marginLeft: '50px'}}>Conjunto de dados: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '35px' }}>
                <Select
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
          </Box>
          <div style={{marginTop: '35px'}}>Clique em <strong>EXECUTAR</strong> para iniciar a execução</div>
          <div>Pipeline será executado de acordo com as configurações salvas nos menus de configuração</div>
        </Box>
        : stepPipeline === 1 ? <Box sx={{textAlign: 'center'}}>Verificando melhor Pipeline...</Box> 
        : stepPipeline === 2 ? <FormControl sx={{marginTop: '20px'}}>
            <FormLabel sx={{textAlign: 'center'}} id="choose-pipeline-label">Escolha o pipeline a ser executado</FormLabel>
            <RadioGroup
              row
              aria-labelledby="choose-pipeline-label"
              name="choose-pipeline-step"
              value={chosenPipeline}
              onChange={handleRadio}
            >     
              {pipelineResultsAuto.pipelines.map((pipelineResults, index) => 
              <Box sx={{marginTop: '20px'}}>
                <Box sx={{marginLeft:'8%'}}>
                  <FormControlLabel value={index} control={<Radio />} label={'Pipeline '+(index+1)} />
                </Box>
                <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                  <Box sx={{textAlign: 'center', width: '84%'}}>
                    <Accordion expanded={expandedAccordion === 'execution-'+index} onChange={handleAccordionChange('execution-'+index)}>
                      <AccordionSummary
                        sx={{backgroundColor: '#00ddff'}}
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={'panel1bh-content-'+index}
                        id={'panel1bh-header-'+index}
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
                                                                                'Sim' : 'Não'})</td>
                                <td>{pipelineResults.inproc_algorithm}</td>
                              </tr>
                              <tr>
                                <td>Algoritmo de redução de viés no pós-processamento</td>
                                <td>{pipelineResults.unbias_postproc_algorithm}</td>
                              </tr>
                            </tbody>
                          </table>
                        </Typography>
                      </AccordionDetails>
                    </Accordion>
                    <Accordion expanded={expandedAccordion === 'performance-metrics-'+index} onChange={handleAccordionChange('performance-metrics-'+index)}>
                      <AccordionSummary
                        sx={{backgroundColor: '#00ddff'}}
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={'panel2bh-content-'+index}
                        id={'panel2bh-header-'+index}
                      >
                        <Typography sx={{ width: '33%', flexShrink: 0 }}>
                          Métricas de Performance
                        </Typography>
                        <Typography sx={{ color: 'text.secondary' }}>Métricas relacionadas a performance do modelo de execução mais recente</Typography>
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
                    <Accordion expanded={expandedAccordion === 'fairness-metrics-'+index} onChange={handleAccordionChange('fairness-metrics-'+index)}>
                      <AccordionSummary
                        sx={{backgroundColor: '#00ddff'}}
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={'panel3bh-content-'+index}
                        id={'panel3bh-header-'+index}
                      >
                        <Typography sx={{ width: '33%', flexShrink: 0 }}>
                          Métricas de Fairness
                        </Typography>
                        <Typography sx={{ color: 'text.secondary' }}>Métricas relacionadas a justiça do modelo de execução mais recente</Typography>
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
                    <Accordion expanded={expandedAccordion === 'score-'+index} onChange={handleAccordionChange('score-'+index)}>
                      <AccordionSummary
                        sx={{backgroundColor: '#00ddff'}}
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={'panel4bh-content-'+index}
                        id={'panel4bh-header-'+index}
                      >
                        <Typography sx={{ width: '33%', flexShrink: 0 }}>
                          Pontuação
                        </Typography>
                        <Typography sx={{ color: 'text.secondary' }}>Pontuação dada de acordo com os pesos e métricas utilizadas com base em todas as execuções</Typography>
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
              </Box>)}
            </RadioGroup>
          </FormControl>
          : stepPipeline === 3 ? <Box sx={{textAlign: 'center'}}>Executando melhor Pipeline...</Box>
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
                            <td style={{fontSize: '13px'}}>{finalPipelineResults.data_checksum}</td>
                          </tr>
                          <tr>
                            <td>Conjunto de dados utilizado</td>
                            <td>{finalPipelineResults.dataset}</td>
                          </tr>
                          <tr>
                            <td>Atributo protegido</td>
                            <td>{finalPipelineResults.preprocessor}</td>
                          </tr>
                          <tr>
                            <td>Algoritmo de redução de viés no dado</td>
                            <td>{finalPipelineResults.unbias_data_algorithm}</td>
                          </tr>
                          <tr>
                            <td>Algoritmo de treinamento (redução de viés: {finalPipelineResults.unbias_data_algorithm === 'UnbiasDataAlgorithms.NOTHING' 
                                                                            && finalPipelineResults.unbias_postproc_algorithm === 'UnbiasDataAlgorithms.NOTHING' ? 
                                                                            'Não' : 'Sim'})</td>
                            <td>{finalPipelineResults.inproc_algorithm}</td>
                          </tr>
                          <tr>
                            <td>Algoritmo de redução de viés no pós-processamento</td>
                            <td>{finalPipelineResults.unbias_postproc_algorithm}</td>
                          </tr>
                          <tr>
                            <td>Data de início da execução</td>
                            <td>{finalPipelineResults.date_start}</td>
                          </tr>
                          <tr>
                            <td>Data de fim da execução</td>
                            <td>{finalPipelineResults.date_end}</td>
                          </tr>
                          <tr>
                            <td>Tempo de Execução</td>
                            <td>{finalPipelineResults.execution_time_ms + ' ms'}</td>
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
                          {finalPipelineResults.performance_metrics.accuracy ?
                          <tr>
                            <td>Acurácia</td>
                            <td>{finalPipelineResults.performance_metrics.accuracy.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.performance_metrics.precision ?
                          <tr>
                            <td>Precisão</td>
                            <td>{finalPipelineResults.performance_metrics.precision.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.performance_metrics.recall ?
                          <tr>
                            <td>Recall</td>
                            <td>{finalPipelineResults.performance_metrics.recall.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.performance_metrics.f1_score ?
                          <tr>
                            <td>F1-Score</td>
                            <td>{finalPipelineResults.performance_metrics.f1_score.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.performance_metrics.auc ?
                          <tr>
                            <td>AUC (Area Under the ROC Curve)</td>
                            <td>{finalPipelineResults.performance_metrics.auc.value}</td>
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
                          {finalPipelineResults.fairness_metrics.statistical_parity_difference ?
                          <tr>
                            <td>Statistical Parity Difference</td>
                            <td>{finalPipelineResults.fairness_metrics.statistical_parity_difference.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.fairness_metrics.disparate_impact ?
                          <tr>
                            <td>Disparate Impact</td>
                            <td>{finalPipelineResults.fairness_metrics.disparate_impact.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.fairness_metrics.average_abs_odds_difference ?
                          <tr>
                            <td>Average Odds Difference</td>
                            <td>{finalPipelineResults.fairness_metrics.average_abs_odds_difference.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.fairness_metrics.equal_opportunity_difference ?
                          <tr>
                            <td>Equal Opportunity Difference</td>
                            <td>{finalPipelineResults.fairness_metrics.equal_opportunity_difference.value}</td>
                          </tr> : ''}
                          {finalPipelineResults.fairness_metrics.theil_index ?
                          <tr>
                            <td>Theil Index</td>
                            <td>{finalPipelineResults.fairness_metrics.theil_index.value}</td>
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
                            <td>{finalPipelineResults.scores.performance_score}</td>
                          </tr>
                          <tr>
                          <td>Pontuação das métricas de fairness</td>
                            <td>{finalPipelineResults.scores.fairness_score}</td>
                          </tr>
                          <tr>
                          <td>Pontuação geral</td>
                            <td>{finalPipelineResults.scores.group_score}</td>
                          </tr>
                        </tbody>
                      </table>
                    </Typography>
                  </AccordionDetails>
                </Accordion>
                </Box>
              </Box>
            </Box> }

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

export default AutoPipelineMenu;