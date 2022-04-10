import * as React from 'react';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Snackbar from '@mui/material/Snackbar';
import Button from '@mui/material/Button';
import PlayArrowRoundedIcon from '@mui/icons-material/PlayArrowRounded';

import FormControl from '@mui/material/FormControl';

import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import Select from '@mui/material/Select';
import axios from 'axios';

function AutoPipelineMenu(props) {
  const [validPlanningVisible, setValidPlanningVisible] = React.useState(false);
  const [dataset, setDataset] = React.useState('Datasets.GERMAN_CREDIT');

  const handleDatasetChange = (event) => {
    setDataset(event.target.value);
  }

  const handleCloseSuccessToast = () => {
    setValidPlanningVisible(false);
  }

  const executeAutoPipeline = (event) => {
    event.preventDefault();

    let data = {
      dataset: dataset
    }

    axios.post('http://localhost:8080/pipeline/auto', data)
         .then((response) =>{
            console.log(response.data);
         });

    setValidPlanningVisible(true);
  }

  return (
    <form onSubmit={executeAutoPipeline}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block'}}>Pipeline Autônomo</h2>
          <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<PlayArrowRoundedIcon />}>Executar</Button>
        </span>
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
              </Select>
              <FormHelperText>Conjunto de dados a ser treinado</FormHelperText>
            </FormControl>
          </Box>
        </Box>

        <div style={{marginTop: '35px'}}>Clique em <strong>EXECUTAR</strong> para iniciar a execução</div>
        <div>Pipeline será executado de acordo com as configurações salvas nos menus de configuração</div>
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