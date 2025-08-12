geotab.addin.initialize = function(context) {
    try {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = "Hola Mundo Geotab";
    } catch (error) {
        const errorMessageDiv = document.getElementById('error-message');
        errorMessageDiv.textContent = "Error al cargar el Add-In: " + error.message;
        errorMessageDiv.style.display = "block";
        console.error("Error in geotab.addin.initialize:", error);
    }
};


//Función opcional para manejar eventos de Geotab (ej. cambio de selección de vehículo)
geotab.addin.onSelectionChanged = function(selection) {
    //Aquí se podría implementar lógica para actualizar el mensaje basado en la selección
    console.log("Selección cambiada:", selection);
};

//Función opcional para manejar eventos de Geotab (ej. cierre de sesión)
geotab.addin.onLogout = function() {
    //Aquí se podría implementar lógica para limpiar recursos o cerrar sesión
    console.log("Usuario cerró sesión");
};