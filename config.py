DISCORD_BOT_TOKEN = "NjkyODI1Nzk4NTA3MjMzMzky.Xn0S8g.8I4-b91oCG1GdaCLFlrkEcZGBvM"

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
