<?php
// Récupérer l'adresse IP de la requête
// $ip_address = $_SERVER['REMOTE_ADDR'];
$ip_address = $_GET['ip'];
$url = "http://ip-api.com/json/{$ip_address}";
$response = file_get_contents($url);
$data = json_decode($response, true);
$add = " | loc: null";
if ($data['status'] == 'success') {
    $country = $data['country'];
    $region = $data['regionName'];
    $city = $data['city'];
    $countryCode = $data['countryCode'];
    $lat = $data['lat'];
    $long = $data['lon'];
    $add = "loc:".$city."__".$region."__".$country."__".$countryCode."__".$lat."__".$long;
} else {
    $add = "loc: null";
}


// Nettoyer l'adresse IP pour qu'elle soit valide comme nom de fichier
$ip_address = str_replace(array(':', '.'), '_', $ip_address);

// Créer un dossier "logs" s'il n'existe pas déjà
$log_directory = 'logs';
if (!is_dir($log_directory)) {
    mkdir($log_directory, 0777, true);
}

// Créer un nom de fichier basé sur l'adresse IP de la requête
$log_file = $log_directory . '/' . $ip_address . '.txt';

$city = $city ?? "null";
$region = $region ?? "null";
$country = $country ?? "null";
$countryCode = $countryCode ?? "null";

// Formater les informations et les écrire dans le fichier texte
$log_content = date('Y-m-d H:i:s') . ' | ';
$log_content .= "URI: " . $_SERVER['REQUEST_URI'] . " | ";
$log_content .= "User Agent: " . $_SERVER['HTTP_USER_AGENT'] . " | ";
$log_content .= "Request Method: " . $_SERVER['REQUEST_METHOD'] . " | ";
$log_content .= $add . "\n";

// Créer le fichier de journal s'il n'existe pas
if (!file_exists($log_file)) {
    file_put_contents($log_file, '');
}

// Ajouter les informations au fichier de journal
file_put_contents($log_file, $log_content, FILE_APPEND);

// Lire la version à partir du fichier version.txt au même niveau que version.php
$version_file = 'version.txt';
if (file_exists($version_file)) {
    $latest_version = file_get_contents($version_file);
} else {
    $latest_version = "Version non disponible";
}

// Retourner la version
echo $latest_version;

