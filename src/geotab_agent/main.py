from geotab_agent.agents import OrchestratorAgent


def run():
    """
    Punto de entrada principal para ejecutar la aplicación.
    Aquí probamos el flujo de trabajo de los agentes.
    """
    print("--- Generador de Add-In de Geotab ---")

    # 1. Definimos la solicitud del usuario (hardcodeada por ahora)
    user_request = "Crea un Add-In de Geotab que muestre un simple 'Hola Mundo Geotab' en la página."

    # 2. Instanciamos el Orquestador
    orchestrator = OrchestratorAgent()

    # 3. Ejecutamos el proceso de orquestación
    orchestrator.run(user_request=user_request)

    print("\n--- Proceso Finalizado ---")


if __name__ == "__main__":
    run()
