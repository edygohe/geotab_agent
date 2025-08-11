from unittest.mock import patch
from geotab_agent.agents import OrchestratorAgent

def test_orchestrator_agent_run_flow():
    """
    Prueba el flujo completo del OrchestratorAgent, asegurando que llama
    a sus sub-agentes en el orden correcto.
    """
    # 1. Preparación (Arrange)
    user_request = "Crear un Add-In de Hola Mundo."
    mock_plan_output = {"plan": "Plan generado por el mock."}
    mock_specs_output = {"specifications": "Especificaciones generadas por el mock."}
    mock_design_output = {"design": "Diseño generado por el mock."}

    # Mockeamos los métodos internos y los agentes dependientes para aislar al orquestador.
    # No queremos probar la generación real del plan o el analista aquí, solo el flujo.
    with patch.object(OrchestratorAgent, '_generate_plan', return_value=mock_plan_output) as mock_generate_plan, \
         patch('geotab_agent.agents.orchestrator_agent.AnalystAgent') as MockAnalyst, \
         patch('geotab_agent.agents.orchestrator_agent.DesignerAgent') as MockDesigner:

        # Configuramos el mock del AnalystAgent para que su método 'run' devuelva las especificaciones mock.
        mock_analyst_instance = MockAnalyst.return_value
        mock_analyst_instance.run.return_value = mock_specs_output
        mock_analyst_instance.agent_name = "Analyst"  # <-- Añadimos esta línea

        # Configuramos el mock del DesignerAgent
        mock_designer_instance = MockDesigner.return_value
        mock_designer_instance.run.return_value = mock_design_output
        mock_designer_instance.agent_name = "Designer"  # <-- Y esta para el diseñador

        # 2. Actuación (Act)
        orchestrator = OrchestratorAgent()
        result = orchestrator.run(user_request=user_request)

        # 3. Aserción (Assert)
        # Verificamos que cada agente fue llamado en el orden correcto y con el input correcto.
        mock_generate_plan.assert_called_once_with(user_request)
        MockAnalyst.assert_called_once()
        mock_analyst_instance.run.assert_called_once_with(input_data=mock_plan_output)
        MockDesigner.assert_called_once()
        mock_designer_instance.run.assert_called_once_with(input_data=mock_specs_output)
        assert result == mock_design_output