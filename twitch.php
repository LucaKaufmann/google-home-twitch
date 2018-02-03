<?php
// edit IP
define("CHROMECAST_DEVICE", "192.168.x.x");
// edit Client ID
define("TWITCH_CLIENT_ID", "1234123123xxxx");

// add your own streams. Key = Google Home input, Value = twitch.tv stream name
$streams = array(
  "stream name 1" => "stream name on Twitch",
  "stream name 2" => "stream name on Twitch"
);

$streamerName = $_GET["name"];

$streamerName = preg_replace("/[^A-Za-z0-9 ]/", '', $streamerName);
$streamerName = trim($streamerName);

$streamerName = strtolower($streamerName);

if (array_key_exists($streamerName, $streams)) {
  $streamToCast = $streams[$streamerName];
} else {
  $streamToCast = $streamerName;
}

$url = "twitch.tv/" . $streamToCast;

$stopcommand = "python /home/pi/stream2chromecast/stream2chromecast.py -devicename ".CHROMECAST_DEVICE." -stop";
$command = "livestreamer " . $url . " best --http-header=Client-ID=".TWITCH_CLIENT_ID." --player-passthrough=http,hls,rtmp --player=\"python /home/pi/stream2chromecast/stream2chromecast.py -devicename ".CHROMECAST_DEVICE." -playurl\"";
exec($stopcommand);
exec($command, $result);

?>
