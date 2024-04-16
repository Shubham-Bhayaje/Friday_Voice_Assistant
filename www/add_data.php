<?php

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $keyword = $_POST['Add_Your_New_Commands'];
    $filePath = $_POST['Add_Your_New_Commands_file_path'];

    // Load existing JSON data from file
    $jsonFilePath = 'C:/Friday/www/user_custom_commands.json';
    $jsonData = file_get_contents($jsonFilePath);
    $data = json_decode($jsonData, true);

    // Add new data to the array
    $newData = array(
        'keyword' => $keyword,
        'file_path' => $filePath
    );

    $data[] = $newData;

    // Convert data to JSON format
    $newJsonData = json_encode($data, JSON_PRETTY_PRINT);

    // Write updated data to the JSON file
    file_put_contents($jsonFilePath, $newJsonData);

    // Optionally, you can redirect the user to a success page
    header("Location: success.html");
    exit();
}

?>
