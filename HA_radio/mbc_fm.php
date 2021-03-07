<?php
        while(1){
        $link=exec('curl -s "http://miniplay.imbc.com/AACLiveURL.ashx?protocol=M3U8&channel=sfm&agent=android&androidVersion=24"');
        $str= substr($link, 7,3);
        if($link != "http://mfmtunein.imbc.com/tsfm/_definst_/tsfm.stream/playlist.m3u8") break; }
        $init="http://1.255.48.56/ssfm/_definst_/sfm.stream/";
        $insert1 = explode("/",$link);
    $res = $init.$insert1[6];
echo($res);
   $r1=substr($res, 0, 250);
$links1 = fopen('/home/radio/mbc_fm_1.txt', 'w');
fwrite($links1, $r1);
$r2=substr($res, 250);
$links2 = fopen('/home/radio/mbc_fm_2.txt', 'w');
fwrite($links2, $r2);
fclose($links1);
fclose($links2);
?>
