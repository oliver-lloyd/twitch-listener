import logging
import requests
import json

def setup_loggers(name, log_file, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s — %(message)s')
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)
    
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger
    
def is_live(streamer_name, client_id):

    twitch_api_stream_url = "https://api.twitch.tv/kraken/streams/" \
                    + streamer_name + "?client_id=" + client_id

    streamer_html = requests.get(twitch_api_stream_url)

    streamer = json.loads(streamer_html.content)

    return streamer["stream"] is not None