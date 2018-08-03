import praw
import time
import os
import asyncio
import discord
import requests
from discord.ext.commands import Bot
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
now = time.time()
place_to_send = None
auto_invest = False
watched_posts = {}
coins = 400

reddit = praw.Reddit(client_id=os.getenv('REDDIT_ID'),
                     client_secret=os.getenv('REDDIT_SECRET'),
                     password=os.getenv('REDDIT_PASS'),
                     user_agent='script:test:v1.0.0 (by /u/bisonbear2)',
                     username=os.getenv('REDDIT_USERNAME'))


BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)


def invest_in_post(id, amount):
    post = reddit.submission(id=id)
    for top_level_comment in post.comments:
        if top_level_comment.author == 'MemeInvestor_bot':
            post.downvote()
            reply_str = '!invest {0}'.format(amount)
            top_level_comment.reply(reply_str)
            post.upvote()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Run !start in the channel where you want the bot to be used')

@client.command(description="Turns the auto-invest feature on or off")
async def auto(toAutoInvest):
    global auto_invest
    if toAutoInvest.lower() == "true":
        auto_invest = True
        embed = discord.Embed(title='Auto investing set to {0}'.format(auto_invest), color=0xff4500)
        await client.send_message(place_to_send, embed=embed)
    elif toAutoInvest.lower() == "false":
        auto_invest = False
        embed = discord.Embed(title='Auto investing set to {0}'.format(auto_invest), color=0xff4500)
        await client.send_message(place_to_send, embed=embed)

@client.command(description="Invest an amount of memecoins into a post, ex: !invest 'post_id' 100")
async def invest(id, amount):
    print(id, amount)
    invest_in_post(id, amount)
    embed = discord.Embed(title='Invested {0} memecoins in post: {1}'.format(amount, id), color=0xff4500)
    await client.send_message(place_to_send, embed=embed)

@client.command(pass_context=True, description="Sets the bot to send messages to whichever channel you run this command in")
async def start(ctx):
    global place_to_send
    place_to_send = ctx.message.channel
    embed = discord.Embed(title='Starting bot in {0}'.format(place_to_send), color=0xff4500)
    await client.send_message(place_to_send, embed=embed)
    # await client.send_message(place_to_send, '```Starting bot in **{0}** ```'.format(place_to_send))

@client.command(description='Displays the current amount of coins that you have')
async def coins():
    embed = discord.Embed(title='You currently have **{0}** coins'.format(coins), color=0xff4500)
    await client.send_message(place_to_send, embed=embed)

@asyncio.coroutine
async def listen_for_posts():
    await client.wait_until_ready()

    subreddit = reddit.subreddit('MemeEconomy')
    posts =  subreddit.stream.submissions(pause_after=0)
    while not client.is_closed:
        post = next(posts)
        global watched_posts

        if post is None:
            if auto_invest:
                curTime = time.time()

                for id in watched_posts.copy():
                    submission = reddit.submission(id=id)
                    print("SCORE: " + str (submission.score))
                    print("TIME DIFF: " +str ((curTime - watched_posts[id]) / 60))

                    if (curTime - watched_posts[id]) / 60 > 60:
                        del(watched_posts[id])
                    elif coins > 100 and \
                            (curTime - watched_posts[id]) / 60 > 25 and \
                            submission.score >= 25 and \
                            submission.score >= (curTime - watched_posts[id]) / 60:
                        invest_in_post(id, (int)(coins * .3))
                        embed = discord.Embed(title='Invested {0} memecoins in post: {1}'.format((int)(coins * .3), id), color=0xff4500)
                        await client.send_message(place_to_send, embed=embed)
                        del(watched_posts[id])

            await asyncio.sleep(30)

        elif post.created_utc > now:
            print(post.title)
            if not place_to_send is None:
                if auto_invest:
                    watched_posts[post.id] = post.created_utc

                embed = discord.Embed(title='**{0}**'.format(post.title), url=post.shortlink,
                                      description="ID: **{0}** *(use this as first option in **!invest**)*".format(post.id), color=0xff4500)
                await client.send_message(place_to_send, embed=embed)
                await client.send_message(place_to_send, post.url)
                await asyncio.sleep(5)
                # await client.send_message(place_to_send, post.title + ' ' + post.id)

@asyncio.coroutine
async def dontcrash():
    while not client.is_closed:
        channels = client.get_all_channels()
        await asyncio.sleep(50)

@asyncio.coroutine
async def get_coins():
    while not client.is_closed:
        global coins
        request = 'https://memes.market/api/investor/{0}'.format(os.getenv('REDDIT_USERNAME'))
        coins = requests.get(request).json()['balance']
        await asyncio.sleep(180)
    # coins = requests.get(request).balance


client.loop.create_task(dontcrash())
client.loop.create_task(get_coins())
client.loop.create_task(listen_for_posts())
client.run(os.getenv('DISCORD_TOKEN'))
