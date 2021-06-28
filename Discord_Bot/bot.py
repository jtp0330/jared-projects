######################################################
#Filename: bot.py
#Descritpion: Python practice using the following tutorial
#Tutorial: Build a Discrod Bot in
# Python That Plays Music and Send GIFs
# @author Rohan Krishna Ullas
# GitHub used: https://github.com/ytdl-org/youtube-dl
######################################################
import os

import discord
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands,tasks
from dotenv import load_dotenv
import youtube_dl
from youtube_dl import YoutubeDL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

players = {}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self,source,*,data,volume=0.5):
        super().__init__(source,volume)
        self.data = data
        self.title=data.get('title')
        self.url=""

        @classmethod
        async def from_url(cls,url,*,loop=None,stream=False):
            loop = loop or asynicio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url,download=not stream))
            if 'entries' in data:
                #plays 1st item in playlist
                data = data['entries'][0]
            filename = data['title'] if stream else ytdl.prepare_filename(data)
            return filename

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        
@bot.command(name='leave',help = 'To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play_song',help='To play song')
async def play(ctx,url):
    try:
        server = ctx.message.guild   
        voice_channel = server.voice_client   
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
@bot.command(name='pause',help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
        
@bot.command(name='stop', help = 'Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anythign at the moment.")
#send gifs on start-up
#@bot.event
#async def on_ready():
#    for guild in bot.guilds:
#        for channel in guild.text_channels:
#            if str(channel) == "general":
#                await channel.send('Bot Activated..')
#                await channel.send(file=discord.File('add_gif_file_name_here.png'))
#            print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))
            

if __name__ == "__main__":
    bot.run(TOKEN)


