<?php
$ch=$_GET['ch'];
$url= shell_exec('python3 sports_naver.py '.$ch);
print($url);
header('Location:'.$url);
exit();
?>
