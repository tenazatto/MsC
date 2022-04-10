import * as React from 'react';
import { useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import Slider from '@mui/material/Slider';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Snackbar from '@mui/material/Snackbar';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import SaveIcon from '@mui/icons-material/Save';

import MultiselectComboBox from './multiselect';
import {
  selectFairnessMetricsSelected,
  fairnessMetricsSelectedPush, 
  fairnessMetricsSelectedClear,
  selectPerformanceMetricsSelected,
  performanceMetricsSelectedPush, 
  performanceMetricsSelectedClear
} from './store';
import store from './store';
import axios from 'axios';

function MetricsMenu(props) {
  const [valuePerformance, setValuePerformance] = React.useState(50);
  const [valueFairness, setValueFairness] = React.useState(50);
  const [valueGroupTab, setValueGroupTab] = React.useState('1');

  const [errorMessage, setErrorMessage] = React.useState('');

  const [spdFairnessMetricVisible, setSpdFairnessMetricVisible] = React.useState(false);
  const [eodFairnessMetricVisible, setEodFairnessMetricVisible] = React.useState(false);
  const [aodFairnessMetricVisible, setAodFairnessMetricVisible] = React.useState(false);
  const [diFairnessMetricVisible, setDiFairnessMetricVisible] = React.useState(false);
  const [tiFairnessMetricVisible, setTiFairnessMetricVisible] = React.useState(false);

  const [spdFairnessMetricValue, setSpdFairnessMetricValue] = React.useState(0);
  const [eodFairnessMetricValue, setEodFairnessMetricValue] = React.useState(0);
  const [aodFairnessMetricValue, setAodFairnessMetricValue] = React.useState(0);
  const [diFairnessMetricValue, setDiFairnessMetricValue] = React.useState(0);
  const [tiFairnessMetricValue, setTiFairnessMetricValue] = React.useState(0);

  const [accPerformanceMetricVisible, setAccPerformanceMetricVisible] = React.useState(false);
  const [prcPerformanceMetricVisible, setPrcPerformanceMetricVisible] = React.useState(false);
  const [rclPerformanceMetricVisible, setRclPerformanceMetricVisible] = React.useState(false);
  const [fscPerformanceMetricVisible, setFscPerformanceMetricVisible] = React.useState(false);
  const [aucPerformanceMetricVisible, setAucPerformanceMetricVisible] = React.useState(false);

  const [accPerformanceMetricValue, setAccPerformanceMetricValue] = React.useState(0);
  const [prcPerformanceMetricValue, setPrcPerformanceMetricValue] = React.useState(0);
  const [rclPerformanceMetricValue, setRclPerformanceMetricValue] = React.useState(0);
  const [fscPerformanceMetricValue, setFscPerformanceMetricValue] = React.useState(0);
  const [aucPerformanceMetricValue, setAucPerformanceMetricValue] = React.useState(0);

  const [invalidMetricVisible, setInvalidMetricVisible] = React.useState(false);
  const [validMetricVisible, setValidMetricVisible] = React.useState(false);

  const debugConsole = false;
  const debugAPI = true;

  const performanceMetrics = [
    {key: 'accuracy', value:'Accuracy'},
    {key: 'precision', value:'Precision'},
    {key: 'recall', value:'Recall'},
    {key: 'f1_score', value:'F1-Score'},
    {key: 'auc', value:'AUC Score'}
  ];
  let performanceMetricsSelected = useSelector(selectPerformanceMetricsSelected);
  const performanceMetricsDefault = [performanceMetrics[0].key];

  const fairnessMetrics = [
    {key: 'statistical_parity_difference', value:'Statistical Parity Difference'},
    {key: 'equal_opportunity_difference', value:'Equal Opportunity Difference'},
    {key: 'average_abs_odds_difference', value:'Average Odds Difference'},
    {key: 'disparate_impact', value:'Disparate Impact'},
    {key: 'theil_index', value:'Theil Index'}
  ];
  let fairnessMetricsSelected = useSelector(selectFairnessMetricsSelected);
  let fairnessMetricsDefault = [fairnessMetrics[0].key];

  const handleChangeGroupTab = (event, newValue) => {
    setValueGroupTab(newValue);
    fairnessMetricsDefault = fairnessMetricsSelected.map((metric) => metric.key);
  };

  const handleChangeGroupSlider = (name, newValue) => {
    if (name === 'FairnessWeight') {
      setValuePerformance(100-newValue);
      setValueFairness(newValue);
    } else {
      setValuePerformance(newValue);
      setValueFairness(100-newValue);
    }
  };

  const handleChangeSlider = (name, newValue) => {
    if (name === 'statistical_parity_difference') {
      setSpdFairnessMetricValue(newValue);
    } else if (name === 'equal_opportunity_difference') {
      setEodFairnessMetricValue(newValue);
    } else if (name === 'average_abs_odds_difference') {
      setAodFairnessMetricValue(newValue);
    } else if (name === 'disparate_impact') {
      setDiFairnessMetricValue(newValue);
    } else if (name === 'theil_index') {
      setTiFairnessMetricValue(newValue);
    } else if (name === 'accuracy') {
      setAccPerformanceMetricValue(newValue);
    } else if (name === 'precision') {
      setPrcPerformanceMetricValue(newValue);
    } else if (name === 'recall') {
      setRclPerformanceMetricValue(newValue);
    } else if (name === 'f1_score') {
      setFscPerformanceMetricValue(newValue);
    } else if (name === 'auc') {
      setAucPerformanceMetricValue(newValue);
    } 
  }

  const handleChangePerformanceMetricsComboBox = (selectedKeys) => {
    function updateSelected() {
      store.dispatch(performanceMetricsSelectedClear());
      selectedKeys.forEach((key) => {
        store.dispatch(performanceMetricsSelectedPush(
          performanceMetrics.filter((metric) => metric.key === key)[0]
        ));
      });
    }

    function logSelected() {
      if (debugConsole) {
        console.log('Performance - Chaves');
        console.log(selectedKeys);
        console.log('Performance - Métricas');
        console.log(performanceMetricsSelected);
      }
    }

    function reinitializeStates() {
      setAccPerformanceMetricVisible(false);
      setPrcPerformanceMetricVisible(false);
      setRclPerformanceMetricVisible(false);
      setFscPerformanceMetricVisible(false);
      setAucPerformanceMetricVisible(false);

      setAccPerformanceMetricValue(0);
      setPrcPerformanceMetricValue(0);
      setRclPerformanceMetricValue(0);
      setFscPerformanceMetricValue(0);
      setAucPerformanceMetricValue(0);
    }

    function setNewMetricValues() {
      let metricInitialWeight = Math.floor(100 / selectedKeys.length);

      if (selectedKeys.includes(performanceMetrics[0].key)) {
        setAccPerformanceMetricVisible(true);
        setAccPerformanceMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(performanceMetrics[1].key)) {
        setPrcPerformanceMetricVisible(true);
        setPrcPerformanceMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(performanceMetrics[2].key)) {
        setRclPerformanceMetricVisible(true);
        setRclPerformanceMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(performanceMetrics[3].key)) {
        setFscPerformanceMetricVisible(true);
        setFscPerformanceMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(performanceMetrics[4].key)) {
        setAucPerformanceMetricVisible(true);
        setAucPerformanceMetricValue(metricInitialWeight);
      }
    }

    function logNewStateValues() {
      if (debugConsole) {
        console.log('Performance - Visíveis');
        console.log([accPerformanceMetricVisible, prcPerformanceMetricVisible, rclPerformanceMetricVisible, fscPerformanceMetricVisible, aucPerformanceMetricVisible]);
        console.log('Performance - Valores');
        console.log([accPerformanceMetricValue, prcPerformanceMetricValue, rclPerformanceMetricValue, fscPerformanceMetricValue, aucPerformanceMetricValue]);
      }
    }

    updateSelected();

    logSelected();

    reinitializeStates();

    setNewMetricValues();

    logNewStateValues();
  }

  const handleChangeFairnessMetricsComboBox = (selectedKeys) => {
    function updateSelected() {
      store.dispatch(fairnessMetricsSelectedClear());
      selectedKeys.forEach((key) => {
        store.dispatch(fairnessMetricsSelectedPush(
          fairnessMetrics.filter((metric) => metric.key === key)[0]
        ));
      });
    }

    function logSelected() {
      if (debugConsole) {
        console.log('Fairness - Chaves');
        console.log(selectedKeys);
        console.log('Fairness - Métricas');
        console.log(fairnessMetricsSelected);
      }
    }

    function reinitializeStates() {
      setSpdFairnessMetricVisible(false);
      setEodFairnessMetricVisible(false);
      setAodFairnessMetricVisible(false);
      setDiFairnessMetricVisible(false);
      setTiFairnessMetricVisible(false);

      setSpdFairnessMetricValue(0);
      setEodFairnessMetricValue(0);
      setAodFairnessMetricValue(0);
      setDiFairnessMetricValue(0);
      setTiFairnessMetricValue(0);
    }

    function setNewMetricValues() {
      let metricInitialWeight = Math.floor(100 / selectedKeys.length);

      if (selectedKeys.includes(fairnessMetrics[0].key)) {
        setSpdFairnessMetricVisible(true);
        setSpdFairnessMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(fairnessMetrics[1].key)) {
        setEodFairnessMetricVisible(true);
        setEodFairnessMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(fairnessMetrics[2].key)) {
        setAodFairnessMetricVisible(true);
        setAodFairnessMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(fairnessMetrics[3].key)) {
        setDiFairnessMetricVisible(true);
        setDiFairnessMetricValue(metricInitialWeight);
      }
      if (selectedKeys.includes(fairnessMetrics[4].key)) {
        setTiFairnessMetricVisible(true);
        setTiFairnessMetricValue(metricInitialWeight);
      }
    }

    function logNewStateValues() {
      if (debugConsole) {
        console.log('Fairness - Visíveis');
        console.log([spdFairnessMetricVisible, eodFairnessMetricVisible, aodFairnessMetricVisible, diFairnessMetricVisible, tiFairnessMetricVisible]);
        console.log('Fairness - Valores');
        console.log([spdFairnessMetricValue, eodFairnessMetricValue, aodFairnessMetricValue, diFairnessMetricValue, tiFairnessMetricValue]);
      }
    }

    updateSelected();

    logSelected();

    reinitializeStates();

    setNewMetricValues();

    logNewStateValues();
  }

  const handleCloseErrorToast = () => {
    setInvalidMetricVisible(false);
  }

  const handleCloseSuccessToast = () => {
    setValidMetricVisible(false);
  }

  const saveMetricWeights = (event) => {
    function isValidToSave() {
      let valid = {};

      let performanceMetricSum = [
        accPerformanceMetricValue, 
        prcPerformanceMetricValue, 
        rclPerformanceMetricValue, 
        fscPerformanceMetricValue, 
        aucPerformanceMetricValue
      ].reduce((acc, val) => acc + val);
      console.log(performanceMetricSum);

      let fairnessMetricSum = [
        spdFairnessMetricValue, 
        eodFairnessMetricValue, 
        aodFairnessMetricValue, 
        diFairnessMetricValue, 
        tiFairnessMetricValue
      ].reduce((acc, val) => acc + val);
      console.log(fairnessMetricSum);

      if ((fairnessMetricSum < 100 && performanceMetricSum < 100) || (fairnessMetricSum > 100 && performanceMetricSum > 100)) {
        valid = {
          isValid: false, 
          errorMessage: 'A soma dos pesos para as métricas de Fairness e de Performance estão '
                        + ((fairnessMetricSum < 100 && performanceMetricSum < 100) ? 'menores' : 'maiores') + ' do que 100%'
        };
      } else if ((fairnessMetricSum < 100 && performanceMetricSum > 100) || (fairnessMetricSum > 100 && performanceMetricSum < 100)) {
        valid = {
          isValid: false, 
          errorMessage: ['A soma dos pesos para as métricas de Fairness está ' 
                        + ((fairnessMetricSum < 100) ? 'menor' : 'maior') + ' do que 100%',
                        <br/>,
                        'A soma dos pesos para as métricas de Performance está '
                        + ((performanceMetricSum < 100) ? 'menor' : 'maior') + ' do que 100%']

        };
      } else if (fairnessMetricSum !== 100) {
        valid = {
          isValid: false,
          errorMessage: 'A soma dos pesos para as métricas de Fairness está ' 
                        + ((fairnessMetricSum < 100) ? 'menor' : 'maior') + ' do que 100%'
        };
      } else if (performanceMetricSum !== 100) {
        valid = {
          isValid: false,
          errorMessage: 'A soma dos pesos para as métricas de Performance está '
                        + ((performanceMetricSum < 100) ? 'menor' : 'maior') + ' do que 100%'
        };
      } else {
        valid = {
          isValid: true,
          errorMessage: undefined
        };
      }

      return valid;
    }

    function saveMetrics() {
      function setPerformanceMetrics(selected_keys, performance_metrics) {
        if (selected_keys.includes(performanceMetrics[0].key)) {
          performance_metrics.metrics[performanceMetrics[0].key] = {
            weight: accPerformanceMetricValue / 100,
            normalize: null
          };
        }
        if (selected_keys.includes(performanceMetrics[1].key)) {
          performance_metrics.metrics[performanceMetrics[1].key] = {
            weight: prcPerformanceMetricValue / 100,
            normalize: null
          };
        }
        if (selected_keys.includes(performanceMetrics[2].key)) {
          performance_metrics.metrics[performanceMetrics[2].key] = {
            weight: rclPerformanceMetricValue / 100,
            normalize: null
          };
        }
        if (selected_keys.includes(performanceMetrics[3].key)) {
          performance_metrics.metrics[performanceMetrics[3].key] = {
            weight: fscPerformanceMetricValue / 100,
            normalize: null
          };
        }
        if (selected_keys.includes(performanceMetrics[4].key)) {
          performance_metrics.metrics[performanceMetrics[4].key] = {
            weight: aucPerformanceMetricValue / 100,
            normalize: null
          };
        }
      }

      function setFairnessMetrics(selected_keys, fairness_metrics) {
        if (selected_keys.includes(fairnessMetrics[0].key)) {
          fairness_metrics.metrics[fairnessMetrics[0].key] = {
            weight: spdFairnessMetricValue / 100,
            normalize: 'diff'
          };
        }
        if (selected_keys.includes(fairnessMetrics[1].key)) {
          fairness_metrics.metrics[fairnessMetrics[1].key] = {
            weight: eodFairnessMetricValue / 100,
            normalize: 'diff'
          };
        }
        if (selected_keys.includes(fairnessMetrics[2].key)) {
          fairness_metrics.metrics[fairnessMetrics[2].key] = {
            weight: aodFairnessMetricValue / 100,
            normalize: 'diff'
          };
        }
        if (selected_keys.includes(fairnessMetrics[3].key)) {
          fairness_metrics.metrics[fairnessMetrics[3].key] = {
            weight: diFairnessMetricValue / 100,
            normalize: 'ratio'
          };
        }
        if (selected_keys.includes(fairnessMetrics[4].key)) {
          fairness_metrics.metrics[fairnessMetrics[4].key] = {
            weight: tiFairnessMetricValue / 100,
            normalize: 'diff'
          };
        }
      }

      let selected_fairness_keys = fairnessMetricsSelected.map((metric) => metric.key);
      let selected_performance_keys = performanceMetricsSelected.map((metric) => metric.key);

      let performance_metrics = {
        group_name: "standard",
        weight: valuePerformance / 100,
        metrics: {}
      };

      let fairness_metrics = {
        group_name: "fairness",
        weight: valueFairness / 100,
        metrics: {}
      };

      setFairnessMetrics(selected_fairness_keys, fairness_metrics);
      setPerformanceMetrics(selected_performance_keys, performance_metrics);

      let metrics = {
        metrics_groups : [
          performance_metrics,
          fairness_metrics
        ]
      };

      axios.put('http://localhost:8080/config/metrics', metrics)
           .then((response) =>{
              if (debugAPI) {
                console.log(response.data);
              }
            });

      console.log(metrics);
    }

    event.preventDefault();

    let validation = isValidToSave();

    if (!validation.isValid) {
      setErrorMessage(validation.errorMessage);
      console.log(errorMessage);
      setInvalidMetricVisible(true);
    } else {
      saveMetrics();
      setValidMetricVisible(true);
    }
  }

  //ComponentDidMount
  React.useEffect(() => {
    function updateSelectedOnMount(metrics) {
      function updatePerformanceMetricsOnMount(saved_performance_metrics, metric) {
        if (metric.key === performanceMetrics[0].key) {
          setAccPerformanceMetricVisible(true);
          setAccPerformanceMetricValue(saved_performance_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === performanceMetrics[1].key) {
          setPrcPerformanceMetricVisible(true);
          setPrcPerformanceMetricValue(saved_performance_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === performanceMetrics[2].key) {
          setRclPerformanceMetricVisible(true);
          setRclPerformanceMetricValue(saved_performance_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === performanceMetrics[3].key) {
          setFscPerformanceMetricVisible(true);
          setFscPerformanceMetricValue(saved_performance_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === performanceMetrics[4].key) {
          setAucPerformanceMetricVisible(true);
          setAucPerformanceMetricValue(saved_performance_metrics.metrics[metric.key].weight * 100);
        }
      }

      function updateFairnessMetricsOnMount(saved_fairness_metrics, metric) {
        if (metric.key === fairnessMetrics[0].key) {
          setSpdFairnessMetricVisible(true);
          setSpdFairnessMetricValue(saved_fairness_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === fairnessMetrics[1].key) {
          setEodFairnessMetricVisible(true);
          setEodFairnessMetricValue(saved_fairness_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === fairnessMetrics[2].key) {
          setAodFairnessMetricVisible(true);
          setAodFairnessMetricValue(saved_fairness_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === fairnessMetrics[3].key) {
          setDiFairnessMetricVisible(true);
          setDiFairnessMetricValue(saved_fairness_metrics.metrics[metric.key].weight * 100);
        }
        if (metric.key === fairnessMetrics[4].key) {
          setTiFairnessMetricVisible(true);
          setTiFairnessMetricValue(saved_fairness_metrics.metrics[metric.key].weight * 100);
        }
      }

      let saved_performance_metrics = metrics.metrics_groups[0];
      let saved_fairness_metrics = metrics.metrics_groups[1];

      let selected_performance_metrics = performanceMetrics.filter((metric) => Object.keys(saved_performance_metrics.metrics).includes(metric.key));
      let selected_fairness_metrics = fairnessMetrics.filter((metric) => Object.keys(saved_fairness_metrics.metrics).includes(metric.key));

      setValuePerformance(saved_performance_metrics.weight * 100);
      setValueFairness(saved_fairness_metrics.weight * 100);

      selected_performance_metrics.forEach((metric) => {
        store.dispatch(performanceMetricsSelectedPush(metric));

        updatePerformanceMetricsOnMount(saved_performance_metrics, metric);
      });
      selected_fairness_metrics.forEach((metric) => {
        store.dispatch(fairnessMetricsSelectedPush(metric));

        updateFairnessMetricsOnMount(saved_fairness_metrics, metric);
      });
    }

    axios.get('http://localhost:8080/config/metrics')
         .then((response) =>{
            if (debugAPI) {
              console.log(response.data);
            }

            updateSelectedOnMount(response.data);
         });

    //store.dispatch(fairnessMetricsSelectedPush(fairnessMetrics[0]));
    //store.dispatch(performanceMetricsSelectedPush(performanceMetrics[0]));
  }, []);

  return (
    <form onSubmit={saveMetricWeights}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block'}}>Métricas</h2>
          <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<SaveIcon />}>Salvar</Button>
        </span>

        <TabContext value={valueGroupTab}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <TabList onChange={handleChangeGroupTab}>
              <Tab label="Métricas de Avaliação" value="1" />
              <Tab label="Métricas de Fairness" value="2" />
            </TabList>
          </Box>
          <TabPanel value="1">
            <div>
              <h3>Métricas de Avaliação</h3>

              <Box sx={{ display: 'flex', width: 400 }}>
                <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={valuePerformance} onChange={(event, value) => handleChangeGroupSlider('PerformanceWeight', value)} /><span> {valuePerformance + '%'}</span>
              </Box>
              <Box sx={{ display: 'flex', width: 400 }}>
                <span style={{whiteSpace: 'nowrap'}}>Métricas p/ uso: </span>
                <MultiselectComboBox options={performanceMetrics} 
                                     selectedDefault={performanceMetricsDefault}
                                     onChange={handleChangePerformanceMetricsComboBox} />
              </Box>
              <Box sx={{ flexGrow: 1, bgcolor: 'background.paper', display: 'flex', height: 240 }}>
                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                  {accPerformanceMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{performanceMetrics[0].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={accPerformanceMetricValue} onChange={(event, value) => handleChangeSlider(performanceMetrics[0].key, value)} /><span> {accPerformanceMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {prcPerformanceMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{performanceMetrics[1].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={prcPerformanceMetricValue} onChange={(event, value) => handleChangeSlider(performanceMetrics[1].key, value)} /><span> {prcPerformanceMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {rclPerformanceMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{performanceMetrics[2].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={rclPerformanceMetricValue} onChange={(event, value) => handleChangeSlider(performanceMetrics[2].key, value)} /><span> {rclPerformanceMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {fscPerformanceMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{performanceMetrics[3].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={fscPerformanceMetricValue} onChange={(event, value) => handleChangeSlider(performanceMetrics[3].key, value)} /><span> {fscPerformanceMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {aucPerformanceMetricVisible ? 
                  <Grid item xs={6} visibility={tiFairnessMetricVisible}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{performanceMetrics[4].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={aucPerformanceMetricValue} onChange={(event, value) => handleChangeSlider(performanceMetrics[4].key, value)} /><span> {aucPerformanceMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                </Grid>
              </Box>
            </div>
          </TabPanel>
          <TabPanel value="2">
            <div>
              <h3>Métricas de Fairness</h3>

              <Box sx={{ display: 'flex', width: 400 }}>
                <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Fairness" value={valueFairness} onChange={(event, value) => handleChangeGroupSlider('FairnessWeight', value)} /><span> {valueFairness + '%'}</span>
              </Box>
              <Box sx={{ display: 'flex', width: 400 }}>
                <span style={{whiteSpace: 'nowrap'}}>Métricas p/ uso: </span>
                <MultiselectComboBox options={fairnessMetrics}
                                    selectedDefault={fairnessMetricsDefault} 
                                    onChange={handleChangeFairnessMetricsComboBox} />
              </Box>
              <Box sx={{ flexGrow: 1, bgcolor: 'background.paper', display: 'flex', height: 240 }}>
                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                  {spdFairnessMetricVisible ? 
                  <Grid item xs={6}>
                    <span><h4 style={{display: 'inline-block', marginRight: '5px'}}>{fairnessMetrics[0].value}</h4><InfoOutlinedIcon /></span>
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={spdFairnessMetricValue} onChange={(event, value) => handleChangeSlider(fairnessMetrics[0].key, value)} /><span> {spdFairnessMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {eodFairnessMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{fairnessMetrics[1].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={eodFairnessMetricValue} onChange={(event, value) => handleChangeSlider(fairnessMetrics[1].key, value)} /><span> {eodFairnessMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {aodFairnessMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{fairnessMetrics[2].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={aodFairnessMetricValue} onChange={(event, value) => handleChangeSlider(fairnessMetrics[2].key, value)} /><span> {aodFairnessMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {diFairnessMetricVisible ? 
                  <Grid item xs={6}>
                    <h4 style={{display: 'inline-block', marginRight: '5px'}}>{fairnessMetrics[3].value}</h4><InfoOutlinedIcon />
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={diFairnessMetricValue} onChange={(event, value) => handleChangeSlider(fairnessMetrics[3].key, value)} /><span> {diFairnessMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                  {tiFairnessMetricVisible ? 
                  <Grid item xs={6} visibility={tiFairnessMetricVisible}>
                    <span><h4 style={{display: 'inline-block', marginRight: '5px'}}>{fairnessMetrics[4].value}</h4><InfoOutlinedIcon /></span>
                    <Box sx={{ display: 'flex', width: 400 }}>
                      <span style={{whiteSpace: 'nowrap'}}>Peso p/ Avaliação: </span><Slider sx={{ marginRight: '20px', marginLeft: '20px'}} aria-label="Performance" value={tiFairnessMetricValue} onChange={(event, value) => handleChangeSlider(fairnessMetrics[4].key, value)} /><span> {tiFairnessMetricValue + '%'}</span>
                    </Box>
                  </Grid> : ''}
                </Grid>
              </Box>
            </div>
          </TabPanel>
        </TabContext>
        <Snackbar open={invalidMetricVisible} autoHideDuration={6000} onClose={handleCloseErrorToast}>
          <Alert onClose={handleCloseErrorToast} severity="error">
            <AlertTitle><strong>Erro de validação</strong></AlertTitle>
            {errorMessage}
          </Alert>
        </Snackbar>
        <Snackbar open={validMetricVisible} autoHideDuration={6000} onClose={handleCloseSuccessToast}>
          <Alert onClose={handleCloseSuccessToast} severity="success">
            <AlertTitle><strong>Sucesso!</strong></AlertTitle>
            Configurações salvas com sucesso!
          </Alert>
        </Snackbar>
      </Box>
    </form>
  );
}

export default MetricsMenu;