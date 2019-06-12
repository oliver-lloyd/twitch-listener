# Twitch listener bot

An easy to use Python bot for retrieving Twitch chat data from multiple streams simultaneously. 

Steps for acquiring credentials:
1) Get a twitch.tv account 
	- get one here https://www.twitch.tv/signup
2) Obtain a Twitch client id
	- Get yours by registering an app here https://dev.twitch.tv/console/apps/create
	- (You can set 'OAuth Redirect URL' to 'http://localhost')
3) Acquire a Twitch OAuth token
	- Get yours here https://twitchapps.com/tmi/

Store these values securely. You now have everything you need to use TwitchListener.

Example usage:

```python

import TwitchListener

# Connect to Twitch
bot = TwitchListener.twitch('yourUsernameHere', 
                             'yourOauthHere', 
                             'yourClientIDHere')

# List of channels to connect to
channels_to_listen_to = ['Northernlion', 'DumbDog', 'DanGheesling']

# Scrape chat data into raw log files. (Duration is seconds)
bot.listen(channels_to_listen_to, duration = 1800) 

# Convert log files into .CSV format
bot.parse_logs(timestamp = True)
```


