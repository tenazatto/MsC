import * as React from 'react';
import Box from '@mui/material/Box';
import MetricsMenu from './Metrics-Menu'
import AnalysisMenu from './Analysis-Menu'
import PlanningMenu from './Planning-Menu'
import ManualPipelineMenu from './Manual-Pipeline-Menu'
import AutoPipelineMenu from './Auto-Pipeline-Menu'

function MenuChoice(props) {
  const chosenComponent = (choice) => {
    if (choice === 'Análise') {
      return (
        <AnalysisMenu />
      );
    } else if (choice === 'Métricas') {
      return (
        <MetricsMenu />
      );
    } else if (choice === 'Planejamento') {
      return (
        <PlanningMenu />
      );
    } else if (choice === 'Pipeline Manual') {
      return (
        <ManualPipelineMenu />
      );
    } else if (choice === 'Pipeline Autônomo') {
      return (
        <AutoPipelineMenu />
      );
    }

    return (
      <div>Componente ainda não implementado</div>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
      {/*<div>{props.choice}</div>*/}

      {chosenComponent(props.choice)}
    </Box>
  );
}

export default MenuChoice;
