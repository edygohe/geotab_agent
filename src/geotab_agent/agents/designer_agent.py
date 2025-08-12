from .base_agent import BaseAgent
from typing import Dict, Any

# TODO: Hacer que el idioma del prompt sea configurable en el futuro.
DESIGNER_PROMPT_TEMPLATE = """
# ROL Y OBJETIVO
Eres el "Agente Diseñador", un desarrollador front-end y arquitecto de software especializado en Add-Ins de Geotab. Tu función es tomar un documento de especificaciones funcionales y traducirlo en un diseño técnico completo y listo para ser implementado.

# CONTEXTO
Has recibido las especificaciones del "Agente Analista". Tu diseño será la entrada directa para el "Agente Programador", que escribirá el código final. Por lo tanto, tu diseño debe ser extremadamente claro, completo y seguir las mejores prácticas para Add-Ins de Geotab.

# TAREA
Basado en las siguientes especificaciones, genera el diseño técnico completo. El diseño debe incluir:
1.  **Estructura de Archivos:** Una lista de los archivos necesarios (ej. `index.html`, `style.css`, `script.js`).
2.  **Código HTML (`index.html`):** El código HTML completo. Debe incluir una referencia al CSS y al JS. Asegúrate de incluir el `div` con el id "geotabAddin" que es requerido por Geotab.
3.  **Código CSS (`style.css`):** El código CSS para dar estilo a los elementos.
4.  **Código JavaScript (`script.js`):** El código JavaScript para la lógica. Debe incluir el esqueleto de la función `geotab.addin.initialize` para interactuar con la API de Geotab. 
    **Importante:** Para cualquier lista de elementos en la que se pueda hacer clic (como una lista de vehículos), utiliza la técnica de **delegación de eventos** (event delegation). Asigna un único 'click listener' al contenedor de la lista (ej. `<ul>`) en lugar de a cada elemento `<li>` individualmente. Esto asegura que los eventos funcionen incluso si la lista se actualiza dinámicamente.
5.  **Manifiesto de Configuración (`config.json`):** El código JSON completo para el archivo de configuración. La URL debe ser un placeholder como `https://<TU_USUARIO.github.io>/<TU_REPOSITORIO>/<ADDIN_NAME>/index.html`.

La respuesta debe estar completamente en español y estructurada con bloques de código markdown para cada archivo.

---
Especificaciones Funcionales Proporcionadas:
{task_description}
---
"""


class DesignerAgent(BaseAgent):
    """
    El agente diseñador que crea la estructura de archivos y el código
    base (HTML, CSS, JS) a partir de las especificaciones.
    """

    def __init__(self):
        super().__init__(agent_name="Designer")

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Toma las especificaciones y genera el diseño técnico.
        """
        print(f"🎨 Diseñador recibió las especificaciones. Creando diseño técnico...")
        specifications = input_data.get("specifications", "")
        if not specifications:
            raise ValueError("Las 'specifications' son requeridas en los datos de entrada para el DesignerAgent.")
        prompt = DESIGNER_PROMPT_TEMPLATE.format(
            task_description=specifications
        )
        response = self._call_llm(prompt)
        return {"design": response.text}