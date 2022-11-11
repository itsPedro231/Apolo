import discord
import os
import youtube_dl
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
import asyncio
queue = []
x = 1
y = 0
z = 1

token = 0 #your bot token goes here

# downloading settings
dlOptions = {
  'format' : 'worstaudio/worstvideo/worst',
  'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
  'restrictfilenames': True,
  'noplaylist': True,
  'nocheckcertificate': True,
  'ignoreerrors': True,
  'logtostderr': False,
  'quiet': False,
  'no_warnings': True,
  'default_search': 'auto',
  'source_address': '0.0.0.0',
}
# streaming settings
ffmpeg_options = { 
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(dlOptions)
# standard prefix
prefix = '!'
bot = commands.Bot(prefix, intents=discord.Intents.default())

@bot.command()
# shows all of the available commands
async def commands(ctx):
  await ctx.channel.send("-- commands -- \n- {}join: Apolo joins the author's voice channel \n- {}play + 'yt link': Apolo plays music \n- {}disconnect: Apolo leaves channel \n- {}pause: Apolo stops the music \n- {}resume: Apolo unpauses the music \n- {}stop: Music is stopped and cancelled \n- {}prefix + 'new prefix': changes the prefix \n-- in development --".format(db['customPrefix'], db['customPrefix'], db['customPrefix'], db['customPrefix'], db['customPrefix'], db['customPrefix'], db['customPrefix'], db['customPrefix'],))

@bot.command()
# changes the prefix
async def prefix(ctx, prefix):
  bot.command_prefix = prefix
  await ctx.send("**Prefix changed to {}**".format(prefix))
  db['customPrefix'] = prefix
  print(db['customPrefix'])
   

@bot.command()
# gets the youtube song link and plays it
async def play(ctx, link):
  flag = True
  if not ctx.message.author.voice:
    await ctx.send("**{}, join a voice channel first**".format(ctx.message.author.name))
  else:
    channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send("**Connected**")
  server = ctx.message.guild
  voice = server.voice_client
  if flag:
    info = ytdl.extract_info(link, download = False)
    URL = info['formats'][0]['url']
    voice.play(discord.FFmpegPCMAudio(URL, **ffmpeg_options))
    flag = False
  else:
    while not flag:
      server = ctx.message.guild
      voice = server.voice_client 
      if voice.is_playing() == True or voice.is_playing() != None:
        queue.append(link)
        link = queue[0]
      else:
        await asyncio.sleep(3)
        flag = True
        await play(ctx, link)
  return voice, x  

# the bot is disconnected from the channel
@bot.command()
async def disconnect(ctx):
  server = ctx.message.guild
  voice = server.voice_client
  if voice.is_connected():
    await voice.disconnect()
    await ctx.send("**Disconnected**")
  else: await ctx.send("**Apolo needs to be in a voice channel**")
  
# the song is paused
@bot.command()
async def pause(ctx):
  server = ctx.message.guild
  voice = server.voice_client
  if voice.is_playing() == True:
    voice.pause()
    await ctx.send("**Paused**")
  else: await ctx.send("**Apolo isnt playing any music**") 

# the song is resumed     
@bot.command()
async def resume(ctx):
  server = ctx.message.guild
  voice = server.voice_client
  if voice.is_paused():
    voice.resume()
    await ctx.send("**resumed**")
  else: await ctx.send("**Apolo isn't paused**")
  
# stop and delete the song
@bot.command()
async def stop(ctx):
  server = ctx.message.guild
  voice = server.voice_client
  if voice.is_playing():
    voice.stop()
    await ctx.send("**stopped**")
  else: await ctx.send("**Apolo isn't playing**")

# makes the bot online forever in replit    
keep_alive()
bot.run(token)
