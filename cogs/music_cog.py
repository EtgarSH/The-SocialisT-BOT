import os
from typing import List, Dict

import discord
import youtube_dl
from discord import VoiceChannel, Guild, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from config import DEFAULT_YTDL_OPTS, DEFAULT_YOUTUBE_SONG_NAME, DEFAULT_YTDL_FORMAT, SONGS_DIR


class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super(MusicCog, self).__init__()
        self.__bot = bot
        self.__voice_clients: List[VoiceClient] = []

    async def __connect_to_voice_channel(self, voice_channel: VoiceChannel):
        voice_client = await voice_channel.connect()
        self.__voice_clients.append(voice_client)

    async def __disconnect_from_voice_channel(self, guild: Guild):
        self.__voice_clients.remove(guild.voice_client)
        await guild.voice_client.disconnect()

    async def __play(self, voice: VoiceClient, url: str):
        song_path = self.__download_song(url, voice)

        if voice.is_playing():
            voice.stop()
        voice.play(discord.FFmpegPCMAudio(song_path))
        voice.volume = 100

    @staticmethod
    def __download_song(url: str, voice_client: VoiceClient) -> str:
        song_name = voice_client.server_id
        path = os.path.join(SONGS_DIR, str("{}.{}".format(song_name, DEFAULT_YTDL_FORMAT)))

        song_there = os.path.isfile(path)
        if song_there:
            os.remove(path)

        opts = DEFAULT_YTDL_OPTS.copy()
        opts["outtmpl"] = path
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([url])

        return path

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as {}".format(self.__bot.user.name))

    @commands.command()
    async def join(self, ctx: Context):
        author = ctx.message.author
        channel = author.voice.channel
        await self.__connect_to_voice_channel(channel)

    @commands.command()
    async def leave(self, ctx: Context):
        await self.__disconnect_from_voice_channel(ctx.guild)

    @commands.command()
    async def play(self, ctx: Context, url: str):
        await ctx.send("Hang on! Playing your requested song! Have a nice CoronaTime!")

        voice: VoiceClient = get(self.__voice_clients, guild=ctx.guild)
        await self.__play(voice, url)

    @commands.command()
    async def stop(self, ctx: Context):
        await ctx.send("Stopping the song...")

        voice: VoiceClient = get(self.__voice_clients, guild=ctx.guild)
        voice.stop()
