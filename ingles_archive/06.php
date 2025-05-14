<!DOCTYPE html>
<html lang="es" data-theme="light">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversor CSV/TXT a SSML con PHP</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css">
    <style>
        /* Estilos de la respuesta anterior (CSS Grid, etc.) */
        details>summary {
            cursor: pointer;
            list-style: revert;
        }

        details article {
            padding: 1em 0 0 1.5em;
            border-left: 2px solid var(--pico-muted-border-color);
            margin-left: 0.5em;
        }

        textarea {
            min-height: 150px;
            resize: vertical;
        }

        table {
            font-size: 0.9em;
        }

        table th {
            white-space: normal;
        }

        .error-text {
            color: var(--pico-form-element-invalid-active-border-color);
        }

        #mainConfigSection article {
            display: grid;
            grid-template-columns: 1fr;
            gap: var(--pico-spacing);
        }

        #csvOptionsFieldset .options-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--pico-form-element-spacing-horizontal);
            align-items: end;
        }

        #csvOptionsFieldset .checkbox-group {
            display: flex;
            flex-direction: column;
            gap: calc(var(--pico-form-element-spacing-vertical) / 1.5);
            margin-top: var(--pico-form-element-spacing-vertical);
        }

        .voice-config-item {
            display: grid;
            grid-template-columns: 1fr;
            gap: calc(var(--pico-form-element-spacing-vertical) / 2);
            padding: var(--pico-block-spacing-vertical) var(--pico-block-spacing-horizontal);
            border: 1px solid var(--pico-form-element-border-color);
            border-radius: var(--pico-border-radius);
            margin-bottom: var(--pico-spacing);
        }

        .voice-config-item label:not(:first-child) {
            margin-top: 0.5rem;
        }

        .voice-config-item .rate-label-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .voice-config-item .rate-display {
            font-weight: bold;
            min-width: 2.5em;
            text-align: right;
        }

        .voice-config-item input[type="range"] {
            width: 100%;
        }

        /* Para feedback de audio */
        #audioLinkContainer a {
            margin-left: 10px;
            font-weight: bold;
        }
    </style>
</head>

