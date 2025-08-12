from .base_agent import BaseAgent
from .coder_agent import CoderAgent
from .deployer_agent import DeployerAgent
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

# Nuevo prompt combinado para reducir las llamadas a la API
ANALYST_DESIGNER_PROMPT_TEMPLATE = """
# ROL Y OBJETIVO
Eres un "Agente de Diseño y Análisis", un híbrido entre un ingeniero de requisitos y un arquitecto de software especializado en Add-Ins de Geotab. Tu función es tomar un plan de desarrollo de alto nivel y convertirlo directamente en un diseño técnico completo y listo para ser implementado por un programador.

# TAREA
Basado en el siguiente plan, genera un diseño técnico que incluya:
1.  **Especificaciones Funcionales:** Una breve descripción de lo que el Add-In debe hacer.
2.  **Diseño de Archivos:** El código completo para `index.html`, `style.css` y `script.js` dentro de bloques de código markdown.
    - El HTML debe incluir el div `<div id="geotabAddin">`.
    - El JavaScript debe usar la técnica de **delegación de eventos** para las listas interactivas.

La respuesta debe estar completamente en español.

---
Plan de Desarrollo Proporcionado:
{plan}
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
        self.coder = CoderAgent()
        self.deployer = DeployerAgent()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orquesta todo el proceso de generación del Add-In utilizando el MCP.
        """
        user_request = input_data.get("user_request")
        if not user_request:
            error_msg = "La clave 'user_request' no se encontró en los datos de entrada."
            self.log(error_msg, "error")
            return {"status": "failed", "message": error_msg}

        self.log(f"Recibió la tarea: '{user_request}'")

        # Etapa 1: Planificación
        plan_output = self._execute_planning_stage(user_request)
        if not plan_output:
            return {"status": "failed", "message": "La etapa de planificación falló."}

        # Etapa 2: Diseño
        design_output = self._execute_design_stage(plan_output)
        if not design_output:
            return {"status": "failed", "message": "La etapa de diseño falló."}

        # Etapa 3: Codificación
        code_output = self._execute_coding_stage(design_output)
        if not code_output:
            return {"status": "failed", "message": "La etapa de codificación falló."}

        # Etapa 4: Despliegue
        deploy_result = self._execute_deployment_stage(code_output)
        if not deploy_result or deploy_result.get("deploy_status") == "failed":
            error_msg = f"{self.deployer.agent_name} no pudo desplegar el Add-In."
            self.log(error_msg, "error")
            return {"status": "failed", "message": error_msg, "output": deploy_result}

        # Unimos y devolvemos el resultado final
        final_output = code_output.copy()
        final_output.update(deploy_result)
        self.log("Proceso de despliegue finalizado.")
        return final_output

    def _execute_planning_stage(self, user_request: str) -> Dict[str, Any] | None:
        self.log("----- 📝 ESTADO: PLANIFICACIÓN -----")
        plan_output = self._generate_plan(user_request)
        if plan_output and plan_output.get("plan"):
            self.log("Plan generado con éxito.")
            self.log(f"--- Plan Generado ---\n{plan_output['plan']}\n---------------------")
            return plan_output
        return None

    def _execute_design_stage(self, plan_output: Dict[str, Any]) -> Dict[str, Any] | None:
        self.log("----- 🎨 ESTADO: ANÁLISIS Y DISEÑO -----")
        self.log("Generando especificaciones y diseño técnico en una sola llamada...")
        design_prompt = ANALYST_DESIGNER_PROMPT_TEMPLATE.format(plan=plan_output['plan'])
        design_response = self._call_llm(design_prompt)
        design_output = {"design": design_response.text}
        if not design_output or not design_output.get("design"):
            error_msg = "El LLM no pudo generar el diseño técnico."
            self.log(error_msg, "error")
            return None
        self.log("Diseño técnico generado con éxito.")
        self.log(f"--- Diseño Técnico Generado ---\n{design_output['design']}\n-------------------------------")
        return design_output

    def _execute_coding_stage(self, design_output: Dict[str, Any]) -> Dict[str, Any] | None:
        self.log("----- 💻 ESTADO: CODIFICACIÓN -----")
        code_output = self.coder.run(input_data=design_output)
        if not code_output or not code_output.get("code_path"):
            error_msg = f"{self.coder.agent_name} no pudo generar los archivos de código."
            self.log(error_msg, "error")
            return None
        self.log(f"{self.coder.agent_name} completó la tarea con éxito.")
        self.log(f"--- Código Generado ---\nArchivos guardados en: {code_output['code_path']}\n-----------------------")
        return code_output

    def _execute_deployment_stage(self, code_output: Dict[str, Any]) -> Dict[str, Any] | None:
        self.log("----- 🚀 ESTADO: DESPLIEGUE -----")
        return self.deployer.run(
            input_data={"source_path": code_output["code_path"]}
        )

    def _generate_plan(self, user_request: str) -> Dict[str, Any]:
        """Interactúa con el LLM para generar un plan de desarrollo de alto nivel."""
        prompt = PLANNING_PROMPT_TEMPLATE.format(user_request=user_request)
        self.log("Pensando... Contactando al LLM para generar un plan.")
        response = self._call_llm(prompt)
        return {"plan": response.text}