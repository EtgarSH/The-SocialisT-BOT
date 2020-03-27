import os
from typing import List

import discord
import youtube_dl
from discord import Message, ChannelType, VoiceChannel, Guild, VoiceClient, AudioSource
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from config import DISCORD_BOT_TOKEN, DEFAULT_YTDL_OPTS, DEFAULT_YOUTUBE_SONG_NAME, DEFAULT_YTDL_FORMAT


class MusicBot(commands.Bot):
    def __init__(self):
        super(MusicBot, self).__init__(command_prefix='$')
        self.__voice_clients: List[VoiceClient] = []

    async def connect_to_voice_channel(self, voice_channel: VoiceChannel):
        voice_client = await voice_channel.connect()
        self.__voice_clients.append(voice_client)

    async def disconnect_from_voice_channel(self, guild: Guild):
        self.__voice_clients.remove(guild.voice_client)
        await guild.voice_client.disconnect()

    async def play(self, url: str, guild: Guild):
        self.__download_song(url)

        voice: VoiceClient = get(self.__voice_clients, guild=guild)
        if voice.is_playing():
            voice.stop()
        voice.play(discord.FFmpegPCMAudio(DEFAULT_YOUTUBE_SONG_NAME))
        voice.volume = 100
        voice.is_playing()

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


bot = MusicBot()


@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user.name))


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    await bot.connect_to_voice_channel(channel)


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx: Context):
    await bot.disconnect_from_voice_channel(ctx.guild)


@bot.command(pass_context=True)
async def play(ctx: Context, url):
    await ctx.send("Hang on! Playing your requested song!")
    await bot.play(url, ctx.guild)


bot.run(DISCORD_BOT_TOKEN)
