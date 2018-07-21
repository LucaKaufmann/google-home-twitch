# google-home-twitch
A basic script to allow Google Home to cast Twitch streams to a Chromecast. You'll need a computer in your local network running either Home Assistant or a web server. I used a Raspberry Pi 3 on Raspbian, any Raspberry Pi should work fine though.

Things that are needed:
* Computer running Home Assistant or Apache/other PHP capable web server
* Google Home/Assistant
* Google Chromecast

## Home assistant
Getting this to work with Home Assistant is incredibly easy. It requires a few different components though:
* [IFTTT](https://home-assistant.io/components/ifttt/)
* [python_scripts](https://home-assistant.io/components/python_script/)
* [media_extractor](https://home-assistant.io/components/media_extractor/)
* [Google Cast](https://home-assistant.io/components/media_player.cast/)

You'll need to copy the *python_scripts* folder from this repository into your home assistant config directory (on Raspbian/Hassbian it's /home/homeassistant/.homeassistant. On Hass.io it's /config).

The twitch.py script in the python_scripts folder needs to be edited. Add your favorite streams (scroll down to *List of Streams* for more info). You'll also need to set your Chromecast in:
```python
hass.services.call("media_extractor", "play_media", {"entity_id": "media_player.YOUR_CHROMECAST", "media_content_id": url, "media_content_type": "video"})
```

Then you'll need to add python_scripts: to your configuration.yaml
```yaml
python_scripts:
```

You'll also need [media_extractor:](https://home-assistant.io/components/media_extractor/). Example:
```yaml
media_extractor:
  default_query: best
```
Save configuration.yaml and restart. You can test the script by going to *Sercices* in Home Assistant (Under Developer tools). Choose python_script.twitch as your service and add the Service Data, for example:
```json
{
"stream_name":"riotgames"
}
```

Click Call Service and the stream should start playing if it's currently online. In case it doesn't work, check your Home assistant logs and you should be able to see an error message.

### Set up IFTTT
To be able to call the script from Google Assistant/Home, you'll need to set up an IFTTT applet. First you need to enable the IFTTT component in Home Assistant, [Check here for instructions](https://home-assistant.io/components/ifttt/). Home Assistant needs to be accessible from outside your network, so you might have to set up [DuckDNS (and I'd recommend Let's Encrypt as well)](https://www.splitbrain.org/blog/2017-08/10-homeassistant_duckdns_letsencrypt). If you're running Hass.io you'll be able to use the [DuckDNS addon with letsencrypt support](https://home-assistant.io/addons/duckdns/). Once that is done, we can move on to IFTTT and set up the applet:

1. Go to [IFTTT.com](https://ifttt.com), you might need to link IFTTT to your Google account and enable the [Webhook component](https://ifttt.com/maker_webhooks).
2. Create a new Applet, as a trigger choose Google Assistant - Say a phrase with a text and number ingredient and enter the phrases (I used "cast $ on player %" and "stream $ on player %"), click Create Trigger
3. As an action choose Webhook. Set the URL to http://YOUR_PUBLIC_IP:8123/api/services/python_script/twitch?api_password=YOUR_HASS_PASSWORD. Set the content type to **application/json** and add this to the Body: *{ "stream_name": "{{TextField}}" , "media_player": {{NumberField}}}* Click save.
4. You should be all done now, ask your Google home to "Stream X" or whatever phrase you used and if the stream is online, it should start playing on the Chromecast after a few seconds.

## Installation guides for Raspberry Pi (PHP and Python script)
For instructions on how to set this up for Home Assistant, scroll down.
Start with a fresh or existing Raspbian installation.
* [Install Apache and PHP](https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md)
* [Install Livestreamer (Debian)](http://docs.livestreamer.io/install.html) - `sudo apt-get install livestreamer` or install in a Virtual environment
* [Install stream2chromecast](https://github.com/Pat-Carter/stream2chromecast) - `sudo apt-get install ffmpeg` and then clone repository into /home/pi/stream2chromecast
* *Optional* [Set up a duckdns domain for your Raspberry pi](http://duckdns.org/install.jsp)

### Setup (PHP):
1. Install Apache, PHP, Livestreamer and stream2chromecast
2. Clone/Copy twitch.php into /var/www/html
3. [Create a new Twitch dev application](https://dev.twitch.tv/dashboard/apps/create), OAuth Redirect URI won't be used so add whatever
4. After creating the Twitch app, [go to the twitch dev dashboard](https://dev.twitch.tv/dashboard/apps), click on Manage and copy the Client ID
5. Edit twitch.php in /var/www/html, change **TWITCH_CLIENT_ID** and paste your Client ID
6. Change **CHROMECAST_DEVICE** to the IP or name of your Chromecast. You can check the name or IP in the Google Home apps under Settings of your Chromecast.
7. Edit/Add the stream names you'd like to be able to cast (See stream names chapter below for more details)
8. You can manually test the script by visiting *IP_OF_YOUR_SERVER*/twitch.php?name=*name of a stream on your list*
9. Set up [port forwarding](https://portforward.com/) to port 80 of your web server (something like external port 8000 > internal port 80) **Warning** this will make your web server accessible from anywhere and is quite risky and I'd recommend checking out the solution using Home Assistant.
10. Go to [IFTTT.com](https://ifttt.com), you might need to link IFTTT to your Google account and enable the [Webhook component](https://ifttt.com/maker_webhooks).
11. Create a new Applet, as a trigger choose Google Assistant - Say a phrase with a text ingredient and enter the phrases (I used "cast $" and "stream $"), click Create Trigger
12. As an action choose Webhook. Set the URL to http://YOUR_PUBLIC_IP:EXTERNAL_PORT/twitch.php?name= {{TextField}}. If you're using a duckdns it could look something like this http://YOUR_DOMAIN.duckdns.org:8000/twitch.php?name= {{TextField}}. Click save.
13. You should be all done now, ask your Google home to "Stream X" or whatever phrase you used and if the stream is online, it should start playing on the Chromecast after a few seconds.

### Using the Python script (Non HASS)
You can call the script this way:
python twitch.py -s STREAM NAME -p CHROMECAST IP -c TWITCH CLIENT ID

## List of streams
A Key-Value array is used for the list of streams. The key is the input from Google Assistant, the Value is the actual stream name on twitch.tv. This allows you to have multiple names for the same stream.

Here's an example:
```python
streams = {
    "overwatchleague": "overwatchleague",
    "overwatch league": "overwatchleague",
    "riotgames": "riotgames",
    "riot games": "riotgames",
    "lcs": "riotgames",
}
```
Or for PHP:
```php
$streams = array(
  "overwatchleague" => "overwatchleague",
  "overwatch league" => "overwatchleague",
  "riotgames" => "riotgames",
  "riot games" => "riotgames",
  "lcs" => "riotgames"
);
```
