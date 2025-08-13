from .base_agent import BaseAgent
from .coder_agent import CoderAgent
from .deployer_agent import DeployerAgent
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

# BUENAS PRÁCTICAS PARA EL CÓDIGO JAVASCRIPT
- **Llamadas a la API:** Usa siempre la cadena `.then().catch()` para manejar las llamadas a la API de Geotab. Llama siempre al `callback()` de `initialize` al final de tu lógica, tanto en éxito como en error.
- **Mapas (IMPORTANTE):** Para mostrar un mapa, la forma más robusta es crear un mapa autocontenido usando la librería **Leaflet.js**. No intentes usar `state.getMap()`.

  **Ejemplo de Add-In con Mapa Autocontenido (Leaflet.js):**
  
  **1. `index.html` (Debe incluir Leaflet y un div para el mapa):**
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Mi Add-In con Mapa</title>
      <!-- CSS de Leaflet -->
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
      <link rel="stylesheet" href="style.css">
  </head>
  <body>
      <div id="geotabAddin">
          <h2>Vehículos en el Mapa</h2>
          <ul id="vehicle-list"></ul>
          <!-- El div donde se renderizará el mapa -->
          <div id="map"></div>
      </div>
      <!-- JS de Leaflet (antes de tu script) -->
      <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
      <script src="script.js"></script>
  </body>
  </html>
  ```

  **2. `style.css` (Debe dar una altura al div del mapa):**
  ```css
  #map {{
      height: 400px;
      width: 100%;
      margin-top: 10px;
  }}

  #vehicle-list li {{
      cursor: pointer;
      padding: 8px;
      border-bottom: 1px solid #eee;
  }}

  #vehicle-list li:hover {{
      background-color: #f0f8ff;
  }}
  #vehicle-list li {{
      cursor: pointer;
      padding: 8px;
      border-bottom: 1px solid #eee;
  }}

  #vehicle-list li:hover {{
      background-color: #f0f8ff;
  }}
  ```

  **3. `script.js` (Debe inicializar el mapa y añadir los datos):**
  ```javascript
  geotab.addin.mapaAddin = function (api, state) {{
      'use strict';

      let map; // Variable para guardar la instancia del mapa

      return {{
          initialize: function (api, state, callback) {{
              // 1. Inicializar el mapa Leaflet en nuestro div
              map = L.map('map').setView([43.6532, -79.3832], 5); // Coordenadas iniciales y zoom

              // 2. Añadir la capa de tiles (el fondo del mapa)
              L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              }}).addTo(map);

              // 3. Obtener los datos para mostrar en el mapa
              // Patrón de 2 pasos: Get<Device> -> Get<DeviceStatusInfo>
              api.call("Get", {{ typeName: "Device", resultsLimit: 5 }})
                  .then(function(devices) {{
                      if (!devices || devices.length === 0) return Promise.resolve([]);
                      const deviceIds = devices.map(d => d.id);
                      return api.call("Get", {{ typeName: "DeviceStatusInfo", search: {{ deviceSearch: {{ ids: deviceIds }} }} }});
                  }})
                  .then(function(deviceStatusInfos) {{
                      // 4. Añadir un marcador por cada vehículo con coordenadas
                      deviceStatusInfos.forEach(function(statusInfo) {{
                          if (statusInfo.latitude && statusInfo.longitude) {{
                              L.marker([statusInfo.latitude, statusInfo.longitude]).addTo(map)
                                  .bindPopup(statusInfo.device.name);
                          }}
                      }});
                      callback(); // ¡Crucial!
                  }})
                  .catch(function(error) {{
                      console.error("Error inicializando el Add-In:", error);
                      callback(); // ¡Crucial!
                  }});
          }}
      }};
  }};
  ```

  **Forma INCORRECTA (NO usar nunca):**
  ```javascript
  // ESTO FALLARÁ
  const result = await api.call("Get", {{ typeName: "Device" }}); 
  ```
- **Seguridad:** No incluyas claves de API ni información sensible en el código del lado del cliente.
- **Traducción:** Si el Add-In necesita ser multilingüe, asegúrate de que el `config.json` incluya la propiedad `"translator"` y que el JavaScript llame a `api.translate()` después de que la UI se haya renderizado.

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
        try:
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
            final_output["status"] = "success"
            return final_output
        except Exception as e:
            # Captura cualquier excepción no controlada durante el flujo
            error_msg = f"Ocurrió un error inesperado en el orquestador: {e}"
            self.log(error_msg, "error")
            # Imprime el traceback para depuración en el servidor
            import traceback
            traceback.print_exc()
            return {"status": "failed", "message": error_msg}

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
        design_text = self._call_llm(design_prompt)
        design_output = {"design": design_text}
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
        plan_text = self._call_llm(prompt)
        return {"plan": plan_text}