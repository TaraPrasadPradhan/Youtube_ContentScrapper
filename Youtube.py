from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import parse_qs, urlparse
from yt_dlp import YoutubeDL
def fetch_youtube_id(url):
    Parsed_Url=urlparse(url)
    if Parsed_Url.hostname=='youtu.be':
        return Parsed_Url.path[1:]
    if '/shorts/' in Parsed_Url.path:
        return Parsed_Url.path.split('/shorts/')[1]
    if Parsed_Url.hostname in ['www.youtube.com','youtube.com']:
        return parse_qs(Parsed_Url.query).get('v',None)[0]
    return None

def fetch_script(url):
    vid=fetch_youtube_id(url)
    if not vid:
        return " Invalid Youtube URL"
    try:
     yt=YouTubeTranscriptApi()
     fetch_transcript=yt.fetch(vid)
     
     Full_text=''.join(
        [snippet.text for snippet in fetch_transcript]
     )
     return Full_text
    except Exception as e:
        return f"Transscript error :{str(e)}"

def get_video_title(url):
    with YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("title", "No Title Found")


