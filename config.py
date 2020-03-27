DISCORD_BOT_TOKEN = "NjkyODI1Nzk4NTA3MjMzMzky.Xn0S8g.8I4-b91oCG1GdaCLFlrkEcZGBvM"

DEFAULT_YTDL_FORMAT = "mp3"

DEFAULT_YTDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': DEFAULT_YTDL_FORMAT,
        'preferredquality': '192',
    }],
}

DEFAULT_YOUTUBE_SONG_NAME = "song.{}".format(DEFAULT_YTDL_FORMAT)
