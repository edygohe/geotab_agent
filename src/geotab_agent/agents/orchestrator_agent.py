from .base_agent import BaseAgent
from .analyst_agent import AnalystAgent
from .designer_agent import DesignerAgent
from ..mcp import Message, Task, TaskInput, Result
from typing import Dict, Any

# TODO: Hacer que el idioma del prompt sea configurable en el futuro.
PLANNING_PROMPT_TEMPLATE = """
# ROL Y OBJETIVO
Eres el "Agente Orquestador", el gestor central de un sistema multi-agente diseñado para crear Add-Ins de Geotab. Tu principal responsabilidad es interpretar la solicitud de un usuario y traducirla en un plan de desarrollo de alto nivel.
Este plan servirá como la hoja de ruta para un equipo de agentes especializados (Analista, Diseñador, Programador, etc.).

# PROTOCOLO DE COMUNICACIÓN
El sistema opera bajo un Protocolo de Comunicación Multi-Agente (MCP), donde el resultado de un agente es la entrada para el siguiente. Por lo tanto, el plan que generes debe ser claro, secuencial y accionable para que el siguiente agente (el Analista) pueda trabajar con él.

# TAREA
Analiza la siguiente solicitud de usuario y crea un plan de desarrollo conciso en formato de lista numerada.
La respuesta debe estar completamente en español.

---
Solicitud del Usuario: '{user_request}'
---
"""


class OrchestratorAgent(BaseAgent):
    """
    El agente orquestador que gestiona el flujo de trabajo completo para la
    creación de un Add-In.
    """

    def __init__(self):
        super().__init__(agent_name="Orchestrator")
        # Inicializamos los agentes que este orquestador va a dirigir
        self.analyst = AnalystAgent()
        self.designer = DesignerAgent()

    def run(self, user_request: str) -> Dict[str, Any]:
        """
        Orquesta todo el proceso de generación del Add-In utilizando el MCP.
        """
        print(f"🚀 Orquestador recibió la tarea: '{user_request}'")

        # 1. Planificación (Orchestrator -> LLM)
        print("\n----- 📝 ESTADO: PLANIFICACIÓN -----")
        plan_output = self._generate_plan(user_request)
        print("✅ Plan generado con éxito.")
        print("\n--- Plan Generado ---")
        print(plan_output["plan"])
        print("---------------------")

        # 2. Análisis (Orchestrator -> Analyst)
        print("\n----- 🔎 ESTADO: ANÁLISIS -----")
        analysis_task = Task(
            description="Generar especificaciones a partir de un plan de alto nivel.",
            input=TaskInput(parameters=plan_output)
        )
        analysis_message = Message(
            fromAgent=self.agent_name,
            toAgent=self.analyst.agent_name,
            task=analysis_task
        )
        print(f"📨 Enviando mensaje a {self.analyst.agent_name} (ID: {analysis_message.messageId})")
        
        specifications_output = self.analyst.run(input_data=analysis_message.task.input.parameters)
        analysis_message.result = Result(status="success", output=specifications_output)
        
        print(f"✅ {self.analyst.agent_name} completó la tarea con éxito.")
        print("\n--- Especificaciones Generadas ---")
        print(analysis_message.result.output["specifications"])
        print("----------------------------------")

        # 3. Diseño (Orchestrator -> Designer)
        print("\n----- 🎨 ESTADO: DISEÑO -----")
        design_task = Task(
            description="Crear diseño técnico a partir de especificaciones.",
            input=TaskInput(parameters=analysis_message.result.output)
        )
        design_message = Message(
            fromAgent=self.agent_name,
            toAgent=self.designer.agent_name,
            task=design_task
        )
        print(f"📨 Enviando mensaje a {self.designer.agent_name} (ID: {design_message.messageId})")
        
        design_output = self.designer.run(input_data=design_message.task.input.parameters)
        design_message.result = Result(status="success", output=design_output)

        print(f"✅ {self.designer.agent_name} completó la tarea con éxito.")
        print("\n--- Diseño Técnico Generado ---")
        print(design_message.result.output["design"])
        print("-------------------------------")

        # Devolvemos el diccionario de salida del último paso.
        return design_message.result.output

    def _generate_plan(self, user_request: str) -> Dict[str, Any]:
        """Interactúa con el LLM para generar un plan de desarrollo de alto nivel."""
        prompt = PLANNING_PROMPT_TEMPLATE.format(user_request=user_request)
        print("🧠 Pensando... Contactando al LLM para generar un plan.")
        response = self._model.generate_content(prompt)
        return {"plan": response.text}