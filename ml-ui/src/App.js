import logo from './logo.svg';
import './App.css';
import { StyledEngineProvider } from '@mui/material/styles';
import { Provider } from 'react-redux';

import store from './store';
import Screen from './Screen';

function App() {
  return (
    <Provider store={store}>
      <StyledEngineProvider injectFirst>
        <Screen />
      </StyledEngineProvider>
    </Provider>
  );
}

export default App;
