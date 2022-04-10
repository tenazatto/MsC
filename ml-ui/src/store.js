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

export default configureStore({
  reducer: {
    fairnessMetricsSelected: fairnessMetricsSelectedRedux.reducer,
    performanceMetricsSelected: performanceMetricsSelectedRedux.reducer,
    validAlgorithms: validAlgorithmsRedux.reducer,
  },
});
