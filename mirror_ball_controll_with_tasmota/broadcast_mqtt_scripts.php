<?php
	$h1="mosquitto_pub -h 172.17.0.2 -t ".$_GET['topic']." -m ".$_GET['mes']."";
        $link=exec($h1);
 exit();
?>
<!DOCTYPE html>
<html lang="ko">
    <head>
        <title>Test page</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
</html>
