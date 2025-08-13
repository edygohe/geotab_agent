from openai import OpenAI, APIError
from .base_provider import BaseLLMProvider
from geotab_agent.config import settings

class OpenAIProvider(BaseLLMProvider):
    """Proveedor de LLM para la API de OpenAI."""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("La clave de API de OpenAI no está configurada en el archivo .env")
        try:
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self._model_name = settings.OPENAI_MODEL_NAME
            print("✅ Proveedor de LLM 'OpenAI' inicializado.")
        except Exception as e:
            print(f"❌ Error al configurar OpenAI: {e}")
            raise

    def generate_content(self, prompt: str) -> str:
        """Llama al modelo de OpenAI con manejo de errores."""
        try:
            completion = self._client.chat.completions.create(
                model=self._model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content or ""
        except APIError as e:
            # Maneja errores específicos de la API de OpenAI (ej. rate limits, auth)
            print(f"❌ [OpenAIProvider] Error de API: {e.status_code} - {e.message}")
            raise # Vuelve a lanzar para que el orquestador lo maneje
        except Exception as e:
            # Maneja otros errores inesperados (ej. problemas de red)
            print(f"❌ [OpenAIProvider] Ocurrió un error inesperado: {e}")
            raise