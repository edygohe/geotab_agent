from .base_agent import BaseAgent
from typing import Dict, Any

# TODO: Hacer que el idioma del prompt sea configurable en el futuro.
ANALYST_PROMPT_TEMPLATE = """
# ROL Y OBJETIVO
Eres el "Agente Analista", un especialista en ingeniería de requisitos de software. Tu función es tomar un plan de desarrollo de alto nivel y convertirlo en un documento de especificaciones funcionales detallado.

# CONTEXTO
Estás trabajando en un equipo de agentes de IA para construir un Add-In de Geotab. El "Agente Orquestador" te ha proporcionado el siguiente plan. Tu resultado será utilizado por el "Agente Diseñador" para crear la arquitectura técnica y el diseño de la interfaz.

# TAREA
Analiza el siguiente plan de desarrollo y genera las especificaciones funcionales.
Debes detallar:
1.  **Requisitos Funcionales:** ¿Qué debe hacer el Add-In? Describe cada función de forma clara y sin ambigüedades.
2.  **Requisitos No Funcionales:** Considera aspectos como la usabilidad, el rendimiento y la apariencia (ej. "debe ser intuitivo", "la carga debe ser rápida").
3.  **Datos Requeridos:** ¿Qué datos de la API de Geotab podrían ser necesarios? (Aunque no los implementes, menciónalos).
4.  **Componentes de la Interfaz (UI):** Describe los elementos visuales necesarios (ej. un botón, un área de texto, un título).

La respuesta debe estar completamente en español y bien estructurada con encabezados.

---
Plan de Desarrollo Proporcionado:
{task_description}
---
"""


class AnalystAgent(BaseAgent):
    """
    El agente analista que transforma un plan de alto nivel en especificaciones
    detalladas.
    """

    def __init__(self):
        super().__init__(agent_name="Analyst")

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Toma un plan y genera las especificaciones.
        """
        print(f"🧠 Analista recibió el plan. Generando especificaciones...")
        plan = input_data.get("plan", "")
        if not plan:
            raise ValueError("El 'plan' es requerido en los datos de entrada para el AnalystAgent.")
        prompt = ANALYST_PROMPT_TEMPLATE.format(task_description=plan)
        response = self._call_llm(prompt)
        return {"specifications": response.text}