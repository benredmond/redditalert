# Reddit Alert

Prerequisites:
1. Python 3 installed on your computer (check with **python --version** or **python3 --version**)
1. PIP installed on your computer (should be installed already if Python 3 is installed)

Steps to set up bot:

1. Open the .env file in the project directory
1. Follow instructions here to get bot token: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
1. Put bot token in 'DISCORD_TOKEN' section of .env file
1. Go here: https://www.reddit.com/prefs/apps
1. Go to bottom and click 'create app'
1. Select 'script' as the application type, enter anything for the other fields (ex. https://localhost:8080 for urls)
1. Click 'create app', then copy the app token (2 underneath the app title) and put it in the .env under 'REDDIT_ID'
1. Copy the 'secret' field from your Reddit app and put it in the .env under 'REDDIT_SECRET'
1. Put your Reddit username and password in the .env file under 'REDDIT_USER' and 'REDDIT_PASS'
1. Run the install script in the terminal by typing **pip3 install -r requirements.txt** (if that doesn't work try replacing pip3 with pip)
1. Run the bot by typing **python3 main.py** (if your default Python is already v3 just type **python main.py**)

How to use the bot:

* First, type **!start** in the channel where you want the bot to send messages (can be in a direct message to the bot)
* The bot will now send you new posts from /r/MemeEconomy
* To invest in a post, type **!invest <id> <amount>**, where <id> is the id of the post (given whenever the bot sends notification of a new post) and <amount> is the amount of coins to invest
* To turn auto-investing in posts on/off, type **!auto <true/false>** (this feature is still under development)
* To get your current amount of coins, type **!coins**

If you have any questions/issues, create a new issue on this repository