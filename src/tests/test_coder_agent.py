from unittest.mock import patch, mock_open
from geotab_agent.agents import CoderAgent
import pytest
import os

def test_coder_agent_run():
    """
    Prueba que el CoderAgent parsea el diseño y escribe los archivos correctamente.
    """
    # 1. Preparación (Arrange)
    design_text = """
    Aquí hay algo de texto.

    ```html
    <h1>Hola Mundo</h1>
    ```

    Más texto.

    ```css
    h1 { color: blue; }
    ```

    ```javascript
    console.log("Hola");
    ```
    """
    input_data = {"design": design_text}

    # Mockeamos las llamadas al sistema de archivos
    with patch("os.makedirs") as mock_makedirs, \
         patch("builtins.open", mock_open()) as mock_file:

        coder = CoderAgent(output_dir="test_output")

        # 2. Actuación (Act)
        result = coder.run(input_data=input_data)

        # 3. Aserción (Assert)
        assert mock_makedirs.call_count >= 1
        project_path = mock_makedirs.call_args_list[1][0][0]
        assert "addin_" in os.path.basename(project_path)

        mock_file.assert_any_call(os.path.join(project_path, "index.html"), "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_any_call("<h1>Hola Mundo</h1>")

        assert "code_path" in result
        assert result["code_path"] == project_path

def test_coder_agent_run_no_design():
    """Prueba que el CoderAgent lanza un error si no hay diseño."""
    coder = CoderAgent()
    with pytest.raises(ValueError, match="El 'design' es requerido"):
        coder.run(input_data={})