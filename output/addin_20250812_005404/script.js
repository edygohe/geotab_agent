geotab.addin.initialize = function(context) {
    // Verificar si el popup ya se ha mostrado en esta sesión.
    let hasShownPopup = localStorage.getItem('geotabGenesisPopupShown');

    if (!hasShownPopup) {
        // Mostrar el popup
        const modal = document.getElementById('modal');
        modal.classList.remove('hidden');

        // Agregar evento de cierre al botón
        const closeButton = document.getElementById('closeModal');
        closeButton.addEventListener('click', () => {
            modal.classList.add('hidden');
            localStorage.setItem('geotabGenesisPopupShown', 'true');
        });

        // Manejo de errores (ejemplo)
        try {
            // Aquí iría cualquier lógica adicional que requiera la API de Geotab.
            console.log("Add-in inicializado correctamente.");
        } catch (error) {
            // Mostrar mensaje de error al usuario (implementar una mejor forma de mostrar errores)
            alert("Error al inicializar el Add-in: " + error.message);
        }
    }
};

// Manejo de eventos adicionales (opcional)
geotab.addin.onLogout = function() {
    // Limpiar el almacenamiento local al cerrar sesión.
    localStorage.removeItem('geotabGenesisPopupShown');
};