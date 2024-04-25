from pytube import YouTube, Playlist
from pathlib import Path
import re
import logging

logging.basicConfig(level=logging.INFO,
                    filename="app.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s"
                    )


class YouTubeDownloader:
    def __init__(self, target_url: str, audio_only: bool = False, is_playlist: bool = False, download_path: str = None):
        self.target_url, self.audio_only, self.is_playlist, self.downloads_path = (target_url, audio_only,
                                                                                   is_playlist, download_path)

    def download(self):
        if self.is_playlist:
            return self.download_playlist()
        else:
            return self.download_video()

    def download_video(self, target_url: str = None):
        if target_url is None:
            target_url = self.target_url
        try:
            yt = YouTube(target_url)
            filename = self.format_name(yt.title, self.audio_only)
            file_path = self.make_path(filename)

            if not self.is_path_existing(file_path):
                logging.info(f"Starting download for URL: {target_url}")
                if self.audio_only:
                    stream = yt.streams.filter(only_audio=True).first()
                else:
                    stream = yt.streams.get_highest_resolution()
                stream.download(filename=filename, output_path=str(file_path.parent))
                logging.info(f"Video {filename} downloaded")
                return True, f"Download completed: {filename}"
            return False, f"{filename} already exists"

        except Exception as e:
            return False, f"Error downloading video: {e}"

    def download_playlist(self):
        try:
            playlist = Playlist(self.target_url)
            for url in playlist.video_urls:
                try:
                    self.download_video(url)
                except Exception as e:
                    logging.info(f"{url} not downloaded; error: {e}")
            logging.info(f"Playlist {playlist.title} downloaded")
            return True, f"Download completed: {playlist.title}"
        except Exception as e:
            return False, f"Error downloading playlist: {e}"

    @staticmethod
    def format_name(yt_title: str, audio_only: bool):
        filename = re.sub("[^A-Za-z0-9]", '_', yt_title).replace("___", "_").replace("__", "_")
        logging.info(f"{filename}")
        if audio_only:
            filename = filename + ".mp3"
        else:
            filename = filename + ".mp4"
        return filename

    def make_path(self, filename: str) -> Path:
        if self.downloads_path is None:
            downloads_path = Path.cwd() / "downloads"
            self.downloads_path = downloads_path.resolve()
        else:
            self.downloads_path = Path(self.downloads_path).resolve()
        self.downloads_path.mkdir(parents=True, exist_ok=True)
        return self.downloads_path / filename

    @staticmethod
    def is_path_existing(path: Path):
        return path.exists()
