# Reddit Alert
Steps to set up bot:

1. Open the .env file in the project directory
2. Follow instructions here to get bot token: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
3. Put bot token in 'DISCORD_TOKEN' section of .env file
4. Go here: https://www.reddit.com/prefs/apps
5. Go to bottom and click 'create app'
6. Select 'script' as the application type, enter anything for the other fields (ex. https://localhost:8080 for urls)
7. Click 'create app', then copy the app token (2 underneath the app title) and put it in the .env under 'REDDIT_ID'
8. Copy the 'secret' field from your Reddit app and put it in the .env under 'REDDIT_SECRET'
9. Put your Reddit username and password in the .env file under 'REDDIT_USER' and 'REDDIT_PASS'
