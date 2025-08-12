geotab.addin.initialize = function(context) {
    try {
        // Mostrar el popup después de un pequeño retraso para asegurar que el DOM esté listo
        setTimeout(function() {
            document.getElementById('popup').classList.add('show');
        }, 100);

        // Cerrar el popup automáticamente después de 5 segundos
        setTimeout(function() {
            document.getElementById('popup').classList.remove('show');
        }, 5000);

        // Manejo del cierre manual (opcional)
        document.getElementById('popup-close').addEventListener('click', function() {
            document.getElementById('popup').classList.remove('show');
        });

    } catch (error) {
        // Manejo de errores
        console.error("Error al inicializar el Add-in:", error);
        // Mostrar un mensaje de error al usuario (implementar una forma adecuada de mostrar mensajes de error en la interfaz)
        alert("Error al mostrar el mensaje. Por favor, contacte al administrador.");
    }
};