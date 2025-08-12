/* global geotab */

/**
 * @returns {object} The Add-In.
 */
geotab.addin.geotabGenesis = function () {
    'use strict';

    // Flag para asegurar que los event listeners se añadan solo una vez.
    let isInitialized = false;

    return {
        /**
         * Se llama una vez que el Add-In se ha cargado.
         * @param {object} api El objeto API de Geotab.
         * @param {object} state El estado guardado del Add-In.
         */
        initialize: function (api, state, callback) {
            // Llama al callback para indicar que la inicialización básica ha terminado.
            callback();
        },

        focus: function (api, state) {
            const userRequestTextArea = document.getElementById('userRequest');
            const generateButton = document.getElementById('generateButton');
            const loaderOverlay = document.getElementById('loader-overlay');
            const resultContainer = document.getElementById('result-container');
            const configOutput = document.getElementById('config-output');
            const copyButton = document.getElementById('copy-button');
            
            // Definimos la URL de la API aquí para que sea fácil de cambiar.
            const apiUrl = 'http://localhost:8000/generate-addin';

            if (!isInitialized) {
                generateButton.addEventListener('click', async function () {
                    const userPrompt = userRequestTextArea.value;
                    if (!userPrompt) {
                        alert('Por favor, describe el Add-In que quieres construir.');
                        return;
                    }

                    // Deshabilitamos el botón para evitar múltiples clics
                    userRequestTextArea.disabled = true;
                    generateButton.disabled = true;
                    loaderOverlay.classList.remove('hidden');
                    resultContainer.classList.add('hidden'); // Ocultar resultados anteriores
                    console.log('Enviando solicitud al backend:', userPrompt);

                    try {
                        const response = await fetch(apiUrl, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ prompt: userPrompt }),
                        });

                        if (!response.ok) {
                            // Captura errores HTTP como 500, 404, etc. que fetch no considera errores de red.
                            const errorText = await response.text();
                            throw new Error(`Error del servidor: ${response.status} ${response.statusText}. Detalles: ${errorText}`);
                        }

                        const result = await response.json();
                        console.log('Respuesta del backend:', result);

                        if (result.output && result.output.config_json && result.output.config_json.trim() !== '') {
                            const formattedJson = JSON.stringify(JSON.parse(result.output.config_json), null, 2);
                            configOutput.value = formattedJson;
                            resultContainer.classList.remove('hidden');
                            resultContainer.scrollIntoView({ behavior: 'smooth' });
                        } else {
                            alert(`Proceso finalizado. Estado: ${result.status || 'desconocido'}. Mensaje: ${result.message || 'Sin mensaje.'}`);
                        }
                    } catch (error) {
                        console.error('Error al contactar el backend:', error);
                        alert('Hubo un error al conectar con el servidor de generación. Asegúrate de que el servidor local esté corriendo.');
                    } finally {
                        // Volvemos a habilitar el botón al finalizar, tanto si hay éxito como si hay error
                        userRequestTextArea.disabled = false;
                        generateButton.disabled = false;
                        loaderOverlay.classList.add('hidden');
                    }
                });

                copyButton.addEventListener('click', function () {
                    navigator.clipboard.writeText(configOutput.value).then(() => {
                        const originalContent = copyButton.innerHTML;
                        copyButton.innerHTML = '✅';
                        copyButton.title = '¡Copiado!';
                        setTimeout(() => {
                            copyButton.innerHTML = originalContent;
                            copyButton.title = 'Copiar al portapapeles';
                        }, 2000);
                    }).catch(err => {
                        console.error('Error al copiar el JSON: ', err);
                    });
                });

                // Marcamos que la inicialización de los listeners ha terminado.
                isInitialized = true;
            }

            // Una vez que el Add-In tiene el foco, le pedimos a la API de Geotab
            // que traduzca todos los elementos que marcamos con data-i18n.
            // Esto reemplaza el texto hardcodeado con el del archivo es.json.
            if (api && typeof api.translate === 'function') {
                api.translate(document.getElementById('geotabAddin'));
            }
        }
    };
};
