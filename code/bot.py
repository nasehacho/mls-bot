import datetime
from discord.ext import commands, tasks 
import discord
from dataclasses import dataclass
import requests

BOT_TOKEN = "MTE2NTU4OTI0MzQwMjQwNzk0Nw.GJx4i0.nA5ETDstw5IMmHXH7s8albc7PtgE7poSQUbDZU" 
CHANNEL_ID = 1164560194693505095 
MAX_SESSION_TIME_MINUTES = 50 

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0  

bot = commands.Bot(command_prefix= "!", intents = discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! How can I help?")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! How can I help?")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder(): 

    if break_reminder.current_loop==0:
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return 
    
    session.is_active = True 
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return  
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}")

@bot.command()
async def joke(ctx):
    response= requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
    await ctx.send(response.json())

bot.run(BOT_TOKEN)  