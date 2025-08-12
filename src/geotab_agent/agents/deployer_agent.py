import pathlib
import shutil
import json
import git
from .base_agent import BaseAgent
from geotab_agent.config import settings


class DeployerAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Deployer")
        self.repo_path = pathlib.Path(settings.GITHUB_ADDINS_REPO_PATH)

    def _copy_files(self, source_path: pathlib.Path, addin_name: str):
        """Copia los archivos del Add-In generado al repositorio local."""
        destination_path = self.repo_path / addin_name
        self.log(f"Copiando archivos de '{source_path}' a '{destination_path}'...")
        # Usamos dirs_exist_ok=True para sobreescribir si ya existe
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        self.log("Copia de archivos completada.")
        return destination_path

    def _update_config_url(self, addin_path: pathlib.Path, addin_name: str) -> str:
        """Actualiza la URL en el config.json para que apunte a la ruta de GitHub Pages."""
        config_file = addin_path / "config.json"
        if not config_file.is_file():
            self.log(f"ADVERTENCIA: No se encontró config.json en '{addin_path}'. No se puede actualizar la URL.", "warning")
            return ""
        
        self.log(f"Actualizando la URL en '{config_file}'...")
        final_url = f"{settings.GITHUB_PAGES_BASE_URL.rstrip('/')}/{addin_name}/index.html"
        
        with open(config_file, 'r+', encoding='utf-8') as f:
            config_data = json.load(f)
            config_data["items"][0]["url"] = final_url
            f.seek(0) # Rebobinar al principio del archivo
            json.dump(config_data, f, indent=2, ensure_ascii=False)
            f.truncate() # Eliminar contenido antiguo si el nuevo es más corto
        
        self.log(f"URL actualizada a: {final_url}")
        return json.dumps(config_data, indent=2, ensure_ascii=False)

    def _commit_and_push(self, addin_name: str):
        """Añade, confirma y sube los cambios al repositorio de GitHub usando un PAT."""
        try:
            repo = git.Repo(self.repo_path)
            
            # Añadir todos los cambios
            self.log(f"Añadiendo '{addin_name}' al área de preparación de Git...")
            repo.git.add(str(self.repo_path / addin_name))

            # Crear el commit
            commit_message = f"feat: Deploy new Add-In '{addin_name}'"
            self.log(f"Creando commit: \"{commit_message}\"")
            # Solo hacer commit si hay cambios
            if not repo.is_dirty(untracked_files=True):
                self.log("No hay cambios para confirmar. Saltando commit y push.")
                return {"deploy_status": "no_changes"}

            repo.index.commit(commit_message)

            # --- Lógica de Push Segura con PAT ---
            self.log("Haciendo push a origin usando el token de acceso personal...")
            
            # Construir la URL remota con el token
            # ej: https://<token>@github.com/usuario/repo.git
            remote_url = settings.GITHUB_REPO_URL
            push_url = remote_url.replace("https://", f"https://{settings.GITHUB_TOKEN}@")

            # Hacer push al origen usando la URL segura
            repo.git.push(push_url)
            
            self.log("Push a GitHub completado con éxito.")
            return {"deploy_status": "success"}
        except Exception as e:
            self.log(f"ERROR: Falló el despliegue con Git. {e}", "error")
            return {"deploy_status": "failed", "error": str(e)}

    def run(self, input_data: dict):
        self.log("Iniciando el proceso de despliegue automático.")
        source_path = pathlib.Path(input_data["source_path"])
        addin_name = source_path.name

        destination_path = self._copy_files(source_path, addin_name)
        updated_config_content = self._update_config_url(destination_path, addin_name)
        
        deploy_result = self._commit_and_push(addin_name)
        deploy_result["config_json"] = updated_config_content
        return deploy_result