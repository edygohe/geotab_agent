# Diseño de Interacción del Orquestador

Este documento detalla cómo el `OrchestratorAgent` utiliza el Protocolo de Comunicación Multi-Agente (MCP) para gestionar el flujo de trabajo.

## Propósito

Mientras que el `ORCHESTRATOR_DESIGN.md` muestra la máquina de estados interna, este diagrama de secuencia se enfoca en las interacciones en tiempo de ejecución. Muestra cómo el orquestador construye y gestiona los objetos `Message` (definidos en `mcp/message.py`) para comunicarse con los agentes especializados.

## Diagrama de Secuencia

```mermaid
sequenceDiagram
    participant Main
    participant Orch as OrchestratorAgent
    participant MCP as MCP (message.py)
    participant Analyst as AnalystAgent
    participant Designer as DesignerAgent

    Main->>Orch: run(user_request)
    activate Orch

    Orch->>Orch: _generate_plan()
    Note right of Orch: 1. Se genera el plan inicial

    Orch->>MCP: new Message(to="Analyst", ...)
    Note left of MCP: Construye el mensaje para el Analista

    Orch->>Analyst: run(input_data)
    activate Analyst
    Analyst-->>Orch: specifications_output
    deactivate Analyst
    Note right of Orch: 2. Se reciben las especificaciones

    Orch->>MCP: new Message(to="Designer", ...)
    Note left of MCP: Construye el mensaje para el Diseñador

    Orch->>Designer: run(input_data)
    activate Designer
    Designer-->>Orch: design_output
    deactivate Designer
    Note right of Orch: 3. Se recibe el diseño técnico

    Orch-->>Main: final_output
    deactivate Orch
```