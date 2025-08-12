geotab.addin.initialize = function(context) {
    // Inicialización del Add-In
    let vehiculos = []; // Array para almacenar datos de vehículos
    let mapa; // Variable para el objeto del mapa

    // Función para obtener datos de la API de Geotab (implementación simplificada)
    function obtenerDatos() {
        // Llamadas a la API de Geotab: /Get/Vehicles, /Get/Diagnostics, /Get/Device
        // ... (implementación de las llamadas a la API usando fetch o similar) ...
        // Ejemplo de datos simulados:
        vehiculos = [
            { id: 1, nombre: "Vehículo 1", estado: "Verde", latitud: 37.7749, longitud: -122.4194, fallos: [] },
            { id: 2, nombre: "Vehículo 2", estado: "Amarillo", latitud: 34.0522, longitud: -118.2437, fallos: [{ id: 101, descripcion: "Fallo de sensor", severidad: "Amarillo", fecha: "2024-10-27" }] },
            // ... más vehículos ...
        ];

        actualizarUI();
    }

    // Función para actualizar la interfaz de usuario
    function actualizarUI() {
        // Actualizar la tabla de vehículos
        let tbody = document.getElementById("tbodyVehiculos");
        tbody.innerHTML = ""; // Limpiar la tabla antes de actualizarla
        vehiculos.forEach(vehiculo => {
            let row = tbody.insertRow();
            let cell1 = row.insertCell();
            let cell2 = row.insertCell();
            let cell3 = row.insertCell();
            cell1.textContent = vehiculo.id;
            cell2.textContent = vehiculo.nombre;
            cell3.textContent = vehiculo.estado;
            // Agregar un listener de eventos para cada fila
            row.addEventListener('click', () => mostrarDetalles(vehiculo));
        });

        // Actualizar el mapa (implementación simplificada)
        // ... (implementación de la visualización del mapa usando una librería como Leaflet o Google Maps) ...

    }

    // Función para mostrar detalles del vehículo
    function mostrarDetalles(vehiculo) {
        let panel = document.getElementById("panelDetalles");
        panel.innerHTML = `<h2>Detalles de ${vehiculo.nombre}</h2>`;
        // ... (Mostrar detalles de fallos) ...
    }

    // Manejo del evento de clic en el botón "Actualizar"
    document.getElementById("btnActualizar").addEventListener("click", obtenerDatos);

    // Llamada inicial para obtener datos
    obtenerDatos();

    // Delegación de eventos para la tabla (se agrega al contenedor <tbody>)
    document.getElementById("tbodyVehiculos").addEventListener("click", function(event) {
        if (event.target.tagName === "TR") {
            let row = event.target;
            let vehiculoId = row.cells[0].textContent;
            // Obtener el vehículo correspondiente y mostrar sus detalles
            let vehiculo = vehiculos.find(v => v.id == vehiculoId);
            mostrarDetalles(vehiculo);
        }
    });
};