<?php ?><?php
if (!(isset($_GET['password']) && isset($_GET['name']))) {
    header('HTTP/1.1 401 Unauthorized');
    die();
}
$pass = $_GET['password'];
$name = $_GET['name'];

$pass = preg_replace("/[^A-Za-z0-9 ]/", '', $pass);
$name = preg_replace("/[^A-Za-z0-9 ]/", '', $name);

$to_open = "../append/" . $name . ".json";
$json = file_get_contents($to_open);
$obj = json_decode($json, True);
if ($obj['password'] === $pass) {
    header('Content-type: image/jpeg');
    header('X-message: ' . $obj['message']);
    echo base64_decode($obj['img']);
    die();
} else {
    header('HTTP/1.1 401 Unauthorized');
    die();
}

