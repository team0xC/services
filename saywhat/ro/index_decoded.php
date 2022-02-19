<?php ?><?php
class PageTemplate {
    public function footer() {
?>
	  </center>
	 </body>
 </html>
	  <?php
    }
    public function header() {
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PhotoSharing Website</title>

  </head>
  <body style="background-color: #d0d0c8;">
<center>

<?php
    }
}
if (isset($_REQUEST['page'])) {
    $p = $_REQUEST['page'];
}
if (empty($p) or $p === "" or $p === "index") {
    $template = new PageTemplate();
    $template->header();
?>
   <h1>Upload an image</h1>
<form method="POST" action="/?page=upload.php" enctype="multipart/form-data">
  Name: <input type="text" name="name"><br>	  
  Password: <input type="password" name="password"><br>
  Message: <input type="text" name="message"><br>
  <input type="file" name="fileToUpload">
  <input type="submit" name="submit" value="Upload Yo Image">
</form>
   <?php
    $template->footer();
} else {
    include_once ($p);
}
