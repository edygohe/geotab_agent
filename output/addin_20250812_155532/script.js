geotab.addin.initialize = function (context) {
    // Inicialización del mapa (se asume el uso de una librería como Leaflet o Google Maps)
    // ...

    // Obtener la lista de vehículos
    getVehicles().then(vehicles => {
        displayVehicles(vehicles);
    });

    // Delegación de eventos para la lista de vehículos
    document.getElementById('vehicleList').addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const vehicleId = event.target.dataset.vehicleId;
            showVehicleDetails(vehicleId);
        }
    });

    // Evento para el botón actualizar
    document.getElementById('updateButton').addEventListener('click', () => {
        getVehicles().then(vehicles => {
            displayVehicles(vehicles);
        });
    });
};


// Funciones auxiliares (ejemplos)
async function getVehicles() {
    // Llamada a la API de Geotab para obtener la lista de vehículos
    // ...  Reemplazar con la llamada real a la API
    return [
        { id: 1, name: "Vehículo 1", faults: [{severity: "high"}, {severity: "low"}] },
        { id: 2, name: "Vehículo 2", faults: [] },
        { id: 3, name: "Vehículo 3", faults: [{severity: "medium"}] }
    ];
}

function displayVehicles(vehicles) {
    const vehicleList = document.getElementById('vehicleList');
    vehicleList.innerHTML = ''; // Limpiar la lista antes de actualizarla

    vehicles.forEach(vehicle => {
        const li = document.createElement('li');
        li.dataset.vehicleId = vehicle.id;
        li.textContent = vehicle.name;
        li.classList.add(getSeverityClass(vehicle.faults));
        vehicleList.appendChild(li);
    });
}

function getSeverityClass(faults) {
    if (faults.some(fault => fault.severity === "high")) return "high";
    if (faults.some(fault => fault.severity === "medium")) return "medium";
    return "low";
}

async function showVehicleDetails(vehicleId) {
    // Llamada a la API para obtener detalles de fallos y ubicación
    // ...
    // Actualizar la tabla #faultDetailsTable y el mapa
}