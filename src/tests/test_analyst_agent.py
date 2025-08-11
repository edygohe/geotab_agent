from unittest.mock import patch, MagicMock
from geotab_agent.agents import AnalystAgent
import pytest

def test_analyst_agent_run():
    """
    Prueba que el AnalystAgent formatea el prompt correctamente y llama al LLM.
    """
    # 1. Preparación (Arrange)
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Mocked specifications"

    # Mockeamos las llamadas a la librería de Gemini para evitar llamadas reales a la API
    # y para asegurarnos de que nuestro agente se inicializa con un modelo mockeado.
    with patch('geotab_agent.agents.base_agent.genai.configure') as mock_configure, \
         patch('geotab_agent.agents.base_agent.genai.GenerativeModel', return_value=mock_model) as mock_generative_model:

        # Instanciamos el agente. Su __init__ ahora llamará a nuestras funciones mockeadas.
        analyst = AnalystAgent()

        # 2. Actuación (Act)
        input_data = {"plan": "1. Create a button. 2. Show 'Hello World'."}
        result = analyst.run(input_data=input_data)

        # 3. Aserción (Assert)
        # Verificamos que la configuración y el modelo fueron llamados.
        mock_configure.assert_called_once()
        mock_generative_model.assert_called_once()

        # Verificamos que el método 'generate_content' de nuestro modelo mock fue llamado.
        mock_model.generate_content.assert_called_once()

        # Verificamos que el prompt enviado al LLM contiene el plan de entrada.
        call_args, _ = mock_model.generate_content.call_args
        prompt_sent_to_llm = call_args[0]
        assert input_data["plan"] in prompt_sent_to_llm

        # Verificamos que el resultado es el que devolvió nuestro mock.
        assert result == {"specifications": "Mocked specifications"}

        # Probamos el caso de error
        with pytest.raises(ValueError, match="El 'plan' es requerido"):
            analyst.run(input_data={})