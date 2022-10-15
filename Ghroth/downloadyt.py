import youtube_dl
import discord

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
    "options":"-vn"
}

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
