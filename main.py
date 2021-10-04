import asyncio

import os
# from dotenv import load_dotenv
import discord
from discord.embeds import Embed
from discord.file import File
from discord.player import AudioPlayer
from youtube_dl.utils import smuggle_url, update_url_query
import youtube_dl
import logging
from discord.ext.commands import bot
from discord.ext import commands
from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL

import random
import datetime

#Global variables

colours = [0xfc0303, 0xfc7303, 0xfcdf0, 0x88fc03, 0x03fc80, 0x03fcdb, 0x03b1fc,0x9d03fc, 0xd203fc, 0xfc03c6, 0xfc0303]

features = ''':sparkles: **Welcome to Otaku** :sparkles:
:musical_note: **Music** :musical_note:
:one: !join : Joins a voice channel.
:two: !link : Plays from a URL (Supported: https://bit.ly/3yYrdbc).
:three: !play : Plays by Search.
:four: !queue : Adds Song in Queue.
:five: !stop : Stops and disconnects the bot from voice.
:six: !stream : Streams from a url (same as yt, but doesn't predownload).
:seven: !volume : Changes the player's volume.

:game_die: **Random** :game_die:
:one: !choose : Helps Selecting Between Words Randomly.
:two: !random : Generates a Random Number between Input Number 1 and Input Number 2.

:mechanic: **Bot Management** :mechanic:
:one: !donate : Donation.
:two: !ping : Checks Server Ping.
:three: !help : Displays this command.

:gear: **Currently Working On** :gear:
:one: Queue Feature.
:two: More Utility Features.
:three: Fun Features.
:four: Pause Feature.
**MORE FEATURES COMING SOON**'''

# load_dotenv('.env')

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),description='Otaku Bot Commands:')
bot.remove_command("help")

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    players = {}
    queues = {}

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays by Search"""

        results = YoutubeSearch(query, max_results=10).to_dict()
        link = f"https://youtube.com/watch?v={results[0]['id']}"
        
        player = await YTDLSource.from_url(link, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        embed=discord.Embed(title='Now Playing', description = results[0]['title'], color=0xc58c85)
        embed.add_field(name='Duration', value=results[0]['duration'], inline=True)
        embed.add_field(name='Author', value=results[0]['channel'], inline=True)
        embed.set_thumbnail(url=results[0]['thumbnails'][0])
        await ctx.send(embed=embed)
    
    @commands.command()
    async def queue(self, ctx, *, query):
        """Adds Song in Queue"""

        results = YoutubeSearch(query, max_results=10).to_dict()
        link = f"https://youtube.com/watch?v={results[0]['id']}"
        

    @commands.command()
    async def link(self, ctx, *, link):
        """Plays from a URL (Supported: https://bit.ly/3yYrdbc)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(link, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            embed = discord.Embed(title='Now Playing', description = link, color = 0xc58c85)
            embed.set_thumbnail(url='./img/Otaku.png')
            await ctx.send(embed=embed)
            

        # await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @link.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def random(self, ctx, num1:int, num2:int):
        """Generates a Random Number between Input Number 1 and Input Number 2"""

        
        embed = discord.Embed(title='The Generated Number Between {} and {}'.format(num1, num2), description = random.randint(num1, num2), color = 0xc58c85)
        await ctx.send(embed=embed)

    @commands.command()
    async def choose(self, ctx, *, string:str):
        """Helps Selecting Between Words Randomly"""

        lst = list(string.split(" "))
        embed = discord.Embed(title = 'The Selected Item is', description = random.choice(lst), color = 0xc58c85)
        await ctx.send(embed=embed)

    # @commands.command()
    # async def 

class Bot_Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        """No need to explain!"""

        if(bot.latency * 1000 > 100):
            await ctx.send(f"Pong! {round(bot.latency * 1000)}ms (Whew. Donate to improve server performance!)")
        else:
            await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
    
    @commands.command()
    async def donate(self, ctx):
        """Donation"""

        embed=discord.Embed(title='Thanks for running this command!', description='Till then Enjoy! HF :D', color=0xc58c85)
        embed.set_thumbnail(url='https://media.giphy.com/media/S8qWh22ptNJNnEpBOf/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        """Custom help command"""
        
        user_name = str(ctx.author).split('#')[0]
        my_embed = discord.Embed(title="Bot commands",
                         description=features,
                         color=colours[random.randrange(0, 10)])
        my_embed.set_author(name=f"Hello {user_name}, here are my",
                    icon_url=message.author.avatar_url)
        my_embed.set_footer(text="Thanks for using Otaku ")
        await ctx.send(embed = my_embed)#"in chat"
        await ctx.author.send(embed = my_embed)#"By DM"
        

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')



bot.add_cog(Music(bot))
bot.add_cog(Random(bot))
bot.add_cog(Bot_Management(bot))
bot.run(os.environ.get('TOKEN'))
