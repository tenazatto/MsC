import { configureStore } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit'

const fairnessMetricsSelectedRedux = createSlice({
  name: 'fairnessMetricsSelected',
  initialState: {
    value: [],
  },
  reducers: {
    fairnessMetricsSelectedPush: (state, action) => {
      state.value.push(action.payload);
    },
    fairnessMetricsSelectedClear: (state) => {
      state.value = [];
    }
  },
})
export const selectFairnessMetricsSelected = (state) => state.fairnessMetricsSelected.value
export const { fairnessMetricsSelectedPush, fairnessMetricsSelectedClear } = fairnessMetricsSelectedRedux.actions

const performanceMetricsSelectedRedux = createSlice({
  name: 'performanceMetricsSelected',
  initialState: {
    value: [],
  },
  reducers: {
    performanceMetricsSelectedPush: (state, action) => {
      state.value.push(action.payload);
    },
    performanceMetricsSelectedClear: (state) => {
      state.value = [];
    }
  },
})
export const selectPerformanceMetricsSelected = (state) => state.performanceMetricsSelected.value
export const { performanceMetricsSelectedPush, performanceMetricsSelectedClear } = performanceMetricsSelectedRedux.actions

const validAlgorithmsRedux = createSlice({
  name: 'validAlgorithms',
  initialState: {
    value: [],
  },
  reducers: {
    validAlgorithmsPush: (state, action) => {
      state.value.push(action.payload);
    },
    validAlgorithmsClear: (state) => {
      state.value = [];
    },
    setValidAlgorithms: (state, action) => {
      state.value = action.payload;
    },
    invertValidAlgorithmsSelected: (state, action) => {
      state.value[action.payload].selected = !state.value[action.payload].selected;
    },
  },
})
export const selectValidAlgorithms = (state) => state.validAlgorithms.value
export const { validAlgorithmsPush, validAlgorithmsClear, setValidAlgorithms, invertValidAlgorithmsSelected } = validAlgorithmsRedux.actions

const pipelineResultsRedux = createSlice({
  name: 'pipelineResults',
  initialState: {
    value: {
      data_checksum:'',
      dataset:'',
      date_end:'',
      date_start:'',
      execution_time_ms:0,
      fairness_metrics:{
        average_abs_odds_difference:{explanation:'',name:'',value:0},
        disparate_impact:{explanation:'',name:'',value:0},
        equal_opportunity_difference:{explanation:'',name:'',value:0},
        statistical_parity_difference:{explanation:'',name:'',value:0},
        theil_index:{explanation:'',name:'',value:0}
      },
      inproc_algorithm:'',
      performance_metrics:{
        accuracy:{explanation:'',name:'',value:0},
        auc:{explanation:'',name:'',value:0},
        f1_score:{explanation:'',name:'',value:0},
        precision:{explanation:'',name:'',value:0},
        recall:{explanation:'',name:'',value:0}
      },
      preprocessor:'',
      scores:{fairness_score:0,group_score:0,performance_score:0},
      unbias_data_algorithm:'',
      unbias_postproc_algorithm:''
    },
  },
  reducers: {
    setPipelineResults: (state, action) => {
      state.value = action.payload;
    },
  },
})

export const selectPipelineResults = (state) => state.pipelineResults.value
export const { setPipelineResults } = pipelineResultsRedux.actions

const pipelineResultsAutoRedux = createSlice({
  name: 'pipelineResultsAuto',
  initialState: {
    value: {
      pipelines: []
    },
  },
  reducers: {
    setPipelineResultsAuto: (state, action) => {
      state.value = action.payload;
    },
  },
})

export const selectPipelineResultsAuto = (state) => state.pipelineResultsAuto.value
export const { setPipelineResultsAuto } = pipelineResultsAutoRedux.actions

export default configureStore({
  reducer: {
    fairnessMetricsSelected: fairnessMetricsSelectedRedux.reducer,
    performanceMetricsSelected: performanceMetricsSelectedRedux.reducer,
    validAlgorithms: validAlgorithmsRedux.reducer,
    pipelineResults: pipelineResultsRedux.reducer,
    pipelineResultsAuto: pipelineResultsAutoRedux.reducer,
  },
});
