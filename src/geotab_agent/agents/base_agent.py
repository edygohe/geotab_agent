import abc
import time
import google.generativeai as genai
from typing import Dict, Any
from google.api_core import exceptions
from geotab_agent.config import settings # Ahora importa desde el archivo correcto


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
                generation_config=settings.GENERATION_CONFIG, # Ahora este campo existe
            )
            print(f"✅ Agente '{self.agent_name}' inicializado. Modelo Gemini listo.")
        except Exception as e:
            print(f"❌ Error al configurar Gemini para el agente '{self.agent_name}': {e}")
            # Re-lanzar la excepción es importante para detener la ejecución si el LLM no está disponible.
            raise

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

    def _call_llm(self, prompt: str, retries: int = 1, delay: int = 5) -> Any:
        """
        Llama al modelo LLM con una lógica de reintentos simple para manejar errores de cuota.
        """
        attempt = 0
        while attempt <= retries:
            try:
                return self._model.generate_content(prompt)
            except exceptions.ResourceExhausted as e:
                if attempt < retries:
                    self.log(f"Cuota de API excedida. Reintentando en {delay} segundos... (Intento {attempt + 1}/{retries})", "warning")
                    time.sleep(delay)
                    attempt += 1
                else:
                    self.log(f"Cuota de API excedida. No quedan más reintentos. Error: {e}", "error")
                    raise  # Vuelve a lanzar la excepción si se agotan los reintentos
            except Exception as e:
                self.log(f"Ocurrió un error inesperado al llamar al LLM: {e}", "error")
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