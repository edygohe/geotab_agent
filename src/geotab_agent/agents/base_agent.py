import abc
import google.generativeai as genai
from typing import Dict, Any
from geotab_agent.config import settings


class BaseAgent(abc.ABC):
    """
    Clase base abstracta para todos los agentes especializados.

    Configura el cliente de Gemini y define la interfaz común que todos
    los agentes deben seguir.
    """

    def __init__(self, agent_name: str):
        """
        Inicializa el agente, configurando su nombre y el cliente de Gemini.

        Args:
            agent_name: Un nombre descriptivo para la instancia del agente.
        """
        self.agent_name = agent_name
        self._model = None
        self._configure_llm()

    def _configure_llm(self):
        """Configura y prepara el modelo generativo de Gemini."""
        try:
            # La configuración es global, por lo que solo necesita hacerse una vez,
            # pero es seguro llamarla varias veces.
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self._model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL_NAME,
                generation_config=settings.GENERATION_CONFIG,
            )
            print(f"✅ Agente '{self.agent_name}' inicializado. Modelo Gemini listo.")
        except Exception as e:
            print(f"❌ Error al configurar Gemini para el agente '{self.agent_name}': {e}")
            # Re-lanzar la excepción es importante para detener la ejecución si el LLM no está disponible.
            raise

    @abc.abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        El punto de entrada principal para la lógica del agente.
        Debe ser implementado por cada subclase.

        Args:
            input_data: Un diccionario con los datos necesarios para realizar la tarea.

        Returns:
            Un diccionario con el resultado de la tarea.
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.agent_name}')>"