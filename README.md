Geotab Genesis: Sistema de Generación de Add-Ins con IA

Geotab Genesis es un sistema multi-agente que automatiza la creación y despliegue de Add-Ins para la plataforma MyGeotab. Utilizando un modelo de lenguaje avanzado (LLM), este sistema interpreta solicitudes en lenguaje natural, diseña, codifica y despliega un Add-In funcional en una URL pública, listo para ser probado.

## ✨ Características Principales

-   **Generación Basada en Prompts:** Crea Add-Ins a partir de descripciones simples en lenguaje natural.
-   **Arquitectura Multi-Agente:** Orquesta un equipo de agentes especializados (Diseñador, Programador, Desplegador) para una máxima modularidad.
-   **Despliegue Automatizado:** Integra y despliega automáticamente el código generado en GitHub Pages.
-   **Código de Calidad:** Sigue las mejores prácticas para el desarrollo de Add-Ins de Geotab, incluyendo la creación de mapas interactivos con Leaflet.js.
-   **Extensible:** Diseñado para ser fácilmente ampliable con nuevos agentes o capacidades.

## 🏗️ Arquitectura

El sistema utiliza un `OrchestratorAgent` para dirigir el flujo de trabajo, desde la interpretación de la solicitud hasta el despliegue final.

```mermaid
graph TD
    subgraph "Usuario"
        A[Usuario envía Prompt a la UI]
    end

    subgraph "Servidor (FastAPI)"
        B(Endpoint /generate-addin)
    end

    subgraph "Sistema de Agentes: Geotab Genesis"
        C[OrchestratorAgent]
        D[CoderAgent]
        E[DeployerAgent]
        F{LLM Provider (Gemini)}
        G[BaseAgent]

        B -- 1. Inicia Orquestador --> C

        C -- 2. Genera Plan y Diseño Técnico --> F
        F -- 3. Devuelve Diseño (HTML/CSS/JS) --> C

        C -- 4. Pasa Diseño a Coder --> D
        D -- 5. Escribe archivos en ./output --> H(Directorio ./output)

        C -- 6. Pasa ruta de código a Deployer --> E
        E -- 7. Copia archivos a Repo Local --> I(Repo Local de GitHub Pages)
        I -- 8. Actualiza config.json --> I
        E -- 9. Git Push --> J((GitHub))
        J -- 10. Despliega en GitHub Pages --> K((URL Pública))
        E -- 11. Hace Polling a la URL --> K

        C -- hereda de --> G
        D -- hereda de --> G
        E -- hereda de --> G
        G -- usa --> F
    end

    A --> B
    E -- 12. Devuelve resultado final --> C
    C -- 13. Devuelve JSON a FastAPI --> B
    B -- 14. Devuelve JSON a UI --> A

    style F fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
    style K fill:#9f9,stroke:#333,stroke-width:2px
```

## 🚀 Instalación y Configuración

Sigue estos pasos para poner en marcha el sistema en tu entorno local.

### Prerrequisitos
-   Python 3.10 o superior
-   Git

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd geotab_agent
```

### 2. Crear un Entorno Virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

```env
# Clave de API para el Modelo de Lenguaje (Gemini)
GEMINI_API_KEY="TU_API_KEY_DE_GEMINI"

# Token de Acceso Personal de GitHub con permisos de 'repo'
GITHUB_TOKEN="TU_GITHUB_PAT"

# URL del repositorio donde se desplegarán los Add-Ins (ej: https://github.com/tu_usuario/tu_repo_pages.git)
GITHUB_REPO_URL="URL_DE_TU_REPOSITORIO_DE_GITHUB_PAGES"

# Ruta local donde tienes clonado el repositorio de GitHub Pages
LOCAL_REPO_PATH="RUTA/A/TU/CLON/LOCAL"

# Tu nombre de usuario de GitHub
GITHUB_USERNAME="tu_usuario_de_github"
```

## 🏃‍♂️ Uso

1.  **Iniciar el Servidor:**
    ```bash
    uvicorn main:app --reload
    ```
2.  **Abrir la Interfaz:**
    Abre tu navegador y ve a `http://127.0.0.1:8000`.

3.  **Generar un Add-In:**
    Escribe una solicitud en el cuadro de texto, por ejemplo:
    > "Crea un Add-In que muestre los 5 vehículos más cercanos en un mapa y una lista interactiva."

    Haz clic en "Generar Add-In" y observa cómo el sistema trabaja. Al finalizar, recibirás la URL pública y el `config.json` para probar tu nuevo Add-In en MyGeotab.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar el sistema, por favor abre un *issue* o envía un *pull request*.