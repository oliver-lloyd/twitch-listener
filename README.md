# Twitch listener bot

An easy to use Python bot for retrieving Twitch chat data from multiple streams simultaneously. 


__Current functionality__:
- Connect and log the chat data from multiple Twitch streams 
- Logging of chat data terminated if the channel goes offline


__Planned functionality__:
- Parsing the stored logs into usable formats (.CSV etc)
- Specify duration of data collection


__Example usage:__

import TwitchListener

# Set up twitch connection
bot = TwitchListener.twitch( nickname = 'yourUsernameHere', oauth = 'yourOauthTokenGoesHere', client_id = 'yourClientIDGoesHere' )

# Scrape chat data. 
bot.listen(channels = ['Northernlion', 'Ninja'], duration = 10 )

# Convert the text log files to csv
bot.parse_logs()
