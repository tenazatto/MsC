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
import axios from 'axios';

function AnalysisMenu(props) {
  const [validAnalysisVisible, setValidAnalysisVisible] = React.useState(false);
  
  const [analysisState, setAnalysisState] = React.useState({
    ml_pipeline: true,
    ml_execution: true,
  });

  const debugAPI = true;

  const handleChange = (event) => {
    setAnalysisState({
      ...analysisState,
      [event.target.name]: event.target.checked,
    });
  };

  const handleCloseSuccessToast = () => {
    setValidAnalysisVisible(false);
  }

  const saveAnalysisOptions = (event) => {
    function saveAnalysis() {
      axios.put('http://localhost:8080/config/analyzer', analysisState)
           .then((response) =>{
              if (debugAPI) {
                console.log(response.data);
              }
            });

      console.log(analysisState);
    }

    event.preventDefault();

    saveAnalysis();
    setValidAnalysisVisible(true);
  }

  //ComponentDidMount
  React.useEffect(() => {
    axios.get('http://localhost:8080/config/analyzer')
         .then((response) =>{
            if (debugAPI) {
              console.log(response.data);
            }
            setAnalysisState(response.data);
         });
  }, []);

  return (
    <form onSubmit={saveAnalysisOptions}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <span>
          <h2 style={{display: 'inline-block', marginBottom: '0'}}>Análise</h2>
          <Button variant="contained" type="submit" style={{float: 'right'}} endIcon={<SaveIcon />}>Salvar</Button>
        </span>

        <FormControl sx={{ m: 3 }} component="fieldset" variant="standard">
          <FormLabel component="legend">Selecionar estratégias de análise</FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox checked={analysisState.ml_execution} onChange={handleChange} name="ml_execution" disabled />
              }
              label="Definir pontuação das métricas"
            />
            <FormControlLabel
              control={
                <Checkbox checked={analysisState.ml_pipeline} onChange={handleChange} name="ml_pipeline" />
              }
              label="Utilizar metadados do Pipeline para etapa de planejamento"
            />
          </FormGroup>
          <FormHelperText>OBS: Selecionar ou não selecionar determinadas estratégias podem causar impactos caso certas etapas de planejamento forem selecionadas</FormHelperText>
        </FormControl>

        <Snackbar open={validAnalysisVisible} autoHideDuration={6000} onClose={handleCloseSuccessToast}>
          <Alert onClose={handleCloseSuccessToast} severity="success">
            <AlertTitle><strong>Sucesso!</strong></AlertTitle>
            Configurações salvas com sucesso!
          </Alert>
        </Snackbar>
      </Box>
    </form>
  );
}

export default AnalysisMenu;