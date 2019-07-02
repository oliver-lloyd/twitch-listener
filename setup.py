from distutils.core import setup
setup(
  name = 'twitch_listener',         # How you named your package folder (MyLib)
  packages = ['twitch_listener'],   # Chose the same as "name"
  version = '1.2.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Tools to scrape Twitch chat data',   # Give a short description about your library
  author = 'Oliver Lloyd',                   # Type in your name
  author_email = 'ollielloyd96@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/lloyd334/twitch-listener',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/lloyd334/twitch-listener/archive/1.2.1.tar.gz',    # I explain this later on
  keywords = ['Twitch', 'twitch.tv', 'chatbot', 'chat', 'bot', 'streamer', 'scraper', 'scraping', 'scrape', 'network', 'analysis', 'graph theory'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'requests'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   

    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
'Programming Language :: Python :: 3.6',
  ],
)