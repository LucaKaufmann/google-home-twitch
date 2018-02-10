from optparse import OptionParser
from subprocess import call

parser = OptionParser()
parser.add_option("-s", "--stream", dest="stream",
                  help="play stream", action="store", type="string")
parser.add_option("-p", "--player", dest="player",
                  help="chromecast player", action="store", type="string")
parser.add_option("-c", "--client-id", dest="clientId",
                  help="twitch client ID", action="store", type="string")

(options, args) = parser.parse_args()
streamInput = options.stream.lower()
CHROMECAST_DEVICE = options.player.lower()
TWITCH_CLIENT_ID = options.clientId.lower()

streams = {
    "stream name 1": "stream name on twitch",
    "stream name 2": "stream name on twitch"
}

if streamInput in streams:
    print "Stream in dictionary"
    streamToCast = streams[streamInput]
else:
    print "Stream not in dictionary"
    streamToCast = streamInput

url = "twitch.tv/"+streamToCast
call(["python", "/home/pi/stream2chromecast/stream2chromecast.py", "-devicename", CHROMECAST_DEVICE, "-stop"])
call(["livestreamer", url, "best", "--http-header=Client-ID="+TWITCH_CLIENT_ID, "--player-passthrough=http,hls,rtmp", "--player=python /home/pi/stream2chromecast/stream2chromecast.py -devicename "+CHROMECAST_DEVICE+" -playurl"])
