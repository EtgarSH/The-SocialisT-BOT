import os
from typing import List

import discord
import youtube_dl
from discord import Message, ChannelType, VoiceChannel, Guild, VoiceClient, AudioSource
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from config import DISCORD_BOT_TOKEN, DEFAULT_YTDL_OPTS, DEFAULT_YOUTUBE_SONG_NAME, DEFAULT_YTDL_FORMAT


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
        self.__download_song(url)

        if voice.is_playing():
            voice.stop()
        voice.play(discord.FFmpegPCMAudio(DEFAULT_YOUTUBE_SONG_NAME))
        voice.volume = 100

    @staticmethod
    def __download_song(url):
        song_there = os.path.isfile(DEFAULT_YOUTUBE_SONG_NAME)
        if song_there:
            os.remove(DEFAULT_YOUTUBE_SONG_NAME)

        with youtube_dl.YoutubeDL(DEFAULT_YTDL_OPTS) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(DEFAULT_YTDL_FORMAT):
                os.rename(file, DEFAULT_YOUTUBE_SONG_NAME)

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
