import os
from queue import Queue
from typing import List, Dict

import discord
import youtube_dl
from discord import VoiceChannel, Guild, VoiceClient, User
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from cogs.model.social_queue import SocialQueue
from config import DEFAULT_YTDL_OPTS, DEFAULT_YTDL_FORMAT, SONGS_DIR


class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super(MusicCog, self).__init__()
        self.__bot = bot
        self.__voice_clients: List[VoiceClient] = []

        self.__social_queues_by_guild: Dict[Guild, SocialQueue[str]] = {}
        self.__participant_queues_by_user_id: Dict[str, Queue[str]] = {}

    async def __connect_to_voice_channel(self, voice_channel: VoiceChannel):
        voice_client = await voice_channel.connect()
        self.__voice_clients.append(voice_client)

    async def __disconnect_from_voice_channel(self, guild: Guild):
        self.__voice_clients.remove(guild.voice_client)
        await guild.voice_client.disconnect()

    def __next(self, voice_client: VoiceClient):
        social_queue = self.__social_queues_by_guild[voice_client.guild]
        song_path = self.__download_song(social_queue.next(), voice_client)
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(discord.FFmpegPCMAudio(song_path), after=lambda _: self.__next(voice_client))
        voice_client.volume = 100

    async def __play(self, user: User, voice: VoiceClient, url: str):
        if user.id not in self.__participant_queues_by_user_id:
            participant_queue = Queue()

            self.__participant_queues_by_user_id[user.id] = participant_queue
            self.__social_queues_by_guild[voice.guild].add_participant_queue(participant_queue)

        self.__participant_queues_by_user_id[user.id].put(url)

        if not voice.is_playing():
            self.__next(voice)

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

        self.__social_queues_by_guild[ctx.guild] = SocialQueue()
        await self.__connect_to_voice_channel(channel)

    @commands.command()
    async def leave(self, ctx: Context):
        await self.__disconnect_from_voice_channel(ctx.guild)

    @commands.command()
    async def play(self, ctx: Context, url: str):
        await ctx.send("Hang on! Queuing your requested song! Have a nice CoronaTime!")

        voice: VoiceClient = get(self.__voice_clients, guild=ctx.guild)
        await self.__play(ctx.author, voice, url)

    @commands.command()
    async def stop(self, ctx: Context):
        await ctx.send("Stopping the song...")

        voice: VoiceClient = get(self.__voice_clients, guild=ctx.guild)
        voice.stop()
