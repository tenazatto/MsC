import * as React from 'react';
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

import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import Select from '@mui/material/Select';

import axios from 'axios';


function ManualPipelineMenu(props) {
  const [validPlanningVisible, setValidPlanningVisible] = React.useState(false);
  const [biasReductionStep, setBiasReductionStep] = React.useState('pre');
  const [trainAlgorithm, setTrainAlgorithm] = React.useState('Algorithms.LOGISTIC_REGRESSION');
  const [reductionBiasAlgorithm, setReductionBiasAlgorithm] = React.useState('UnbiasDataAlgorithms.REWEIGHING');
  const [dataset, setDataset] = React.useState('Datasets.GERMAN_CREDIT');
  const [protectedAtt, setProtectedAtt] = React.useState('Preprocessors.AGE');

  const [trainAlgorithmMessage, setTrainAlgorithmMessage] = React.useState('Algoritmo de treinamento sem redução de viés');
  const [reductionBiasAlgorithmMessage, setReductionBiasAlgorithmMessage] = React.useState('Algoritmo de redução de viés no pré-processamento');

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
    } else {
      setProtectedAtt('Preprocessors.AGE');
    }
  }

  const handleProtectedAttChange = (event) => {
    setProtectedAtt(event.target.value);
  }

  const handleCloseSuccessToast = () => {
    setValidPlanningVisible(false);
  }

  const executeManualPipeline = (event) => {
    event.preventDefault();

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
            console.log(response.data);
         });

    setValidPlanningVisible(true);
  }

  return (
    <form onSubmit={executeManualPipeline}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block'}}>Pipeline Manual</h2>
          <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<PlayArrowRoundedIcon />}>Executar</Button>
        </span>

        <Box sx={{textAlign: 'center'}}>
          <Box sx={{marginLeft: ((document.getElementsByTagName("form")[0].clientWidth-550)/2) + 'px'}}>
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
                </Select>
                <FormHelperText>Conjunto de dados a ser treinado</FormHelperText>
              </FormControl>
            </Box>

            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '20px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px', marginLeft: '50px'}}>Atributo Protegido: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '35px' }}>
                {dataset === 'Datasets.ADULT_INCOME' ?
                <Select
                  value={protectedAtt}
                  onChange={handleProtectedAttChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Preprocessors.SEX'}>Sexo (Masculino/Feminino)</MenuItem>
                </Select>
                :
                <Select
                  value={protectedAtt}
                  onChange={handleProtectedAttChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Preprocessors.AGE'}>Idade (-25 anos/+25 anos)</MenuItem>
                  <MenuItem value={'Preprocessors.FOREIGN'}>Nacionalidade (Local/Estrangeiro)</MenuItem>
                </Select>
                }
                <FormHelperText>Atributo protegido para medir justiça</FormHelperText>
              </FormControl>
            </Box>
          </Box>
          
          <FormControl sx={{marginTop: '10px'}}>
            <FormLabel id="bias-reduction-label">Redução de viés será aplicada em qual etapa do Pipeline?</FormLabel>
            <RadioGroup
              row
              aria-labelledby="bias-reduction-label"
              name="bias-reduction-step"
              value={biasReductionStep}
              onChange={handleRadio}
            >
              <FormControlLabel value="pre" control={<Radio />} label="Pré-Processamento/Dados" />
              <FormControlLabel value="in" control={<Radio />} label="Processamento/Treinamento" />
              <FormControlLabel value="post" control={<Radio />} label="Pós-Processamento/Avaliação" />
              <FormControlLabel value="nothing" control={<Radio />} label="Nenhum (Executar treinamento convencional)"/>
            </RadioGroup>
          </FormControl>

          <Box sx={{marginLeft: ((document.getElementsByTagName("form")[0].clientWidth-550)/2) + 'px'}}>
            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '20px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px'}}>Algoritmo de treinamento: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '35px' }}>
                {biasReductionStep !== 'in' ?
                <Select
                  value={trainAlgorithm}
                  onChange={handleTrainAlgorithmChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                >
                  <MenuItem value={'Algorithms.LOGISTIC_REGRESSION'}>Logistic Regression</MenuItem>
                  <MenuItem value={'Algorithms.RANDOM_FOREST'}>Random Forest</MenuItem>
                  <MenuItem value={'Algorithms.GRADIENT_BOOST'}>Gradient Boost</MenuItem>
                  <MenuItem value={'Algorithms.SUPPORT_VECTOR_MACHINES'}>Support Vector Machines</MenuItem>
                </Select>
                :
                <Select
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
            <Box sx={{ display: 'flex', maxWidth: 550, marginTop: '20px' }}>
              <span style={{whiteSpace: 'nowrap', verticalAlign: 'middle', paddingTop: '20px'}}>Algoritmo de redução de viés: </span>
              <FormControl sx={{ m: 1, width: 300, marginLeft: '15px' }}>
                {biasReductionStep === 'pre' ?
                <Select
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