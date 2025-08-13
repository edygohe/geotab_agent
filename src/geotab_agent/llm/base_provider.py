import abc

class BaseLLMProvider(abc.ABC):
    """
    Clase base abstracta para cualquier proveedor de modelos de lenguaje.
    Define la interfaz común para generar contenido.
    """

    @abc.abstractmethod
    def generate_content(self, prompt: str) -> str:
        """Toma un prompt y devuelve la respuesta del modelo como una cadena de texto."""
        pass