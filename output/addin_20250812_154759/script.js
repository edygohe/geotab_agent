geotab.addin.initialize = function (context) {
    let vehiculos = [];
    let panelIzquierdo = document.getElementById('panelIzquierdo');
    let panelDerecho = document.getElementById('panelDerecho');
    let btnActualizar = document.getElementById('btnActualizar');

    // Función para obtener la lista de vehículos
    function obtenerVehiculos() {
        // Llamada a la API de Geotab /Get/Vehicles
        // ... (implementación de la llamada a la API) ...
        // Ejemplo de datos de retorno (reemplazar con la respuesta real de la API)
        vehiculos = [
            { id: 1, name: 'Vehículo 1' },
            { id: 2, name: 'Vehículo 2' },
            // ... más vehículos
        ];
        actualizarUI();
    }

    // Función para obtener información de fallos
    function obtenerFallos(idVehiculo) {
        // Llamada a la API de Geotab /Get/Diagnostics
        // ... (implementación de la llamada a la API) ...
        // Ejemplo de datos de retorno (reemplazar con la respuesta real de la API)
        return [
            { codigo: 'F001', severidad: 'critico', descripcion: 'Fallo crítico', fecha: '2024-10-27 10:00' },
            // ... más fallos
        ];
    }

    // Función para actualizar la interfaz de usuario
    function actualizarUI() {
        panelIzquierdo.innerHTML = '';
        vehiculos.forEach(vehiculo => {
            let estado = obtenerEstado(vehiculo.id);
            let elementoVehiculo = document.createElement('div');
            elementoVehiculo.classList.add('vehiculo');
            elementoVehiculo.innerHTML = `<div class="estado estado-${estado}"></div> ${vehiculo.name}`;
            elementoVehiculo.addEventListener('click', () => mostrarDetalles(vehiculo.id));
            panelIzquierdo.appendChild(elementoVehiculo);
        });
    }

    // Función para obtener el estado del vehículo
    function obtenerEstado(idVehiculo) {
        let fallos = obtenerFallos(idVehiculo);
        if (fallos.some(fallo => fallo.severidad === 'critico' || fallo.severidad === 'alto')) return 'critico';
        if (fallos.some(fallo => fallo.severidad === 'medio')) return 'medio';
        return 'bajo';
    }

    // Función para mostrar los detalles de los fallos
    function mostrarDetalles(idVehiculo) {
        let fallos = obtenerFallos(idVehiculo);
        let tabla = `<table><thead><tr><th>Código</th><th>Severidad</th><th>Descripción</th><th>Fecha y Hora</th></tr></thead><tbody>`;
        fallos.forEach(fallo => {
            tabla += `<tr><td>${fallo.codigo}</td><td>${fallo.severidad}</td><td>${fallo.descripcion}</td><td>${fallo.fecha}</td></tr>`;
        });
        tabla += `</tbody></table>`;
        panelDerecho.innerHTML = tabla;
    }

    obtenerVehiculos();
    btnActualizar.addEventListener('click', obtenerVehiculos);
};