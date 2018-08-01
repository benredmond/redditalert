# Reddit Alert
Steps to set up bot:

1. Follow instructions here to get bot token: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
2. Put bot token in 'DISCORD_TOKEN' section of .env file
3. Go here: https://www.reddit.com/prefs/apps
4. Go to bottom and click 'create app'
5. Select 'script' as the application type, enter anything for the other fields (ex. https://localhost:8080 for urls)
6. Click 'create app', then copy the app token (2 underneath the app title) and put it in the .env under 'ID'
7. Copy the 'secret' field from your Reddit app and put it in the .env under 'SECRET'
8. Put your Reddit username and password in the .env file under 'USER' and 'PASS'
