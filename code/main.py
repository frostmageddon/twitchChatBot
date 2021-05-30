from twitchio.ext import commands
from twitchio.client import Client
import os
from datetime import datetime


channel='frostmageddon'
userList = []
messagecount = 0
messageThreashHold = 50

bot = commands.Bot(
    irc_token=os.environ['TWITCH_TOKEN'],
    client_id=os.environ['TWITCH_CLIENT_ID'],
    nick='frostmageddon',
    prefix='!',
    initial_channels=[channel],
)


client = Client(
    client_id=os.environ['TWITCH_CLIENT_ID'],
    client_secret=os.environ['TWITCH_CLIENT_SECRET'],
)

# Register an event with the bot
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

@bot.event
async def event_message(ctx):
    
    timeNow = datetime.now()
    current_time = timeNow.strftime("%H:%M:%S")
    print(ctx.author)
    print(f'{current_time} {ctx.content}')
    os.write(chatlogfile, f'{current_time} {ctx.author} {ctx.content}\n'.encode())
    await bot.handle_commands(ctx)
    queueUsers(ctx)

def queueUsers(ctx):
    global messagecount
    messagecount += 1
    if messagecount > 50:
        print("count is greater than 3")
        messagecount =0
        os.write(chatlogfile, str(userList).encode())

    exist_count = userList.count(ctx.author)
    if (exist_count == 0):
        
        userList.append(ctx.author)
        



@bot.command(name='test')
async def test_command(ctx):
    await ctx.send("this is a test response")

@bot.command(name='biggdogz')
async def test_command(ctx):
    await ctx.send("hey whats up!? ")

@bot.command(name='time')
async def get_local_time(ctx):
    timeNow = datetime.now()
    current_time = timeNow.strftime("%H:%M:%S")
    await ctx.send(f"Current time = {current_time}")

@bot.command(name='water')
async def explain_water(ctx):
    await ctx.send("water is not wet")

@bot.command(name='who')
async def get_chatters(ctx):
    chatters = await client.get_chatters(channel)
    all_chatters = ' '.join(chatters.all)
   # if all_chatters.__len__ > 490
    await ctx.send(f"In chat: {all_chatters}")
    
@bot.command(name="followers")
async def get_followers(ctx):
    followers = await client.get_followers(channel)
    os.write(chatlogfile, f'{followers}\n'.encode())

@bot.command(name="zack")
async def troll_zack(ctx):
    await ctx.send("Hey Zack, remember to <alt-f4> if you run into issues ;)")

if __name__ == '__main__':
    os.chdir("../data")
    path = os.getcwd() 
    path += "/log"
    global chatlogfile
    chatlogfile = os.open(path,os.O_RDWR|os.O_CREAT|os.O_APPEND)
    
    bot.run()