<body>
    <main>
        <header>
            <h1>{{ mainTitle }}</h1>
            <p>Herramienta para generar SSML y audio desde CSV/TXT con PHP y CLI.</p>
        </header>

        <div id="app">
            <section id="mainConfigSection">
                <article>
                    <div role="group">
                        <label for="fileInput">
                            1. Seleccionar archivo CSV/TXT:
                            <input type="file" id="fileInput" @change="handleFileUpload" accept=".csv,.txt">
                        </label>
                        <small>Archivo: {{ fileName || 'Ninguno' }}</small>
                    </div>

                    <fieldset id="csvOptionsFieldset">
                        <legend>2. Opciones de CSV/TXT y Datos</legend>
                        <div class="options-group">
                            <div>
                                <label for="separator">Separador (Detectado: {{ autoDetectedSeparatorSymbol }}):</label>
                                <select id="separator" v-model="csvOptions.separator">
                                    <option value=",">Coma (,)</option>
                                    <option value=";">Punto y coma (;)</option>
                                    <option value="\t">Tabulador (Tab)</option>
                                    <option value="|">Pipe (|)</option>
                                </select>
                            </div>
                            <div class="checkbox-group">
                                <label for="shuffleRows">
                                    <input type="checkbox" id="shuffleRows" v-model="csvOptions.shuffleRows" role="switch">
                                    Desordenar filas
                                </label>
                                <label for="invertColumns">
                                    <input type="checkbox" id="invertColumns" v-model="csvOptions.invertColumns" role="switch">
                                    Invertir Col. 1 y 2
                                </label>
                            </div>
                        </div>
                    </fieldset>
                </article>
            </section>

            <section>
                <fieldset id="sapiVoicesFieldset">
                    <legend>3. Selección y Configuración de Voces SAPI</legend>
                    <p><small>Selecciona las voces (cargadas desde el servidor) y ajusta su velocidad.</small></p>

                    <div class="grid">
                        <div v-for="(voiceConfig, index) in sapiVoices" :key="index">
                            <div class="voice-config-item">
                                <label :for="'voice' + index + 'Name'">Voz para Posición {{ index + 1 }}:</label>
                                <select :id="'voice' + index + 'Name'" v-model="voiceConfig.name">
                                    <option disabled value="">Seleccione una voz</option>
                                    <option v-for="voice in availableVoices" :key="voice.id" :value="voice.id">{{ voice.name }}</option>
                                </select>

                                <div class="rate-label-container">
                                    <label :for="'voice' + index + 'Rate'">Velocidad Voz {{ index + 1 }}:</label>
                                    <span class="rate-display">{{ voiceConfig.rate }}</span>
                                </div>
                                <input type="range" :id="'voice' + index + 'Rate'" min="-10" max="10" v-model.number="voiceConfig.rate">
                            </div>
                        </div>
                    </div>
                </fieldset>
            </section>

            <section>
                <h4>4. Vistas Previas</h4>
                <details open id="tablePreviewDetails">
                    <summary>Datos (Tabla)</summary>
                    <article>
                        <div v-if="csvPreview.displayRows.length > 0 || csvPreview.displayHeaders.length > 0" style="overflow-x: auto;">
                            <table>
                                <thead>
                                    <tr>
                                        <th v-for="(header, hIndex) in csvPreview.displayHeaders" :key="'header-' + hIndex" v-html="header"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(row, rIndex) in csvPreview.displayRows.slice(0, csvPreview.maxPreviewRows)" :key="'row-' + rIndex">
                                        <td v-for="(cell, cIndex) in row" :key="'cell-' + rIndex + '-' + cIndex">{{ cell }}</td>
                                    </tr>
                                </tbody>
                            </table>
                            <p v-if="csvPreview.displayRows.length > csvPreview.maxPreviewRows">
                                <small>Mostrando primeras {{ csvPreview.maxPreviewRows }} filas de {{ csvPreview.displayRows.length }}.</small>
                            </p>
                        </div>
                        <p v-else-if="fileName && !csvPreview.parseError"><small>Ajusta el separador o verifica el contenido del archivo.</small></p>
                        <p v-else-if="csvPreview.parseError"><small class="error-text">Error al parsear: {{ csvPreview.parseError }}. Verifica el separador y el archivo.</small></p>
                        <p v-else><small>Carga un archivo CSV/TXT para ver la vista previa.</small></p>
                    </article>
                </details>

                <details id="ssmlPreviewDetails">
                    <summary>SSML Generado</summary>
                    <article>
                        <textarea readonly v-model="generatedSSMLText" placeholder="El SSML generado aparecerá aquí..."></textarea>
                    </article>
                </details>
            </section>

            <footer>
                <button @click="processAndGenerateAudio" :disabled="!selectedFile || isLoadingAudio">
                    <span v-if="isLoadingAudio" aria-busy="true">Procesando audio…</span>
                    <span v-else>Generar SSML y Audio</span>
                </button>
                <p><small>{{ statusMessage }}</small><span id="audioLinkContainer"></span></p>
            </footer>
        </div>
    </main>

    <script>
        <?php
        $command = 'balcon -l';
        $output = [];
        $return_var = 0;

        exec($command, $output, $return_var);

        // Si el comando falla, usar valores por defecto
        if ($return_var !== 0 || empty($output)) {
            $output = [
                "Microsoft David Desktop",
                "Microsoft Helena Desktop",
                "Microsoft Zira Desktop"
            ];
        }

        // Mapear las voces al formato esperado por el frontend
        $voices = [];
        foreach ($output as $voice) {
            $voice = trim($voice);
            if (empty($voice)) continue;

            // Generar ID en formato slug (minusculas, guiones)
            $id = strtolower(str_replace(' ', '-', $voice));

            $voices[] = [
                'id' => $id,
                'name' => $voice // Mantenemos el nombre original para mostrar
            ];
        }
        ?>



        // ESTA VARIABLE SERÍA GENERADA POR PHP:
        const serverProvidedVoices = <?php echo json_encode($output) ?>;
    </script>

    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

    <script>
        const {
            createApp,
            ref,
            reactive,
            computed
        } = Vue;

        createApp({
            data() {
                return {
                    mainTitle: 'Conversor CSV/TXT a SSML y Audio',
                    selectedFile: null,
                    fileContentCache: '',
                    parsedRawRows: [],
                    fileName: '',
                    autoDetectedSeparator: '', // Almacena el separador detectado
                    csvOptions: {
                        separator: ',', // Valor por defecto, se actualizará con la detección
                        shuffleRows: false,
                        invertColumns: false,
                    },
                    sapiVoices: [{
                            name: '',
                            rate: 0
                        },
                        {
                            name: '',
                            rate: 0
                        }
                    ],
                    availableVoices: serverProvidedVoices, // Usar las voces del servidor
                    csvPreview: {
                        originalFileHeaders: [],
                        displayHeaders: [],
                        displayRows: [],
                        maxPreviewRows: 20,
                        parseError: ''
                    },
                    generatedSSMLText: '',
                    statusMessage: 'Listo. Cargue un archivo para comenzar.',
                    isLoadingAudio: false,
                }
            },
            computed: {
                autoDetectedSeparatorSymbol() {
                    if (this.autoDetectedSeparator === '\t') return 'Tab';
                    if (this.autoDetectedSeparator === ',') return 'Coma (,)';
                    if (this.autoDetectedSeparator === ';') return 'Punto y Coma (;)';
                    if (this.autoDetectedSeparator === '|') return 'Pipe (|)';
                    return 'N/A';
                }
            },
            methods: {
                // ... (métodos de la respuesta anterior: clearAllProcessedData, parseFileAndPreparePreview, refreshTablePreview, updateDisplayHeaders, getVoiceDisplayName, escapeXml, escapeHtml, triggerSSMLClearAndAdviseRegenerate) ...
                // COPIA LOS MÉTODOS DE LA RESPUESTA ANTERIOR AQUÍ, LUEGO MODIFICA/AÑADE:

                handleFileUpload(event) {
                    this.selectedFile = event.target.files[0];
                    this.clearAllProcessedData();
                    document.getElementById('audioLinkContainer').innerHTML = ''; // Limpiar enlace de audio

                    if (this.selectedFile) {
                        this.fileName = this.selectedFile.name;
                        this.statusMessage = 'Archivo cargado. Procesando...';

                        const reader = new FileReader();
                        reader.onload = (e) => {
                            this.fileContentCache = e.target.result;
                            // --- Detección de separador ---
                            this.autoDetectedSeparator = this.detectBestSeparator(this.fileContentCache.substring(0, 5000)); // Analizar primeros 5KB
                            if (this.autoDetectedSeparator) {
                                this.csvOptions.separator = this.autoDetectedSeparator;
                            }
                            // --- Fin Detección ---
                            this.parseFileAndPreparePreview();
                        };
                        reader.onerror = (e) => {
                            this.statusMessage = 'Error al leer el archivo.';
                            console.error("Error de lectura:", e);
                            this.fileContentCache = '';
                        };
                        reader.readAsText(this.selectedFile);
                    } else {
                        this.fileName = '';
                        this.fileContentCache = '';
                        this.statusMessage = 'Ningún archivo seleccionado.';
                    }
                },

                detectBestSeparator(textBlock) {
                    const separators = [{
                            char: ',',
                            count: 0,
                            name: 'Coma'
                        },
                        {
                            char: ';',
                            count: 0,
                            name: 'Punto y Coma'
                        },
                        {
                            char: '|',
                            count: 0,
                            name: 'Pipe'
                        },
                        {
                            char: '\t',
                            count: 0,
                            name: 'Tabulador'
                        }
                    ];

                    if (!textBlock) return null;

                    // Contar ocurrencias de cada separador en las primeras N líneas (ej. 10)
                    const lines = textBlock.split('\n').slice(0, 10);
                    lines.forEach(line => {
                        separators.forEach(sep => {
                            sep.count += (line.split(sep.char).length - 1);
                        });
                    });

                    // Encontrar el separador con más ocurrencias, pero solo si tiene un conteo significativo
                    separators.sort((a, b) => b.count - a.count);

                    if (separators[0].count > 0 && separators[0].count > (separators[1] ? separators[1].count : -1)) {
                        // Evitar falsos positivos si hay muchos de un caracter que no es separador en una sola línea.
                        // Podríamos añadir lógica para verificar que el separador aparece consistentemente en varias líneas.
                        // Por ahora, el de mayor conteo es suficiente si > 0.
                        return separators[0].char;
                    }
                    return null; // O devolver el default ','
                },

                clearAllProcessedData() {
                    this.parsedRawRows = [];
                    this.csvPreview.originalFileHeaders = [];
                    this.csvPreview.displayHeaders = [];
                    this.csvPreview.displayRows = [];
                    this.csvPreview.parseError = '';
                    this.generatedSSMLText = '';
                    this.autoDetectedSeparator = ''; // Resetear separador detectado
                    document.getElementById('audioLinkContainer').innerHTML = '';
                },

                parseFileAndPreparePreview() { // (Mantener como antes, pero asegurar que se llama DESPUÉS de detectar separador)
                    if (!this.fileContentCache) {
                        this.statusMessage = this.selectedFile ? 'Contenido no disponible.' : 'Carga un archivo.';
                        this.clearAllProcessedData();
                        return;
                    }
                    this.statusMessage = 'Analizando archivo y actualizando vista previa...';
                    if (this.generatedSSMLText && !this.isLoadingAudio) { // No limpiar si se está cargando audio
                        this.generatedSSMLText = '';
                        this.statusMessage = 'Fuente de datos cambiada. El SSML ha sido limpiado, por favor regenere.';
                    }

                    Papa.parse(this.fileContentCache, {
                        delimiter: this.csvOptions.separator, // Usar el separador (auto o manual)
                        header: false,
                        skipEmptyLines: true,
                        complete: (results) => {
                            this.csvPreview.parseError = '';
                            if (results.errors.length > 0) {
                                console.error("Errores de parseo:", results.errors);
                                this.csvPreview.parseError = results.errors.map(err => err.message).join(', ');
                                this.statusMessage = `Error al parsear CSV: ${this.csvPreview.parseError}`;
                                this.clearAllProcessedData();
                            } else {
                                if (results.data.length > 0) {
                                    if (results.data.length === 1) {
                                        this.csvPreview.originalFileHeaders = (results.data[0] || []).map(() => ``);
                                        this.parsedRawRows = JSON.parse(JSON.stringify(results.data));
                                    } else {
                                        this.csvPreview.originalFileHeaders = results.data[0] || [];
                                        this.parsedRawRows = JSON.parse(JSON.stringify(results.data.slice(1)));
                                    }
                                } else {
                                    this.csvPreview.originalFileHeaders = [];
                                    this.parsedRawRows = [];
                                }
                                this.statusMessage = 'Archivo analizado. Aplicando transformaciones para vista previa...';
                            }
                            this.refreshTablePreview();
                        }
                    });
                },

                refreshTablePreview() { // (Mantener como antes)
                    if (this.parsedRawRows.length === 0 && this.csvPreview.originalFileHeaders.length === 0) {
                        if (!this.fileName) this.statusMessage = 'Cargue un archivo.';
                        else if (!this.csvPreview.parseError) this.statusMessage = 'Archivo vacío o sin datos parseables.';
                        this.csvPreview.displayRows = [];
                        this.csvPreview.displayHeaders = [];
                        return;
                    }

                    let processedRows = JSON.parse(JSON.stringify(this.parsedRawRows));

                    if (this.csvOptions.shuffleRows && processedRows.length > 1) {
                        for (let i = processedRows.length - 1; i > 0; i--) {
                            const j = Math.floor(Math.random() * (i + 1));
                            [processedRows[i], processedRows[j]] = [processedRows[j], processedRows[i]];
                        }
                    }

                    if (this.csvOptions.invertColumns) {
                        processedRows = processedRows.map(row => {
                            if (row && row.length >= 2) {
                                const newRow = [...row];
                                [newRow[0], newRow[1]] = [newRow[1], newRow[0]];
                                return newRow;
                            }
                            return row;
                        });
                    }
                    this.csvPreview.displayRows = processedRows;
                    this.updateDisplayHeaders();
                    if (!this.csvPreview.parseError && !this.isLoadingAudio) this.statusMessage = 'Vista previa de tabla actualizada.';
                },

                updateDisplayHeaders() { // (Mantener como antes)
                    let baseHeaders = this.csvPreview.originalFileHeaders;
                    let maxColsFromData = 0;
                    if (this.csvPreview.displayRows.length > 0 && this.csvPreview.displayRows[0]) {
                        maxColsFromData = Math.max(0, ...this.csvPreview.displayRows.map(r => r ? r.length : 0));
                    }
                    const numColsToDisplay = Math.max(baseHeaders.length, maxColsFromData);

                    if (numColsToDisplay === 0) {
                        this.csvPreview.displayHeaders = [];
                        return;
                    }

                    const newHeaders = [];
                    for (let i = 0; i < numColsToDisplay; i++) {
                        let actualColIndexForVoice = i;
                        if (this.csvOptions.invertColumns) {
                            if (i === 0) actualColIndexForVoice = 1;
                            else if (i === 1) actualColIndexForVoice = 0;
                        }

                        let headerText = (baseHeaders && baseHeaders[i] != null) ? String(baseHeaders[i]) : `Columna ${i + 1}`;
                        let voiceName = '';
                        let voiceRateInfo = '';
                        let currentVoiceSettings = null;

                        if (actualColIndexForVoice === 0 && this.sapiVoices[0]) {
                            currentVoiceSettings = this.sapiVoices[0];
                        } else if (actualColIndexForVoice === 1 && this.sapiVoices[1]) {
                            currentVoiceSettings = this.sapiVoices[1];
                        }

                        if (currentVoiceSettings && currentVoiceSettings.name) {
                            voiceName = this.getVoiceDisplayName(currentVoiceSettings.name);
                            voiceRateInfo = ` (Vel: ${currentVoiceSettings.rate})`;
                        }

                        if (voiceName) {
                            newHeaders.push(`${this.escapeHtml(headerText)} <br><small>(Voz: ${this.escapeHtml(voiceName)}${voiceRateInfo})</small>`);
                        } else {
                            newHeaders.push(this.escapeHtml(headerText));
                        }
                    }
                    this.csvPreview.displayHeaders = newHeaders;
                },

                getVoiceDisplayName(voiceId) { // (Mantener como antes)
                    const voice = this.availableVoices.find(v => v.id === voiceId);
                    return voice ? voice.name : voiceId;
                },

                // ANTERIORMENTE generateSSML, AHORA processAndGenerateAudio
                async processAndGenerateAudio() {
                    if (this.csvPreview.displayRows.length === 0) {
                        this.statusMessage = 'No hay datos en la vista previa para generar SSML.';
                        return;
                    }
                    this.statusMessage = 'Generando SSML...';
                    this.isLoadingAudio = true;
                    document.getElementById('audioLinkContainer').innerHTML = ''; // Limpiar enlace anterior

                    // Generar SSML (lógica de la función generateSSML anterior)
                    let rowsForSSML = this.csvPreview.displayRows;
                    let ssml = `<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-ES">\n`;
                    rowsForSSML.forEach(rowArray => {
                        if (!rowArray || rowArray.length === 0 || !rowArray.some(cell => String(cell).trim() !== '')) return;
                        const voiceSettings1 = this.sapiVoices[0];
                        const voiceSettings2 = this.sapiVoices[1];
                        const textCol1 = rowArray[0] != null ? this.escapeXml(String(rowArray[0]).trim()) : '';
                        const textCol2 = rowArray[1] != null ? this.escapeXml(String(rowArray[1]).trim()) : '';
                        const rateCol1 = 100 + (voiceSettings1.rate * 5);
                        const rateCol2 = 100 + (voiceSettings2.rate * 5);

                        if (textCol1 && voiceSettings1.name) {
                            ssml += `  <voice name="${this.escapeXml(voiceSettings1.name)}">\n`;
                            ssml += `    <prosody rate="${rateCol1}%">${textCol1}</prosody>\n`;
                            ssml += `  </voice>\n`;
                        }
                        if (textCol2 && voiceSettings2.name) {
                            ssml += `  <voice name="${this.escapeXml(voiceSettings2.name)}">\n`;
                            ssml += `    <prosody rate="${rateCol2}%">${textCol2}</prosody>\n`;
                            ssml += `  </voice>\n`;
                        }
                    });
                    ssml += `</speak>`;
                    this.generatedSSMLText = ssml;
                    this.statusMessage = 'SSML generado. Enviando para procesar audio...';

                    // Enviar SSML a PHP para generar audio
                    try {
                        const response = await fetch('', { // Enviar al mismo script PHP
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                ssml: this.generatedSSMLText,
                                originalFilename: this.fileName, // PHP usará esto para nombrar el WAV
                                // Opcional: enviar detalles de voz si PHP los necesita para el CLI
                                // voice1: this.sapiVoices[0],
                                // voice2: this.sapiVoices[1],
                            }),
                        });

                        if (!response.ok) {
                            const errorData = await response.json().catch(() => ({
                                message: 'Error de red o respuesta no JSON.'
                            }));
                            throw new Error(`Error del servidor: ${response.status} ${response.statusText}. ${errorData.message || ''}`);
                        }

                        const result = await response.json();

                        if (result.success) {
                            this.statusMessage = `Éxito: ${result.message}`;
                            const audioLink = document.createElement('a');
                            audioLink.href = result.audioFile; // Asumiendo que PHP devuelve la ruta al archivo
                            audioLink.textContent = `Descargar ${result.audioFile.split('/').pop()}`; // Mostrar solo nombre de archivo
                            audioLink.setAttribute('download', '');
                            document.getElementById('audioLinkContainer').appendChild(audioLink);
                        } else {
                            this.statusMessage = `Error de PHP: ${result.message} ${result.errorDetails ? JSON.stringify(result.errorDetails) : ''}`;
                        }
                    } catch (error) {
                        this.statusMessage = `Error en la petición: ${error.message}`;
                        console.error('Error al enviar SSML:', error);
                    } finally {
                        this.isLoadingAudio = false;
                        const ssmlDetails = document.getElementById('ssmlPreviewDetails');
                        if (ssmlDetails && !ssmlDetails.hasAttribute('open')) {
                            ssmlDetails.setAttribute('open', '');
                        }
                    }
                },
                escapeXml(unsafe) { // (Mantener como antes)
                    if (typeof unsafe !== 'string') return '';
                    return unsafe.replace(/[<>&'"]/g, c => ({
                        '<': '&lt;',
                        '>': '&gt;',
                        '&': '&amp;',
                        '\'': '&apos;',
                        '"': '&quot;'
                    } [c]));
                },
                escapeHtml(unsafe) { // (Mantener como antes)
                    if (typeof unsafe !== 'string') return '';
                    return unsafe.replace(/[&<>"']/g, c => ({
                        '&': '&amp;',
                        '<': '&lt;',
                        '>': '&gt;',
                        '"': '&quot;',
                        "'": '&#039;'
                    } [c]));
                },
                triggerSSMLClearAndAdviseRegenerate(optionChangedMsg) { // (Mantener como antes)
                    if (this.generatedSSMLText && !this.isLoadingAudio) {
                        this.generatedSSMLText = '';
                        this.statusMessage = `${optionChangedMsg} cambiado. El SSML ha sido limpiado, por favor regenere.`;
                        document.getElementById('audioLinkContainer').innerHTML = ''; // Limpiar enlace de audio también
                    }
                }
            },
            watch: { // (Mantener como antes, pero separator ahora llama a parseFileAndPreparePreview)
                'csvOptions.separator': function() {
                    if (this.selectedFile && this.fileContentCache) {
                        this.parseFileAndPreparePreview();
                    }
                },
                'csvOptions.shuffleRows': function() {
                    this.refreshTablePreview();
                    this.triggerSSMLClearAndAdviseRegenerate('Opción de desordenar');
                },
                'csvOptions.invertColumns': function() {
                    this.refreshTablePreview();
                    this.triggerSSMLClearAndAdviseRegenerate('Opción de invertir columnas');
                },
                'sapiVoices': {
                    handler() {
                        this.refreshTablePreview();
                        this.triggerSSMLClearAndAdviseRegenerate('Configuración de voz');
                    },
                    deep: true
                }
            },
            mounted() {
                // Poblar selectores de voz con la primera voz disponible si no hay nada seleccionado
                if (this.availableVoices.length > 0) {
                    if (!this.sapiVoices[0].name) this.sapiVoices[0].name = this.availableVoices[0].id;
                    if (!this.sapiVoices[1].name && this.availableVoices.length > 1) this.sapiVoices[1].name = this.availableVoices[1].id;
                    else if (!this.sapiVoices[1].name) this.sapiVoices[1].name = this.availableVoices[0].id; // fallback a la primera si solo hay una
                }
                this.refreshTablePreview();
            }
        }).mount('#app');
    </script>
</body>

</html>