from unittest.mock import patch, MagicMock
from geotab_agent.agents import DesignerAgent
import pytest

def test_designer_agent_run():
    """
    Prueba que el DesignerAgent formatea el prompt correctamente y llama al LLM.
    """
    # 1. Preparación (Arrange)
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Mocked design"

    # Mockeamos las llamadas a la librería de Gemini
    with patch('geotab_agent.agents.base_agent.genai.configure') as mock_configure, \
         patch('geotab_agent.agents.base_agent.genai.GenerativeModel', return_value=mock_model) as mock_generative_model:

        # Instanciamos el agente
        designer = DesignerAgent()

        # 2. Actuación (Act)
        input_data = {"specifications": "Requirements: 1. Button 'Click me'. 2. Text 'Hello'."}
        result = designer.run(input_data=input_data)

        # 3. Aserción (Assert)
        mock_configure.assert_called_once()
        mock_generative_model.assert_called_once()
        mock_model.generate_content.assert_called_once()

        call_args, _ = mock_model.generate_content.call_args
        prompt_sent_to_llm = call_args[0]
        assert input_data["specifications"] in prompt_sent_to_llm

        assert result == {"design": "Mocked design"}

        # Probamos el caso de error
        with pytest.raises(ValueError, match="Las 'specifications' son requeridas"):
            designer.run(input_data={})