geotab.addin.initialize = function(context) {
    // Obtener el elemento donde se mostrará el mensaje
    const messageElement = document.getElementById('helloMessage');

    // Mostrar el mensaje
    messageElement.textContent = "Hola Mundo Geotab";

    // Ejemplo de acceso a datos de Geotab (para futuras expansiones)
    //  const myData = context.getData();
    //  console.log(myData);

    // Manejo de eventos (para futuras expansiones)
    //  geotab.addin.addEventListener('event', function(eventData) {
    //      console.log(eventData);
    //  });
};