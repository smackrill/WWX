## This bot was created by Shawn and Delilah Mackrill, Feb 2023(Father and Daughter)
## This is our first discord bot that we have created!!!
## Yes we totally used a lot of help from Stack Overflow and AI assistants
## A lot of work still went into this and we learned a lot along the way!
## Please be respectful of our learning process- if you have supportive input please feel free to let us know!

import discord
from discord.ext import commands
import sqlite3
import asyncio
from datetime import datetime, timedelta

## Connect to database file, if no database file is present one will be created by the script.
## You may erase a database file to reset the counter
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages (user_id INTEGER, channel_id INTEGER, message_id INTEGER)''')
conn.commit()
## Discord intents
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix=',', intents=intents)

## Bot event that updates the database file when a user posts a message with an image extension in specified channels.
## You must specify the channel ID's where you want the bot to monitor
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id in [## Erase this comment and enter your channel ID's here separated with commas.]:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['.jpeg', '.jpg', '.png', '.gif', '.img']):
                c.execute("SELECT * FROM messages WHERE user_id=? AND channel_id=? AND message_id=?", (message.author.id, message.channel.id, message.id))
                data = c.fetchone()
                if data is None:
                    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (message.author.id, message.channel.id, message.id))
                    conn.commit()
                break
    await bot.process_commands(message)

## Let's us know that the bot has logged in, this will be posted in the cmdline output.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

## This is the command that will initiate population of the database file for a sepcified user.
## Use this when you initially set up the bot, and you want to begin populating your database file
## Depending on how many channels you have specified, this may take some time.
## You can edit the amount of days popcount will go back for this count.
## Execute with ,popcount @username OR ,popcount @self
## Edit the "await ctx.send" line below to change the message the bot will post
@bot.command(name='popcount')
async def populate_db(ctx, member: discord.Member):
    await ctx.send(f'Starting count for **{member.display_name}**. Do you realize how many messages I have to go through?  I could do it in a microsecond, but I think I will take my time...to spite you.')
    channels = [bot.get_channel(id) for id in [## Erase this comment and enter your channel ID's here separated with commas.]]
    for channel in channels:
        print(f'Processing channel: {channel.name}')
        # Only retrieve messages from the past 120 days
        before_date = datetime.utcnow() - timedelta(days=120)
        try:
            async for message in channel.history(limit=None):
                if message.author == member:
                    for attachment in message.attachments:
                        if any(attachment.filename.lower().endswith(ext) for ext in ['.jpeg', '.jpg', '.png', '.gif', '.img']):
                            c.execute("SELECT * FROM messages WHERE user_id=? AND channel_id=? AND message_id=?", (member.id, channel.id, message.id))
                            data = c.fetchone()
                            if data is None:
                                c.execute("INSERT INTO messages VALUES (?, ?, ?)", (member.id, channel.id, message.id))
                                conn.commit()
                                print(f'Inserted message {message.id} into database')
                            else:
                                print(f'Message {message.id} already in database')
                            break
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f'Error while processing channel {channel.name}: {e}')
   
    await ctx.send(f'All messages for {member.mention} have been counted. Try ` ,count @self mention `.')

## This command returns the amount of images a user has uploaded and have been captured by the bot.
## This returns the value of the initial popcount including any additional images that have been uploaded since.
## Execute this command with ,count @user OR ,count @self
@bot.command(name='count')
async def message_count(ctx, member: discord.Member):
    c.execute("SELECT COUNT(*) FROM messages WHERE user_id=?", (member.id,))
    count = c.fetchone()[0]
    await ctx.send(f'**{member.display_name}** has {count} uploads.')

## This command will change the status of the bot.
## To execute this command, type ,status 'activite_type'
@bot.command(name='status')
async def change_status(ctx, activity_type: str, *, activity_name: str):
    activity_types = {
        'playing': discord.ActivityType.playing,
        'streaming': discord.ActivityType.streaming,
        'listening': discord.ActivityType.listening,
        'watching': discord.ActivityType.watching
    }
    if activity_type.lower() not in activity_types:
        await ctx.send(f'Invalid activity type. Valid types are: {", ".join(activity_types.keys())}')
        return
    activity = discord.Activity(type=activity_types[activity_type.lower()], name=activity_name)
    await bot.change_presence(activity=activity)
    await ctx.send(f'Status changed to {activity_type} {activity_name}')

bot.run('ENTER YOUR BOT TOKEN HERE')