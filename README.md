# google-home-twitch
A basic script to allow Google Home to cast Twitch streams to a Chromecast. You'll need a computer in your local network as a web server. I used a Raspberry Pi 3 on Raspbian, any Raspberry Pi should work fine though.

Things that are needed:
* Apache or other PHP capable web server
* Google Home/Assistant
* Google Chromecast

## Installation guides for Raspberry Pi
Start with a fresh or existing Raspbian installation.
* [Install Apache and PHP](https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md)
* [Install Livestreamer (Debian)](http://docs.livestreamer.io/install.html) - `sudo apt-get install livestreamer` or install in a Virtual environment
* [Install stream2chromecast](https://github.com/Pat-Carter/stream2chromecast) - `sudo apt-get install ffmpeg` and then clone repository into /home/pi/stream2chromecast
* *Optional* [Set up a duckdns domain for your Raspberry pi](http://duckdns.org/install.jsp)

## Setup:
1. Install Apache, PHP, Livestreamer and stream2chromecast
2. Clone/Copy twitch.php into /var/www/html
3. [Create a new Twitch dev application](https://dev.twitch.tv/dashboard/apps/create), OAuth Redirect URI won't be used so add whatever
4. After creating the Twitch app, [go to the twitch dev dashboard](https://dev.twitch.tv/dashboard/apps), click on Manage and copy the Client ID
5. Edit twitch.php in /var/www/html, change **TWITCH_CLIENT_ID** and paste your Client ID
6. Change **CHROMECAST_DEVICE** to the IP or name of your Chromecast. You can check the name or IP in the Google Home apps under Settings of your Chromecast.
7. Edit/Add the stream names you'd like to be able to cast (See stream names chapter below for more details)
8. You can manually test the script by visiting *IP_OF_YOUR_SERVER*/twitch.php?name=*name of a stream on your list*
9. Set up [port forwarding](https://portforward.com/) to port 80 of your web server (something like external port 8000 > internal port 80) **Warning** this will make your web server accessible from anywhere and is quite risky, but for now it's the easiest way to get this done.
10. Go to [IFTTT.com](https://ifttt.com), you might need to link IFTTT to your Google account and enable the [Webhook component](https://ifttt.com/maker_webhooks).
11. Create a new Applet, as a trigger choose Google Assistant - Say a phrase with a text ingredient and enter the phrases (I used "cast $" and "stream $"), click Create Trigger
12. As an action choose Webhook. Set the URL to http://YOUR_PUBLIC_IP:EXTERNAL_PORT/twitch.php?name= {{TextField}}. If you're using a duckdns it could look something like this http://YOUR_DOMAIN.duckdns.org:8000/twitch.php?name= {{TextField}}. Click save.
13. You should be all done now, ask your Google home to "Stream X" or whatever phrase you used and if the stream is online, it should start playing on the Chromecast after a few seconds.

## List of streams
A Key-Value array is used for the list of streams. The key is the input from Google Assistant, the Value is the actual stream name on twitch.tv. This allows you to have multiple names for the same stream.

Here's an example:
```php
$streams = array(
  "overwatchleague" => "overwatchleague",
  "overwatch league" => "overwatchleague",
  "riotgames" => "riotgames",
  "riot games" => "riotgames",
  "lcs" => "riotgames"
);
```
