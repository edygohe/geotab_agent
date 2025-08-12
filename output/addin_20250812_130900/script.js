geotab.addin.initialize = function(context) {
    // Inicialización del Add-In
    let vehicles = [];
    let selectedVehicle = null;
    let map = null;

    // Funciones para obtener datos de la API de Geotab (implementación pendiente)
    function getVehicles() { /* ... */ }
    function getFaults(vehicleId) { /* ... */ }
    function getLocation(vehicleId) { /* ... */ }

    function updateUI() { /* ... */ }

    function handleError(error) {
        document.getElementById('errorMessages').textContent = error.message;
    }

    // Evento de clic en el botón "Actualizar"
    document.getElementById('updateButton').addEventListener('click', () => {
        getVehicles();
    });

    // Inicialización
    getVehicles().then(updateUI).catch(handleError);

    // ... Resto de la lógica JavaScript (manejo de eventos, actualización de la UI, etc.) ...
};