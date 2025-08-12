geotab.addin.initialize = function (context) {
    // Obtener el elemento de la lista de vehículos
    const vehicleList = document.getElementById('vehicleList');
    const errorMessage = document.getElementById('error-message');

    // Función para obtener datos de vehículos (simulando la llamada a la API de Geotab)
    function getVehicles() {
        // Reemplazar con la llamada real a la API de Geotab
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const vehicles = [
                    { name: "Vehículo 1", id: "12345" },
                    { name: "Vehículo 2", id: "67890" },
                    { name: "Vehículo 3", id: "13579" },
                    { name: "Vehículo 4", id: "24680" },
                    { name: "Vehículo 5", id: "11223" }
                ];
                resolve(vehicles);
            }, 1000); // Simula un retraso de 1 segundo
        });
    }

    // Función para mostrar la lista de vehículos
    function displayVehicles(vehicles) {
        vehicleList.innerHTML = ''; // Limpiar la lista antes de actualizarla
        vehicles.forEach(vehicle => {
            const listItem = document.createElement('li');
            listItem.textContent = vehicle.name;
            listItem.dataset.vehicleId = vehicle.id; // Almacenar el ID en el dataset
            vehicleList.appendChild(listItem);
        });
    }

    // Manejo de errores
    function handleError(error) {
        errorMessage.textContent = "Error al obtener datos de vehículos: " + error.message;
        errorMessage.style.display = 'block';
    }

    // Delegación de eventos para la lista de vehículos
    vehicleList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const vehicleId = event.target.dataset.vehicleId;
            alert(`ID del Vehículo: ${vehicleId}`);
        }
    });

    // Obtener y mostrar los vehículos
    getVehicles()
        .then(displayVehicles)
        .catch(handleError);

    // (Opcional) Actualización periódica de datos
    // setInterval(() => {
    //     getVehicles()
    //         .then(displayVehicles)
    //         .catch(handleError);
    // }, 300000); // Actualizar cada 5 minutos (300000 milisegundos)
};