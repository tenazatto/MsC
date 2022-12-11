import * as React from 'react';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Snackbar from '@mui/material/Snackbar';
import Button from '@mui/material/Button';
import SaveIcon from '@mui/icons-material/Save';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Checkbox from '@mui/material/Checkbox';
import Slider from '@mui/material/Slider';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import StorageOutlinedIcon from '@mui/icons-material/StorageOutlined';
import ModelTrainingIcon from '@mui/icons-material/ModelTraining';
import InsightsIcon from '@mui/icons-material/Insights';
import CheckIcon from '@mui/icons-material/Check';

import {
  selectValidAlgorithms,
  setValidAlgorithms,
  invertValidAlgorithmsSelected
} from './store';
import store from './store';
import { useSelector } from 'react-redux';
import axios from 'axios';

function PlanningMenu(props) {
  const [validPlanningVisible, setValidPlanningVisible] = React.useState(false);
  const [thresholdValue, setThresholdValue] = React.useState([0, 0]);

  const debugAPI = true;

  const [planningState, setPlanningState] = React.useState({
    ml_pipeline: true,
    ml_data_checksum: true,
    ml_algorithm_validation: true,
    ml_pipeline_threshold: true,
  });

  let validAlgorithmsSelected = useSelector(selectValidAlgorithms);
  let validAlgorithms = [
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Logistic Regression", "Sem método", "Sem método"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.EQUALIZED_ODDS"],
      labels: ["Logistic Regression", "Sem método", "Equalized Odds"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS"],
      labels: ["Logistic Regression", "Sem método", "Calibrated Equalized Odds"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION"],
      labels: ["Logistic Regression", "Sem método", "Reject Option Classification"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.REWEIGHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Logistic Regression", "Reweighing", "Sem método"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Logistic Regression", "Disparate Impact Remover", "Sem método"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Logistic Regression", "Optimized Preprocessing", "Sem método"],
      selected: true
    },
    {
      options: ["Algorithms.LOGISTIC_REGRESSION", "UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Logistic Regression", "Learning Fair Representations", "Sem método"],
      selected: true
    },
    {
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Random Forest", "Sem método", "Sem método"],
      selected: true
    },
    {
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.EQUALIZED_ODDS"],
      labels: ["Random Forest", "Sem método", "Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS"],
      labels: ["Random Forest", "Sem método", "Calibrated Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION"],
      labels: ["Random Forest", "Sem método", "Reject Option Classification"],
      selected: true
    },
    {   
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.REWEIGHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Random Forest", "Reweighing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Random Forest", "Disparate Impact Remover", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Random Forest", "Optimized Preprocessing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.RANDOM_FOREST", "UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Random Forest", "Learning Fair Representations", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Gradient Boost", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.EQUALIZED_ODDS"],
      labels: ["Gradient Boost", "Sem método", "Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS"],
      labels: ["Gradient Boost", "Sem método", "Calibrated Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION"],
      labels: ["Gradient Boost", "Sem método", "Reject Option Classification"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.REWEIGHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Gradient Boost", "Reweighing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Gradient Boost", "Disparate Impact Remover", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Gradient Boost", "Optimized Preprocessing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.GRADIENT_BOOST", "UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Gradient Boost", "Learning Fair Representations", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Naive Bayes", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.EQUALIZED_ODDS"],
      labels: ["Naive Bayes", "Sem método", "Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS"],
      labels: ["Naive Bayes", "Sem método", "Calibrated Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION"],
      labels: ["Naive Bayes", "Sem método", "Reject Option Classification"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.REWEIGHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Naive Bayes", "Reweighing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Naive Bayes", "Disparate Impact Remover", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Naive Bayes", "Optimized Preprocessing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.NAIVE_BAYES", "UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Naive Bayes", "Learning Fair Representations", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Support Vector Machines", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.EQUALIZED_ODDS"],
      labels: ["Support Vector Machines", "Sem método", "Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS"],
      labels: ["Support Vector Machines", "Sem método", "Calibrated Equalized Odds"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION"],
      labels: ["Support Vector Machines", "Sem método", "Reject Option Classification"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.REWEIGHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Support Vector Machines", "Reweighing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Support Vector Machines", "Disparate Impact Remover", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Support Vector Machines", "Optimized Preprocessing", "Sem método"],
      selected: true
    },
    {   
      options: ["Algorithms.SUPPORT_VECTOR_MACHINES", "UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Support Vector Machines", "Learning Fair Representations", "Sem método"],
      selected: true
    },
    {   
      options: ["UnbiasInProcAlgorithms.PREJUDICE_REMOVER", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Prejudice Remover", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Adversarial Debiasing", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Exponentiated Gradient Reduction", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Rich Subgroup Fairness", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Meta Fair Classifier", "Sem método", "Sem método"],
      selected: true
    },
    {   
      options: ["UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION", "UnbiasDataAlgorithms.NOTHING", "UnbiasPostProcAlgorithms.NOTHING"],
      labels: ["Grid Search Reduction", "Sem método", "Sem método"],
      selected: true
    }
  ];

  const handleChange = (event) => {
    if(event.target.name === 'ml_algorithm_validation' && event.target.checked) {
      store.dispatch(setValidAlgorithms(validAlgorithms));
    }

    setPlanningState({
      ...planningState,
      [event.target.name]: event.target.checked,
    });
  };

  const handleSelectList = (index) => {
    store.dispatch(invertValidAlgorithmsSelected(index))
    console.log(validAlgorithmsSelected);
  }

  const handleThresholdChange = (event, newValue) => {
    setThresholdValue(newValue);
  };

  const handleCloseSuccessToast = () => {
    setValidPlanningVisible(false);
  }

  const savePlanningOptions = (event) => {
    function savePlanning() {
      console.log(planningState);

      axios.put('http://localhost:8080/config/planner', planningState)
            .then((response) =>{
              if (debugAPI) {
                console.log(response.data);
              }
            });

      if (planningState.ml_algorithm_validation) {
        let validAlgorithmsToSave = {
          valid_algorithms: validAlgorithmsSelected.filter(algorithms => algorithms.selected)
                                                   .map(algorithms => algorithms.options)
        }

        console.log(validAlgorithmsToSave);

        axios.put('http://localhost:8080/config/valid_algorithms', validAlgorithmsToSave)
              .then((response) =>{
                if (debugAPI) {
                  console.log(response.data);
                }
              });
      }

      if (planningState.ml_pipeline_threshold) {
        let scoreThreshold = {
          min_score: thresholdValue[0],
          max_score: thresholdValue[1]
        }

        console.log(scoreThreshold);
        axios.put('http://localhost:8080/config/score', scoreThreshold)
              .then((response) =>{
                if (debugAPI) {
                  console.log(response.data);
                }
              });
      }
    }

    event.preventDefault();

    savePlanning();
    setValidPlanningVisible(true);
  }

  //ComponentDidMount
  React.useEffect(() => {
    axios.get('http://localhost:8080/config/valid_algorithms')
         .then((response) =>{
            if (debugAPI) {
              console.log(response.data);
            }

            validAlgorithms = validAlgorithms.map((validAlgorithm) => {
              return {
                ...validAlgorithm, 
                selected: response.data.valid_algorithms
                                      .some((valid_algorithm) => validAlgorithm.options[0] === valid_algorithm[0] && 
                                                                 validAlgorithm.options[1] === valid_algorithm[1] && 
                                                                 validAlgorithm.options[2] === valid_algorithm[2])
              };
            });
            
            store.dispatch(setValidAlgorithms(validAlgorithms));
         });

    axios.get('http://localhost:8080/config/score')
         .then((response) =>{
            if (debugAPI) {
              console.log(response.data);
            }

            setThresholdValue([response.data.min_score, response.data.max_score]);
         });

    axios.get('http://localhost:8080/config/planner')
         .then((response) =>{
            if (debugAPI) {
              console.log(response.data);
            }
            setPlanningState(response.data);
         });
  }, []);

  return (
    <form onSubmit={savePlanningOptions}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block', marginBottom: '0'}}>Planejamento</h2>
          <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<SaveIcon />}>Salvar</Button>
        </span>

        <FormControl sx={{ m: 3 }} component="fieldset" variant="standard">
          <FormLabel component="legend">Selecionar estratégias de planejamento</FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox checked={planningState.ml_pipeline} onChange={handleChange} name="ml_pipeline" disabled />
              }
              label="Escolher o modelo com a melhor pontuação"
            />
            <FormControlLabel
              control={
                <Checkbox checked={planningState.ml_data_checksum} onChange={handleChange} name="ml_data_checksum" />
              }
              label="Escolher o modelo de acordo com os dados mais recentes encontrados em execuções prévias"
            />
            <FormControlLabel
              control={
                <Checkbox checked={planningState.ml_algorithm_validation} onChange={handleChange} name="ml_algorithm_validation" />
              }
              label="Restringir conjunto de algoritmos escolhidos"
            />
            {planningState.ml_algorithm_validation ?
            <Box sx={{ height: 285, maxWidth: 400, marginLeft: '35px', overflow: 'auto' }}>
              <List sx={{ width: 380, bgcolor: 'background.paper' }}>
              {validAlgorithmsSelected.map((value, index) => {
                const labelId = `checkbox-list-label-${index}`;
        
                return (
                  <ListItem
                    key={index}
                    disablePadding
                  >
                    <ListItemButton role={undefined}
                      sx={{backgroundColor: value.selected ? '#00DDFF' : 'background.paper'}}
                      onClick={(event) => handleSelectList(index)} dense>
                      <ListItemText id={labelId} primary={<div>
                        <div><StorageOutlinedIcon fontSize="small" /> {value.labels[1]}</div>
                        <div><ModelTrainingIcon fontSize="small" /> {value.labels[0]} {value.selected ? <CheckIcon sx={{float:'right'}} /> : ''}</div>
                        <div><InsightsIcon fontSize="small" /> {value.labels[2]}</div>
                      </div>} />
                    </ListItemButton>
                  </ListItem>
                );
              })}
              </List>
            </Box> : ''}
            <FormControlLabel
              control={
                <Checkbox checked={planningState.ml_pipeline_threshold} onChange={handleChange} name="ml_pipeline_threshold" />
              }
              label="Restringir limiar de pontuação"
            />
            {planningState.ml_pipeline_threshold ?
            <Box sx={{ display: 'flex', width: 400, marginLeft: '35px' }}>
              <span style={{whiteSpace: 'nowrap'}}>{thresholdValue[0]} </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} getAriaLabel={() => 'Threshold'} value={thresholdValue} max={1000} onChange={handleThresholdChange} /><span> {thresholdValue[1]}</span>
            </Box> : ''}
          </FormGroup>
          <FormHelperText>OBS: Selecionar ou não selecionar determinadas estratégias podem causar impactos caso certas etapas de análise não forem selecionadas</FormHelperText>
        </FormControl>

        <Snackbar open={validPlanningVisible} autoHideDuration={6000} onClose={handleCloseSuccessToast}>
          <Alert onClose={handleCloseSuccessToast} severity="success">
            <AlertTitle><strong>Sucesso!</strong></AlertTitle>
            Configurações salvas com sucesso!
          </Alert>
        </Snackbar>
      </Box>
    </form>
  );
}

export default PlanningMenu;