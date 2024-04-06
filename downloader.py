from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError
from pathlib import Path

class YouTubeDownloader():
    def __init__(self):
        self.downloads_path = Path.home() / "downloads"
        self.downloads_path.mkdir(parents=True, exist_ok=True)

    def download_video(self, video_url, audio_only=False):
        try:
            yt = YouTube(video_url)
            if audio_only:
                stream = yt.streams.filter(only_audio=True).first()
                filename = f"{yt.title}.mp3"
            else:
                stream = yt.streams.get_highest_resolution()
                filename = f"{yt.title}.mp4"
        
            stream.download(filename=filename, output_path=self.downloads_path)
            return True, f"Download completed: {filename}"
        except Exception as e:
            return False, f"Error downloading video: {e}"
        
    
    def download_playlist(self, playlist_url, audio_only=False):
        try:
            playlist = Playlist(playlist_url)
            for video_url in playlist.video_urls:
                success, message = self.download_video(video_url, audio_only=audio_only)
                if not success:
                    return False, message
            return True, f"Download completed: {playlist.title}"
        except Exception as e:
            return False, f"Error downloading playlist: {e}"

if __name__ == "__main__":
    video_url = ''
    downloader = YouTubeDownloader(video_url)
    downloader.download_stream(audio_only=True)