<?php ?><?php
$template = new PageTemplate();
$template->header();
$target_dir = "../append/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 0;
$imageFileType = pathinfo($target_file, PATHINFO_EXTENSION);
$fsize = $_FILES['fileToUpload']['size'];
if (isset($_POST["submit"]) && isset($_POST['name']) && isset($_POST['password']) && isset($_POST['message'])) {
    if ($imageFileType == "jpg") {
        $uploadOk = 1;
    } else {
        echo "<p>Sorry, only JPG images are accepted.</p>";
        $uploadOk = 0;
    }
    if (!($fsize >= 0 && $fsize <= 200000)) {
        $uploadOk = 0;
        echo "<p>Sorry, JPG too large.</p>";
    }
    if (!preg_match('/[a-zA-Z0-9_]+/', $_POST['name'])) {
        $uploadOk = 0;
        echo "<p>Sorry, the name that you gave is invalid</p>";
    }
}
if ($uploadOk) {
    $newpath = $target_dir . $_POST['name'] . ".json";
    if (file_exists($newpath)) {
        echo "<p>Sorry, looks like you already uploaded a file.</p>";
        exit - 1;
    }
    $img_contents = file_get_contents($_FILES["fileToUpload"]["tmp_name"]);
    $to_save = array();
    $to_save['password'] = $_POST['password'];
    $to_save['message'] = $_POST['message'];
    $to_save['img'] = base64_encode($img_contents);
    $to_save_str = json_encode($to_save);
    echo "json string: " . $to_save_str;
    if (file_put_contents($newpath, $to_save_str) === False) {
        echo "<p>Error uploading your file.</p>";
    } else {
        echo "<p>Image correctly uploaded.</p>";
        echo "<p><a href='/?page=view.php&name=" . urlencode($_POST['name']) . "&password=" . urlencode($_POST['password']) . "'>View your image</a></p>";
    }
}
$template->footer();
