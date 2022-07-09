from distutils.core import setup

setup(
    name='twitch_chat_recorder',  # How you named your package folder (MyLib)
    packages=['twitch_chat_recorder'],  # Chose the same as "name"
    version='1.0.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Tools to scrape Twitch chat data',  # Give a short description about your library
    author='Carlo Menegazzo',  # Type in your name
    author_email='carlo.menegazzo@gmail.com',  # Type in your E-Mail
    url='https://github.com/M3ne/twitch-chat-recorder',  # Provide either the link to your github or to your website
    download_url='https://github.com/M3ne/twitch-chat-recorder/archive/1.0.0.tar.gz',
    keywords=['Twitch', 'twitch.tv', 'chatbot', 'chat', 'bot', 'streamer', 'scraper', 'scraping', 'scrape', 'network',
              'analysis', 'graph theory', 'record', 'data'],  # Keywords that define your package best
    install_requires=[
        'pandas',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.9',
    ],
)
