import discord
from discord import file
from discord import voice_client
from discord.channel import VoiceChannel
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import youtube_dl




load_dotenv()

DISCORD_TOKEN = os.getenv("discord_token_Ghroth")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

youtube_dl.utils.bug_reports_messages = lambda : ""

ytdl_format_options = {
    "format" : "bestaudio/best",
    "restictfilenames" : True,
    "noplaylist": True,
    "nocheckcertificate" : True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quite" : True,
    "no_warnings": True,
    "default_search":"auto",
    "source_address":"0.0.0.0"
}
ffmpeg_options = {
'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
}
loop = False

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self,source,*, data,volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        print(data)
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None,stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None,lambda: ytdl.extract_info(url,download=not stream))
        if "entries" in data:
            data = data['entries'][0]
        filename = data["title"] if stream else ytdl.prepare_filename(data)
        return filename





@bot.command(name='join',help="Tells the bot to join the voice channel")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(Name="leave", help='to make the bot leave the voice channel')
async def leave(ctx):
    voice_client=ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connect to a voice channel.")
    



@bot.command(name="play_file", help="To play a song")
async def play(ctx, url):
    try:
        server = ctx.message.guild
        print(str(server.voice_client))
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source=filename))
        await ctx.send("Now Singing: {} ".format(filename))

    except:
        await ctx.send("That cannot be found.")

@bot.command(name="play",help="to stream a song")
async def stream(ctx,url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        if voice_channel.is_playing():
            ctx.send("A song is already playing, adding to the playlist")
        print("potato")
        async with ctx.typing():
            with ytdl:
                song_info = ytdl.extract_info(url, download=False)
                print(song_info)
            await ctx.send("Now Singing: {} ".format(song_info["title"]))
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source=song_info["formats"][0]["url"],**ffmpeg_options))
            voice_channel.play.source = discord.PCMVolumeTransformer(voice_channel.play)
    except:
        await ctx.send("The song cannot be found.")


        
@bot.command(name="loop",help="")
async def loop(ctx):
    global loop

    if loop:
        await ctx.send("no longer looping through the sacred data")
        loop = False
    else:
        await ctx.send("Looping through the sacred data")
        loop = True
        
@bot.command(name="pause", help="this pauses the song")
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("I am not playing anything right now, Azathoth may awaken.")


@bot.command(name="resume", help="resumes the song")
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume();
    else:
        await ctx.send("No tune was played this past moment.")

@bot.command(name="stop", help="stops the song")
async def stop(ctx):
    voice_client =ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("I have not played anything this past moment")


@bot.event
async def on_ready():
    print("The bot is ready!")

@bot.command(Name="hello", help="simple hello message")
async def hello(ctx):
    await ctx.send("Hello, may I sing you a sweet tune? Keep the eater of worlds -Azathoth, in slumber? !play to play a song.")

def start_bot():
    return bot.start(DISCORD_TOKEN)