import discord
from discord.ext import commands


class AntiGroovySpamCog(commands.Cog):
    LOGIN_MESSAGE = "Logged in as {}"
    DIRECT_SPAM_ALERT_MESSAGE = "Please write commands in the Groovy Commands channel!"

    def __init__(self, bot: commands.Bot):
        super(AntiGroovySpamCog, self).__init__()
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.LOGIN_MESSAGE.format(self.__bot.user.name))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.__bot.user:
            return

        if message.content:
            if self.__is_command(message) and not self.__is_in_groovy_commands_channel(message):
                await message.author.send(self.DIRECT_SPAM_ALERT_MESSAGE)
                await message.delete()

    @staticmethod
    def __is_command(message: discord.Message):
        return message.content and (message.content[0] == '-' or message.content[0] == '$')

    @staticmethod
    def __is_in_groovy_commands_channel(message: discord.Message):
        return message.channel.name == 'groovy-commands'
