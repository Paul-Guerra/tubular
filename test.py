import youtube_dl

# ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     'logger': MyLogger(),
#     'progress_hooks': [my_hook],
# }
opts = {
  'nocheckcertificate': True,
  'keepvideo': False,
  'outtmpl': 'tmp/%(title)s - %(id)s.%(ext)s',
  'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '128',
  }],
}

with youtube_dl.YoutubeDL(opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=4axllc8XSPY'])