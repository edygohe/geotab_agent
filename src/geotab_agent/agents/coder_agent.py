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
        self._write_file_from_block(design_text, ["html"], "index.html", project_path)
        self._write_file_from_block(design_text, ["css"], "style.css", project_path)
        self._write_file_from_block(design_text, ["javascript", "js"], "script.js", project_path)
        self._write_file_from_block(design_text, ["json"], "config.json", project_path)

        self.log(f"Código generado con éxito en: {project_path}")
        return {"code_path": project_path}

    def _write_file_from_block(self, text: str, lang_aliases: list[str], filename: str, path: str):
        """Extrae un bloque de código markdown y lo escribe en un archivo, probando varios alias de lenguaje."""
        for lang in lang_aliases:
            # La expresión regular busca el alias del lenguaje, ignorando mayúsculas/minúsculas,
            # seguido de una nueva línea, y captura todo hasta los tres backticks de cierre.
            # Esto es más robusto ante espacios o caracteres extra después del alias.
            pattern = re.compile(rf"```{lang}[^\n]*\n(.*?)\n```", re.IGNORECASE | re.DOTALL)
            match = pattern.search(text)
            if match:
                code = match.group(1).strip()
                file_path = os.path.join(path, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                self.log(f"Archivo creado: {file_path}", "info")
                return  # Salimos en cuanto encontramos una coincidencia
        # Si el bucle termina sin encontrar nada
        self.log(f"No se encontró bloque de código para '{filename}' (alias probados: {lang_aliases}).", "warning")