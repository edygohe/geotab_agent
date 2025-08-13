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
        self.log("Recibió el diseño. Escribiendo archivos de código...")
        design_text = input_data.get("design", "")
        if not design_text:
            raise ValueError("El 'design' es requerido en los datos de entrada para el CoderAgent.")

        # Crear un directorio único para esta ejecución
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_path = os.path.join(self.output_dir, f"addin_{timestamp}")
        os.makedirs(project_path, exist_ok=True)

        # Parsear y escribir cada archivo
        html_success = self._write_file_from_block(design_text, ["html"], "index.html", project_path)
        self._write_file_from_block(design_text, ["css"], "style.css", project_path)
        js_success = self._write_file_from_block(design_text, ["javascript", "js"], "script.js", project_path)
        self._write_localization_files(project_path)
        self._write_config_json(project_path)

        # Si no se pudieron crear los archivos esenciales, se considera un fallo.
        if not (html_success and js_success):
            self.log("No se pudieron generar los archivos esenciales (HTML/JS) a partir de la respuesta del LLM. La codificación ha fallado.", "error")
            # Devolvemos un diccionario vacío para indicar el fallo al orquestador.
            return {}

        self.log(f"Código generado con éxito en: {project_path}")
        return {"code_path": project_path}

    def _write_file_from_block(self, text: str, lang_aliases: list[str], filename: str, path: str) -> bool:
        """Extrae un bloque de código y lo escribe. Devuelve True si tiene éxito, False si no."""
        for lang in lang_aliases:
            # La expresión regular busca el alias del lenguaje, ignorando mayúsculas/minúsculas,
            # seguido de una nueva línea, y captura todo hasta los tres backticks de cierre.
            # Esto es más robusto ante espacios o caracteres extra después del alias.
            pattern = re.compile(rf"```{lang}[^\n]*\n(.*?)\n```", re.IGNORECASE | re.DOTALL)
            match = pattern.search(text)
            if match:
                # Usamos lstrip() para quitar espacios/líneas en blanco al principio, pero no al final.
                code = match.group(1).lstrip()
                file_path = os.path.join(path, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                self.log(f"Archivo creado: {file_path}", "info")
                return True  # Éxito
        # Si el bucle termina sin encontrar nada
        self.log(f"No se encontró bloque de código para '{filename}' (alias probados: {lang_aliases}).", "warning")
        return False # Fallo

    def _write_localization_files(self, project_path: str):
        """Crea la estructura de carpetas y archivos básicos para la localización."""
        translations_dir = os.path.join(project_path, "translations")
        os.makedirs(translations_dir, exist_ok=True)
        
        # Crear un archivo de traducción en español vacío.
        es_json_path = os.path.join(translations_dir, "es.json")
        with open(es_json_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        self.log(f"Archivo de localización base creado: {es_json_path}", "info")

    def _write_config_json(self, project_path: str):
        """Crea un archivo config.json de plantilla en el directorio del proyecto."""
        project_name = os.path.basename(project_path)
        config_data = {
            "name": f"Generated Add-In ({project_name})",
            "supportEmail": "edygohe@gmail.com",
            "version": "1.0.0",
            "translator": "translations/",
            "items": [
                {
                    "url": f"https://<TU_USUARIO.github.io>/<TU_REPOSITORIO>/{project_name}/index.html",
                    "path": "Map/Generated",
                    "menuName": { "en": f"Generated: {project_name}" }
                }
            ],
            "isSigned": False
        }
        file_path = os.path.join(project_path, "config.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        self.log(f"Archivo creado: {file_path}", "info")
