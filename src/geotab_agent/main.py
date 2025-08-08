from geotab_agent.config import settings


def run():
    """
    Punto de entrada principal para ejecutar la aplicación.
    Demuestra la carga de configuración.
    """
    print("Iniciando el agente de Geotab...")
    print(f"Modelo Gemini a usar: {settings.GEMINI_MODEL_NAME}")
    # Por seguridad, no imprimimos la clave completa, solo verificamos que existe.
    print(f"Clave de Google API cargada: {'Sí' if settings.GOOGLE_API_KEY else 'No'}")


if __name__ == "__main__":
    run()
