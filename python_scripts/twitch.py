streamInput = data.get('stream_name').lower()
chromecastInput = data.get('media_player')
chromecast = chromecastInput

streams = {
    "overwatchleague": "overwatchleague",
    "overwatch league": "overwatchleague",
    "owl": "overwatchleague",
    "lcs": "riotgames",
    "gdq": "gamesdonequick",
    "games done quick": "gamesdonequick"
}

if streamInput in streams:
    streamToCast = streams[streamInput]
else:
    streamToCast = streamInput

url = "https://twitch.tv/"+streamToCast

if (chromecast == 1):
    mediaPlayer = "CHROMECAST_1"
elif (chromecast == 2):
    mediaPlayer = "CHROMECAST_2"
elif (chromecast == 3):
    mediaPlayer = "CHROMECAST_3"
else:
    mediaPlayer = ""


logger.info("Streaming {} to {}".format(streamInput, mediaPlayer))
hass.services.call("media_extractor", "play_media", {"entity_id": "media_player."+mediaPlayer, "media_content_id": url, "media_content_type": "video"})
