from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any


class Settings(BaseSettings):
    """
    Clase que gestiona la configuración de la aplicación.
    Carga automáticamente las variables desde un archivo .env y las valida.
    """

    # Carga las variables desde un archivo .env en la raíz del proyecto.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- Claves de API (leída desde .env) ---
    # Pydantic se encarga de la validación. Si no encuentra la variable,
    # lanzará un error claro y detallado.
    GOOGLE_API_KEY: str

    # --- Configuración del Modelo Gemini (con valores por defecto) ---
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash-latest"

    GENERATION_CONFIG: Dict[str, Any] = {
        "temperature": 0.2,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 8192, # Aumentado para tareas complejas de código
    }


# Creamos una única instancia que será usada en toda la aplicación
settings = Settings()