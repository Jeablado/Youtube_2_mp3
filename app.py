from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
from downloader import YouTubeDownloader
import logging

logging.basicConfig(level=logging.INFO,
                    filename="app.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s"
                    )


class DownloadThread(QtCore.QThread):
    download_finished = QtCore.Signal(str)

    def __init__(self, url, audio_only, is_playlist, downloads_path):
        super().__init__()
        self.url = url
        self.audio_only = audio_only
        self.is_playlist = is_playlist
        self.downloads_path = downloads_path

    def run(self):
        logging.info("\n")
        logging.info("Thread is running")
        downloader = YouTubeDownloader(target_url=self.url, audio_only=self.audio_only,
                                            is_playlist=self.is_playlist, download_path=self.downloads_path)
        result, message = downloader.download()
        self.download_finished.emit(message)
        if result:
            logging.info(f"{message}")
        else:
            logging.info(f"Download failed.{message}")


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YT Downloader")
        self.setWindowIcon(QIcon("assets/logo_app.png"))
        self.setup_ui()
        self.setup_connections()
        self.setup_css()
    
    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        first_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(first_row_layout)
        self.lb_info1 = QtWidgets.QLabel("WELCOME !")
        first_row_layout.addWidget(self.lb_info1)

        second_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(second_row_layout)
        self.lb_info2 = QtWidgets.QLabel("Please enter your YT URL below")
        second_row_layout.addWidget(self.lb_info2)

        third_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(third_row_layout)

        self.le_URL = QtWidgets.QLineEdit()
        self.cbb_format = QtWidgets.QComboBox()
        self.cbb_format.addItems(["mp3", "mp4"])
        self.cbb_video_playlist = QtWidgets.QComboBox()
        self.cbb_video_playlist.addItems(["video", "playlist"])
        self.btn_download = QtWidgets.QPushButton("Download")
        third_row_layout.addWidget(self.le_URL)
        third_row_layout.addWidget(self.cbb_format)
        third_row_layout.addWidget(self.cbb_video_playlist)
        third_row_layout.addWidget(self.btn_download)

    def setup_connections(self):
        self.le_URL.returnPressed.connect(self.download)
        self.btn_download.clicked.connect(self.download)

    def setup_css(self):
        self.setStyleSheet("""              
        QWidget {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        
        QLineEdit {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: "white";
            min-width: 300px;
        }

        QComboBox {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: "white";
        }

        QPushButton {
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #45a049;
        }

        QLabel {
            margin-top: 5px;
            font-size: 14px;
        }
        """)

    def download(self):
        url = self.le_URL.text()
        if url:
            self.lb_info1.setText("Download started.. please wait..")
            self.lb_info2.setText("")
            QtWidgets.QApplication.processEvents()

            audio_only = self.cbb_format.currentText() == "mp3"
            is_playlist = self.cbb_video_playlist.currentText() == "playlist"
            self.download_thread = DownloadThread(url, audio_only, is_playlist, None)
            self.download_thread.download_finished.connect(self.handle_download_finished)
            self.download_thread.start()

        else:
            self.lb_info1.setText("") 
            self.lb_info2.setText("Please enter an URL") 
    
    def handle_download_finished(self, message):
        self.lb_info1.setText(message)
        self.lb_info2.setText("Please enter your YT URL below")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = App()
    win.show()
    app.exec_()
