import os
import re
import json
from datetime import datetime
from typing import Dict, Any
from .base_agent import BaseAgent

class CoderAgent(BaseAgent):
    """
    El agente programador que toma un diseño técnico y escribe los archivos
    de código correspondientes en el disco.
    """

    def __init__(self, output_dir: str = "output"):
        super().__init__(agent_name="Coder")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Toma el diseño técnico, lo parsea y escribe los archivos.
        """
        print(f"💻 Programador recibió el diseño. Escribiendo archivos de código...")
        design_text = input_data.get("design", "")
        if not design_text:
            raise ValueError("El 'design' es requerido en los datos de entrada para el CoderAgent.")

        # Crear un directorio único para esta ejecución
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_path = os.path.join(self.output_dir, f"addin_{timestamp}")
        os.makedirs(project_path, exist_ok=True)

        # Parsear y escribir cada archivo
        self._write_file_from_block(design_text, "html", "index.html", project_path)
        self._write_file_from_block(design_text, "css", "style.css", project_path)
        self._write_file_from_block(design_text, "javascript", "script.js", project_path)
        self._write_config_json(project_path)

        print(f"✅ Código generado con éxito en: {project_path}")
        return {"code_path": project_path}

    def _write_file_from_block(self, text: str, lang: str, filename: str, path: str):
        """Extrae un bloque de código markdown y lo escribe en un archivo."""
        # La expresión regular anterior era demasiado estricta. Esta es más robusta
        # y captura todo el contenido entre los delimitadores del bloque de código.
        pattern = re.compile(rf"```{lang}(.*?)```", re.DOTALL)
        match = pattern.search(text)
        if match:
            # group(1) captura el contenido. .strip() elimina espacios y saltos de línea
            # al principio y al final, como el que queda después de la etiqueta de lenguaje.
            code = match.group(1).strip()
            file_path = os.path.join(path, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"   - Archivo creado: {file_path}")
        else:
            print(f"   - Advertencia: No se encontró bloque de código para '{lang}' en el diseño.")

    def _write_config_json(self, project_path: str):
        """Crea un archivo config.json de plantilla en el directorio del proyecto."""
        project_name = os.path.basename(project_path)
        config_data = {
            "name": f"Generated Add-In ({project_name})",
            "supportEmail": "edygohe@gmail.com",
            "version": "1.0.0",
            "items": [
                {
                    "url": f"https://<TU_USUARIO.github.io>/<TU_REPOSITORIO>/{project_name}/index.html",
                    "path": "Development/Generated",
                    "menuName": {
                        "en": f"Generated: {project_name}"
                    }
                }
            ],
            "isSigned": False
        }
        file_path = os.path.join(project_path, "config.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        print(f"   - Archivo creado: {file_path}")