# CHAT recorder for Twitch streams

An easy-to-use Python bot for retrieving Twitch chat data from multiple streams/channels 
simultaneously.
The module help you to launch a process monitoring a list of streamers of Twitch platform for an amount of time or until the it is ask to stop the recording. 

RAW data are logged in the <code>output/logs</code> and analysis results are generated in <code>output/reports</code>.
Reports involves stream-elements notification analysis, chatter characteristics and basic words extrapolation.
  
## Credits
This project is a fork of the project <code>twitch-listener</code> and a special thanks goes to 
[**oliver-lloyd**](https://github.com/oliver-lloyd).

## Required modules
- **pandas**: pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. Install it with <code>pip install pandas</code>. Pip will install its dependencies like *numpy*.
- **requests**: Requests is a simple, yet elegant, HTTP library. Install it with <code>pip install requests</code>

Missing pip on windows? don't worry, follow those steps:
1. Download PIP *get-pip.py*
   1. Launch a command prompt if it isn't already open. To do so, open the Windows search bar, type cmd and click on the icon.

   2. Then, run the following command to download the get-pip.py file:
           
	  <code>curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py</code>
2. Installing PIP on Windows
 
    To install PIP type in the following: <code>python get-pip.py</code>
	
    If the file isn’t found, double-check the path to the folder where you saved the file. You can view the contents of your current directory using the following command: <code>dir</code>
3. Verify Installation

    Once you’ve installed PIP, you can test whether the installation has been successful by typing the following:
    <code>pip --version</code>
    
	Result returns in console the current version of pip installed

## Installation:
```
pip install twitch-chat-recorder
```


# Steps for acquiring Twitch credentials (skip if you already have these):
1) Get a twitch.tv account 
	- get one here https://www.twitch.tv/signup
2) Obtain a Twitch client id
	- Get yours by registering an app here https://dev.twitch.tv/console/apps/create
	- (You can set 'OAuth Redirect URL' to 'http://localhost')
3) Acquire a Twitch OAuth token
	- Get yours here https://twitchapps.com/tmi/

Store these values securely. You now have everything you need to use TwitchListener.

# Example usage:

#TODO: update example script 
```python

from twitch_chat_recorder import listener

# Connect to Twitch
bot = listener.TwitchConnector('yourUsernameHere',
                                'yourOauthHere',
				'yourClientIDHere')

# List of channels to connect to
channels_to_listen_to = ['Enkk', 'AnimeNightLive', 'Ivan_Grieco', "Cerbero_Podcast"]

# Scrape live chat data into raw log files. (Duration is seconds, default 0 to keep logging forever)
bot.listen(channels_to_listen_to, duration=1800)

# Convert log files into .CSV format
bot.parse_logs(timestamp=True)

# Generate adjacency matrix
bot.adj_matrix(weighted=False, matrix_name="streamer_network.csv")
```

## Notes
#### Bot List
Bot chat metrics uses a list of bot names defined in resources. This list shall be update with the apperence of new bot 
tools. The current list of bots are downloaded from *https://twitchinsights.net/bots*

A future development will download the bot list from *https://twitchbots.info/api*
