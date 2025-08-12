from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pathlib
from geotab_agent.agents import OrchestratorAgent

# Creamos la aplicación FastAPI
app = FastAPI(
    title="Geotab Genesis API",
    description="Una API para generar Add-Ins de Geotab usando agentes de IA.",
    version="0.1.0",
)

# --- Configuración de CORS (La "Lista de Invitados VIP") ---
# Esto es crucial. Le decimos al navegador que permita peticiones
# desde MyGeotab a nuestro servidor localhost.
origins = [
    "https://my.geotab.com",
    # También es útil añadir localhost para pruebas locales del front-end
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    prompt: str

@app.post("/generate-addin")
def generate_addin(request: GenerationRequest):
    orchestrator = OrchestratorAgent()
    # 1. El orquestador ejecuta la tarea y devuelve la ruta de salida
    result = orchestrator.run(user_request=request.prompt)
    
    output_path = result.get("code_path")
    config_content = ""

    # 2. Si tenemos una ruta, intentamos leer el config.json generado
    if output_path:
        try:
            config_file_path = pathlib.Path(output_path) / "config.json"
            if config_file_path.is_file():
                config_content = config_file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo leer el archivo config.json generado. Error: {e}")

    # 3. Añadimos el contenido del JSON al diccionario de resultados
    result['config_json'] = config_content
    return {"status": "success", "message": "Add-In generation process completed.", "output": result}

@app.get("/health")
def health_check():
    """Un endpoint simple para verificar que la API está funcionando."""
    return {"status": "ok"}