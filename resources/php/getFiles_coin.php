<?php
header("Access-Control-Allow-Origin: http://127.0.0.1:5500");
$directory = '../data_coins/';
$fileNames = [];
if ($handle = opendir($directory)) {
    while (false !== ($file = readdir($handle))) {
        if ($file != "." && $file != "..") {
            $fileNameWithoutExtension = pathinfo($file, PATHINFO_FILENAME);
            $fileNames[] = $fileNameWithoutExtension;
        }
    }
    closedir($handle);
} else {
    echo "error dir";
}

shuffle($fileNames);

$selectedFiles = array_slice($fileNames, 0, min(50, count($fileNames)));

$output = [
    'files' => $selectedFiles
];

$jsonOutput = json_encode($output);
$outputFile = 'data/getFiles_coin.json';
file_put_contents($outputFile, $jsonOutput);

echo "JSON output has been saved to $outputFile";
