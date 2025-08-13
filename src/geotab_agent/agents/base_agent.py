import abc
from typing import Dict, Any
from geotab_agent.config import settings
from geotab_agent.llm import BaseLLMProvider, GeminiProvider, OpenAIProvider


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
        self._llm_provider: BaseLLMProvider | None = None
        self._configure_llm()

    def _configure_llm(self):
        """
        Configura y prepara el proveedor de LLM basado en la configuración.
        Este es un ejemplo del patrón de diseño Factory.
        """
        provider_name = settings.LLM_PROVIDER.lower()
        if provider_name == "gemini":
            self._llm_provider = GeminiProvider()
        elif provider_name == "openai":
            self._llm_provider = OpenAIProvider()
        else:
            raise ValueError(f"Proveedor de LLM no soportado: '{settings.LLM_PROVIDER}'")

    def log(self, message: str, level: str = "info"):
        """
        Registra un mensaje en la consola con un prefijo de agente y nivel.
        """
        level_map = {
            "info": "✅",
            "warning": "⚠️",
            "error": "❌",
        }
        prefix = level_map.get(level.lower(), "ℹ️")
        print(f"{prefix} [{self.agent_name}] {message}")

    def _call_llm(self, prompt: str) -> str:
        """Delega la llamada al proveedor de LLM configurado."""
        if not self._llm_provider:
            raise RuntimeError("El proveedor de LLM no ha sido inicializado.")
        # La lógica de reintentos ahora está dentro de cada proveedor específico.
        return self._llm_provider.generate_content(prompt)

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