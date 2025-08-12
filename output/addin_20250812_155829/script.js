geotab.addin.initialize = function (context) {
    // Obtener los datos de los vehículos desde la API de Geotab
    fetchVehicles().then(vehicles => {
        displayVehicles(vehicles);
        setupEventListeners();
    }).catch(error => {
        displayError(error);
    });
};

function fetchVehicles() {
    // Reemplazar con la llamada real a la API de Geotab
    // Ejemplo (adaptar a la API real):
    return fetch('/api/vehicles?limit=5&orderBy=id')
        .then(response => response.json())
        .then(data => data.vehicles || []); // Manejar casos donde no hay vehículos
}

function displayVehicles(vehicles) {
    const vehicleList = document.getElementById('vehicleList');
    vehicleList.innerHTML = ''; // Limpiar la lista antes de actualizarla

    vehicles.forEach(vehicle => {
        const listItem = document.createElement('li');
        listItem.textContent = vehicle.name;
        listItem.dataset.vehicleId = vehicle.id; // Almacenar el ID en el dataset
        vehicleList.appendChild(listItem);
    });
}

function setupEventListeners() {
    const vehicleList = document.getElementById('vehicleList');
    vehicleList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const vehicleId = event.target.dataset.vehicleId;
            displayVehicleDetails(vehicleId);
        }
    });

    const modalCloseButton = document.querySelector('.close');
    modalCloseButton.addEventListener('click', closeModal);
}

function displayVehicleDetails(vehicleId) {
    const modal = document.getElementById('vehicleDetailsModal');
    const vehicleIdElement = document.getElementById('vehicleId');
    vehicleIdElement.textContent = vehicleId;
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('vehicleDetailsModal');
    modal.style.display = 'none';
}

function displayError(error) {
    // Mostrar un mensaje de error al usuario (ej. alert, modal, etc.)
    alert(`Error al obtener los datos de los vehículos: ${error}`);
}