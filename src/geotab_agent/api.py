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
    # Permitimos cualquier subdominio de ngrok para el túnel HTTPS
    allow_origin_regex=r"https://.*\.ngrok-free\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    prompt: str

@app.post("/generate-addin")
def generate_addin(request: GenerationRequest):
    orchestrator = OrchestratorAgent()
    # 1. El orquestador ejecuta todo el flujo, incluido el despliegue
    # y la actualización del config.json.
    result = orchestrator.run(input_data={"user_request": request.prompt})
    
    # 2. El 'result' ya contiene toda la información necesaria,
    # incluido el 'config_json' actualizado por el DeployerAgent.
    return {"status": "success", "message": "Add-In generation process completed.", "output": result}

@app.get("/health")
def health_check():
    """Un endpoint simple para verificar que la API está funcionando."""
    return {"status": "ok"}