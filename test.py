import pytest
from downloader import YouTubeDownloader
from pathlib import Path


@pytest.fixture(scope="module")
def youtube_downloader_video_audio_path():
    return YouTubeDownloader("https://www.youtube.com/watch?v=MZGw222bWdM", True, False,
                             "C:/Users/jerem/Downloads")


@pytest.fixture(scope="module")
def youtube_downloader_video_audio_without_path():
    return YouTubeDownloader("https://www.youtube.com/watch?v=MZGw222bWdM", True,
                             False)


@pytest.fixture
def cwd_path():
    return Path("C:/Users/jerem/Desktop/Dev actif/youtube_2_mp3/downloads")


def test_download_video_all_ok(youtube_downloader_video_audio_path):
    file = Path("C:/Users/jerem/Downloads/Recommence_encore_MIJ_Ases.mp3")
    if file.exists():
        file.unlink()
    downloader = youtube_downloader_video_audio_path
    result, message = downloader.download()
    assert result is True
    assert message == "Download completed: Recommence_encore_MIJ_Ases.mp3"


def test_download_video_already_existing(youtube_downloader_video_audio_path):
    downloader = youtube_downloader_video_audio_path
    result, message = downloader.download()
    assert result is False
    assert message == "Recommence_encore_MIJ_Ases.mp3 already exists"


def test_download_video_without_path_all_ok(youtube_downloader_video_audio_without_path, cwd_path):
    file = cwd_path / "Recommence_encore_MIJ_Ases.mp3"
    if file.exists():
        file.unlink()
    downloader = youtube_downloader_video_audio_without_path
    result, message = downloader.download()
    assert result is True
    assert message == "Download completed: Recommence_encore_MIJ_Ases.mp3"


def test_download_video_without_path_already_existing(youtube_downloader_video_audio_without_path, cwd_path):
    downloader = youtube_downloader_video_audio_without_path
    result, message = downloader.download()
    assert result is False
    assert message == "Recommence_encore_MIJ_Ases.mp3 already exists"


def test_format_name(youtube_downloader_video_audio_path):
    assert (youtube_downloader_video_audio_path.format_name("exemple----youtube.test%", True)
            == "exemple_youtube_test_.mp3")
    assert (youtube_downloader_video_audio_path.format_name("__.xyz&%%test", False)
            == "_xyz_test.mp4")


def test_make_path_with_download_path(youtube_downloader_video_audio_path):
    assert (youtube_downloader_video_audio_path.make_path("testfile.txt")
            == Path("C:/Users/jerem/Downloads/testfile.txt"))


def test_make_path_without_download_path(youtube_downloader_video_audio_without_path, cwd_path):
    assert youtube_downloader_video_audio_without_path.make_path("testfile.txt") == cwd_path / "testfile.txt"


def test_is_path_existing(youtube_downloader_video_audio_path):
    existing_file = Path("C:/Users/jerem/Downloads/existing_file.txt")
    existing_file.touch()
    assert youtube_downloader_video_audio_path.is_path_existing(existing_file)
