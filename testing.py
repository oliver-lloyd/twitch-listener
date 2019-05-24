# Get dictionary of live streams
from twitch import TwitchClient

client = TwitchClient(client_id='2ieanu14o1w8iphbl3smon6fbik2y5')
live = client.streams.get_live_streams()
streams = {}
for i in live:
    streams[i['channel']['display_name']] = i
  