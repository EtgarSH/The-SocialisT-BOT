DISCORD_BOT_TOKEN_PATH = './discord_token.txt'

SONGS_DIR = "./songs/"

DEFAULT_YTDL_FORMAT = "mp3"

DEFAULT_YTDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': DEFAULT_YTDL_FORMAT,
        'preferredquality': '192',
    }],
}
