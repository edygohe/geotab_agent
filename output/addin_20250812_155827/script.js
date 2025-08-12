geotab.addin.initialize = function (context) {
    // Obtener el elemento de la lista de vehículos
    const vehicleList = document.getElementById('vehicleList');
    const errorMessage = document.getElementById('error-message');

    // Manejo de errores
    const handleError = (error) => {
        errorMessage.textContent = `Error: ${error.message}`;
        errorMessage.style.display = 'block';
    };

    // Función para obtener los 5 primeros vehículos (implementación simplificada, se necesita adaptar a la API de Geotab)
    const getVehicles = async () => {
        try {
            // Reemplazar con la llamada real a la API de Geotab
            const response = await fetch('/api/vehicles?limit=5'); // Ejemplo, ajustar según la API
            if (!response.ok) {
                throw new Error(`Error de red: ${response.status}`);
            }
            const data = await response.json();
            if (!data || !data.vehicles) {
                throw new Error('Datos inválidos de la API');
            }
            return data.vehicles;
        } catch (error) {
            handleError(error);
            return [];
        }
    };

    // Función para mostrar la lista de vehículos
    const displayVehicles = (vehicles) => {
        vehicleList.innerHTML = ''; // Limpiar la lista antes de actualizarla
        vehicles.forEach(vehicle => {
            const listItem = document.createElement('li');
            listItem.textContent = vehicle.name;
            listItem.dataset.vehicleId = vehicle.id; // Almacenar el ID en el dataset
            vehicleList.appendChild(listItem);
        });
    };

    // Delegación de eventos para clicks en la lista
    vehicleList.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            const vehicleId = event.target.dataset.vehicleId;
            alert(`El ID del vehículo seleccionado es: ${vehicleId}`);
        }
    });

    // Obtener y mostrar los vehículos al inicializar el Add-In
    getVehicles().then(displayVehicles);
};