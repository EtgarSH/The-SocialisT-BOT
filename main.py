from discord.ext import commands

from cogs.anti_groovy_spam_cog import AntiGroovySpamCog
from config import DISCORD_BOT_TOKEN
from cogs.music_cog import MusicCog


def main():
    bot = commands.Bot(command_prefix='$')

    bot.add_cog(MusicCog(bot))
    bot.add_cog(AntiGroovySpamCog(bot))

    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
