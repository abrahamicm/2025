<?php
// Comando a ejecutar
$command = 'balcon -l';

// Array para almacenar las líneas de salida
$output = array();

// Variable para el código de retorno
$return_var = 0;

// Ejecutar el comando
exec($command, $output, $return_var);

// Verificar si se ejecutó correctamente
if ($return_var !== 0) {
    $output  = [
        "Microsoft David Desktop",
        "Microsoft Helena Desktop",
        "Microsoft Zira Desktop"
    ];
} 

// Alternativa con shell_exec() para obtener toda la salida como string
// $output = shell_exec($command);
// echo "<pre>" . htmlspecialchars($output) . "</pre>";
