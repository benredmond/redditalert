import praw
import time
import os
import asyncio
import discord
from discord.ext.commands import Bot
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
now = time.time()
place_to_send = None

reddit = praw.Reddit(client_id=os.getenv('REDDIT_ID'),
                     client_secret=os.getenv('REDDIT_SECRET'),
                     password=os.getenv('REDDIT_PASS'),
                     user_agent='script:test:v1.0.0 (by /u/bisonbear2)',
                     username=os.getenv('REDDIT_USERNAME'))


BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Run !start in the channel where you want the bot to be used')

@client.command(description="Invest an amount of memecoins into a post, ex: !invest 'post_id' 100")
async def invest(id, amount):
    print(id, amount)
    post = reddit.submission(id=id)
    for top_level_comment in post.comments:
        if top_level_comment.author == 'MemeInvestor_bot':
            post.downvote()
            top_level_comment.reply('!invest ' + amount)
            post.upvote()
            embed = discord.Embed(title='Invest {0} in post {1}'.format(amount, id), color=0xff4500)
            await client.send_message(place_to_send, embed=embed)


@client.command(pass_context=True, description="Sets the bot to send messages to whichever channel you run this command in")
async def start(ctx):
    global place_to_send
    place_to_send = ctx.message.channel
    embed = discord.Embed(title='Starting bot in {0}'.format(place_to_send), color=0xff4500)
    await client.send_message(place_to_send, embed=embed)
    # await client.send_message(place_to_send, '```Starting bot in **{0}** ```'.format(place_to_send))

@asyncio.coroutine
async def listen_for_posts():
    await client.wait_until_ready()

    subreddit = reddit.subreddit('MemeEconomy')
    posts =  subreddit.stream.submissions(pause_after=0)
    while not client.is_closed:
        post = next(posts)

        if post is None:
            # Wait 60 seconds for a new submission
            await asyncio.sleep(30)

        elif post.created_utc > now:
            print(post.title)
            if not place_to_send is None:
                embed = discord.Embed(title='**{0}**'.format(post.title), url=post.shortlink,
                                      description="ID: **{0}** *(use this as first option in **!invest**)*".format(post.id), color=0xff4500)
                await client.send_message(place_to_send, embed=embed)
                await client.send_message(place_to_send, post.url)
                # await client.send_message(place_to_send, post.title + ' ' + post.id)

@asyncio.coroutine
async def dontcrash():
    channels = client.get_all_channels()
    asyncio.sleep(50)


client.loop.create_task(dontcrash())
client.loop.create_task(listen_for_posts())
client.run(os.getenv('DISCORD_TOKEN'))
