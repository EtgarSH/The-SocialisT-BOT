from discord.ext import commands

from cogs.anti_groovy_spam_cog import AntiGroovySpamCog
from config import DISCORD_BOT_TOKEN_PATH
from cogs.music_cog import MusicCog


def load_discord_token() -> str:
    with open(DISCORD_BOT_TOKEN_PATH, 'r') as token_file:
        return token_file.read()


def main():
    bot = commands.Bot(command_prefix='$')

    bot.add_cog(MusicCog(bot))
    bot.add_cog(AntiGroovySpamCog(bot))

    bot.run(load_discord_token())


if __name__ == "__main__":
    main()
