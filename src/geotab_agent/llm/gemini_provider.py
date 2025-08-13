import time
import google.generativeai as genai
from google.api_core import exceptions
from .base_provider import BaseLLMProvider
from geotab_agent.config import settings

class GeminiProvider(BaseLLMProvider):
    """Proveedor de LLM para la API de Google Gemini."""

    def __init__(self):
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self._model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL_NAME,
                generation_config=settings.GENERATION_CONFIG,
            )
            print("✅ Proveedor de LLM 'Gemini' inicializado.")
        except Exception as e:
            print(f"❌ Error al configurar Gemini: {e}")
            raise

    def generate_content(self, prompt: str, retries: int = 1, delay: int = 5) -> str:
        """Llama al modelo Gemini con lógica de reintentos para errores de cuota."""
        attempt = 0
        while attempt <= retries:
            try:
                response = self._model.generate_content(prompt)
                return response.text
            except exceptions.ResourceExhausted as e:
                if attempt < retries:
                    print(f"⚠️ [GeminiProvider] Cuota de API excedida. Reintentando en {delay} segundos...")
                    time.sleep(delay)
                    attempt += 1
                else:
                    print(f"❌ [GeminiProvider] Cuota de API excedida. No quedan más reintentos. Error: {e}")
                    raise
            except Exception as e:
                print(f"❌ [GeminiProvider] Ocurrió un error inesperado: {e}")
                raise
        return "" # No debería llegar aquí