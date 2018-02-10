streamInput = data.get('stream_name').lower()

streams = {
    "overwatchleague": "overwatchleague",
    "overwatch league": "overwatchleague",
    "owl": "overwatchleague",
    "lcs": "riotgames",
    "stream name 1": "stream name on twitch",
    "stream name 2": "stream name on twitch"
}

if streamInput in streams:
    streamToCast = streams[streamInput]
else:
    streamToCast = streamInput

url = "https://twitch.tv/"+streamToCast

logger.info("Streaming {}".format(streamInput))
hass.services.call("media_extractor", "play_media", {"entity_id": "media_player.YOUR_CHROMECAST", "media_content_id": url, "media_content_type": "video"})
