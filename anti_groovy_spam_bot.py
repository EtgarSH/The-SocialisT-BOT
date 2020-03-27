import discord

from config import DISCORD_BOT_TOKEN


class AntiGroovySpamBot(discord.Client):
    LOGIN_MESSAGE = "Logged in as {}"
    DIRECT_SPAM_ALERT_MESSAGE = "Please write commands in the Groovy Commands channel!"

    async def on_ready(self):
        print(self.LOGIN_MESSAGE.format(self.user))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
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


if __name__ == "__main__":
    bot = AntiGroovySpamBot()
    bot.run(DISCORD_BOT_TOKEN)
