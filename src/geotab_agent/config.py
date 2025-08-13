from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any

class Settings(BaseSettings):
    """
    Centraliza la configuración de la aplicación, cargando valores desde
    un archivo .env para mantener las claves seguras y fuera del código.
    """
    # Cargar variables desde un archivo .env
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # --- Configuración General del LLM ---
    LLM_PROVIDER: str = "gemini" # Puede ser "gemini" o "openai"

    # --- Configuración de Google Gemini ---
    GOOGLE_API_KEY: str
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash"
    GENERATION_CONFIG: Dict[str, Any] = {"temperature": 0.1}

    # --- Configuración de OpenAI ---
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"

    # --- Configuraciones para el despliegue en GitHub ---
    GITHUB_USERNAME: str
    GITHUB_TOKEN: str # Tu Personal Access Token
    # URL del repositorio donde se despliegan los Add-Ins
    GITHUB_REPO_URL: str # ej: https://github.com/edygohe/addins.git
    # URL base para GitHub Pages donde se sirven los Add-Ins
    GITHUB_PAGES_BASE_URL: str # ej: https://edygohe.github.io/addins
    # Ruta local al repositorio donde se despliegan los Add-Ins
    GITHUB_ADDINS_REPO_PATH: str # ej: C:/opt/ws_egomez/addins

# Instancia única de la configuración para ser usada en toda la aplicación
settings = Settings()