from pytube import YouTube
from pytube.exceptions import RegexMatchError
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, video_url):
        self.video_url = video_url
        try:
            self.yt = YouTube(self.video_url)
        except Exception as e:
            self.yt = None
        home = Path.home()
        self.downloads_path = home / "downloads"
        self.downloads_path.mkdir(parents=True, exist_ok=True)

    def download_stream(self, audio_only = False):
        try:
            if audio_only:
                stream = self.yt.streams.filter(only_audio=True).first()
                filename = self.yt.title + '.mp3'
            else:
                stream = self.yt.streams.get_highest_resolution()
                filename = self.yt.title + '.mp4'
        
            stream.download(filename=filename, output_path=self.downloads_path)
            return True, f"Download completed: {filename}"
        except Exception as e:
            return False, f"Invalid URL"

if __name__ == "__main__":
    video_url = ''
    downloader = YouTubeDownloader(video_url)
    downloader.download_stream(audio_only=True)