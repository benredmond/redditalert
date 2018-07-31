import praw
import time
import os
import threading
from threading import Timer
import asyncio
import discord
from discord.ext.commands import Bot
from asgiref.sync import AsyncToSync
now = time.time()
channel = "NONE"

reddit = praw.Reddit(user_agent='script:test:v1.0.0 (by /u/bisonbear2)',
                     client_id=os.environ['ID'], client_secret=os.environ['SECRET'],
                     username=os.environ['USER'], password=os.environ['PASS'])



BOT_PREFIX = ("?", "!")
TOKEN = os.environ['DISCORD_TOKEN']
client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print("RECIEVED")
    if message == "!start":
        channel = message.channel
        print (channel)


@client.command()
async def invest(id, amount):
    print(id, amount)
    post = reddit.submission(id=id)
    for top_level_comment in post.comments:
        if top_level_comment.author == 'MemeInvestor_bot':
            post.downvote()
            top_level_comment.reply('!invest ' + amount)
            post.upvote()

@client.command()
async def test(amount):
    print(amount)

@asyncio.coroutine
async def listen_for_posts():
    await client.wait_until_ready()
    start_time = time.time()

    subreddit = reddit.subreddit('MemeEconomy')
    posts =  subreddit.stream.submissions(pause_after=0)
    while not client.is_closed:
        post = next(posts)

        if post is None:
            # Wait 60 seconds for a new submission
            await asyncio.sleep(30)

        elif post.created_utc > now:
            print(post.title)
            if not channel == "NONE":
                await client.send_message(channel, post.url)
                await client.send_message(channel, post.title + ' ' + post.id)

@asyncio.coroutine
async def dontcrash():
    channels = client.get_all_channels()
    asyncio.sleep(50)


client.loop.create_task(dontcrash())
client.loop.create_task(listen_for_posts())
client.run(TOKEN)
