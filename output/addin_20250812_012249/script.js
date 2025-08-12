geotab.addin.initialize = function (context) {
    // Inicialización del Add-In
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const vehicleIdInput = document.getElementById('vehicleId');
    const damageTypeSelect = document.getElementById('damageType');
    const searchButton = document.getElementById('searchButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');
    const vehicleTable = document.getElementById('vehicleTable');

    // Obtener tipos de daño de la configuración (implementación pendiente)
    const damageTypes = getDamageTypesFromConfig();
    populateDamageTypeSelect(damageTypes);

    searchButton.addEventListener('click', () => {
        errorMessage.textContent = '';
        loadingIndicator.style.display = 'block';
        const filters = getFilters();
        fetchDamagedVehicles(filters)
            .then(vehicles => displayVehicles(vehicles))
            .catch(error => handleError(error))
            .finally(() => loadingIndicator.style.display = 'none');
    });

    // Funciones auxiliares (implementación pendiente):
    function getDamageTypesFromConfig() {
        // Obtener la lista de tipos de daño de la configuración del Add-In
        // ...
        return ["Colisión", "Avería Mecánica", "Daño Eléctrico"];
    }

    function populateDamageTypeSelect(damageTypes) {
        damageTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.text = type;
            damageTypeSelect.add(option);
        });
    }

    function getFilters() {
        // Obtener los filtros del usuario
        // ...
        return {
            startDate: startDateInput.value,
            endDate: endDateInput.value,
            vehicleId: vehicleIdInput.value,
            damageType: damageTypeSelect.value
        };
    }

    function fetchDamagedVehicles(filters) {
        // Consultar la API de Geotab con los filtros
        // ...
        return new Promise((resolve, reject) => {
            // Simulación de la llamada a la API
            setTimeout(() => {
                const simulatedData = [
                    {vehicleId: '123', date: '2024-03-08', description: 'Choque frontal', location: '34.0522,-118.2437', damageType: 'Colisión'},
                    {vehicleId: '456', date: '2024-03-15', description: 'Fallo en el motor', location: '37.7749,-122.4194', damageType: 'Avería Mecánica'}
                ];
                resolve(simulatedData);
            }, 1000);
        });
    }

    function displayVehicles(vehicles) {
        // Mostrar los vehículos en la tabla
        // ...
        const tbody = vehicleTable.querySelector('tbody');
        tbody.innerHTML = '';
        vehicles.forEach(vehicle => {
            const row = tbody.insertRow();
            row.insertCell().textContent = vehicle.vehicleId;
            row.insertCell().textContent = vehicle.date;
            row.insertCell().textContent = vehicle.description;
            row.insertCell().textContent = vehicle.location;
            row.insertCell().textContent = vehicle.damageType;
        });
    }

    function handleError(error) {
        // Manejar los errores
        // ...
        errorMessage.textContent = 'Error al obtener los datos: ' + error.message;
    }
};