geotab.addin.initialize = function(context) {
    // Verificar la disponibilidad de la API de Geotab (para futuras expansiones)
    console.log("Geotab API version:", context.version);

    // Mostrar el mensaje "Hola Edgar!"
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = "Hola Edgar!";

    //Consideraciones para el cierre del mensaje (opcional, no implementado en esta versión)
    //Se podría agregar un botón o un temporizador para ocultar el mensaje después de un tiempo.
};