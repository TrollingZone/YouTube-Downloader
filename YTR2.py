import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QCheckBox, QRadioButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pytube import YouTube, Playlist

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'YouTube Downloader'
        self.icon = 'icon.png'
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.setStyleSheet('background-color: #202020; color: white;')
        
        # Create a label for the video URL or playlist URL
        url_label = QLabel('Enter the URL of the YouTube video or playlist:', self)
        
        # Create a line edit to accept the video URL or playlist URL
        self.url_edit = QLineEdit(self)
        
        # Create a radio button for single video download
        self.video_radio = QRadioButton('Single Video', self)
        self.video_radio.setChecked(True)
        self.video_radio.toggled.connect(self.on_radio_toggled)
        
        # Create a radio button for playlist download
        self.playlist_radio = QRadioButton('Playlist', self)
        self.playlist_radio.toggled.connect(self.on_radio_toggled)
        
        # Create a label for the video quality
        quality_label = QLabel('Select video quality:', self)
        
        # Create a combo box to select video quality
        self.quality_combo = QComboBox(self)
        self.quality_combo.addItem('Highest Resolution')
        self.quality_combo.addItem('720p')
        self.quality_combo.addItem('480p')
        self.quality_combo.addItem('360p')
        self.quality_combo.addItem('240p')
        self.quality_combo.addItem('144p')
        self.quality_combo.setCurrentIndex(0)
        
        # Create a checkbox for audio-only download
        self.audio_only_checkbox = QCheckBox('Audio-only', self)
        
        # Create a button to download the video or playlist
        download_button = QPushButton('Download', self)
        download_button.clicked.connect(self.download)
        
        # Create a vertical layout for the widgets
        vbox = QVBoxLayout()
        vbox.addWidget(url_label)
        vbox.addWidget(self.url_edit)
        vbox.addWidget(self.video_radio)
        vbox.addWidget(self.playlist_radio)
        vbox.addWidget(quality_label)
        vbox.addWidget(self.quality_combo)
        vbox.addWidget(self.audio_only_checkbox)
        vbox.addWidget(download_button)
        
        # Create a horizontal layout for the radio buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.video_radio)
        hbox.addWidget(self.playlist_radio)
        hbox.addStretch(1)
        
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.show()
        
    def on_radio_toggled(self):
        # Disable the video quality combo and audio-only checkbox if single video is selected
        if self.video_radio.isChecked():
            self.quality_combo.setEnabled(True)
            self.audio_only_checkbox.setEnabled(True)
        # Enable the video quality combo and audio-only checkbox if playlist is selected
        elif self.playlist_radio.isChecked():
            self.quality_combo.setEnabled(True)
            self.audio_only_checkbox.setEnabled(True)
        
    def download(self):
        url = self.url_edit.text()
        
        # Check if the video URL or playlist URL is empty
        if url == '':
            QMessageBox.warning(self, 'Error', 'Please enter a valid URL')
            return
        
        # Check if a radio button is selected
        if not self.video_radio.isChecked() and not self.playlist_radio.isChecked():
            QMessageBox.warning(self, 'Error', 'Please select an option')
            return
        
        # If single video is selected
        if self.video_radio.isChecked():
            try:
                yt = YouTube(url)
                stream = self.get_stream(yt, self.quality_combo.currentText(), self.audio_only_checkbox.isChecked())
                stream.download()
                QMessageBox.information(self, 'Download complete', 'Video has been downloaded successfully')
            except Exception as e:
                QMessageBox.warning(self, 'Error', str(e))
                
        # If playlist is selected
        elif self.playlist_radio.isChecked():
            try:
                playlist = Playlist(url)
                videos = playlist.video_urls
                
                for video_url in videos:
                    yt = YouTube(video_url)
                    stream = self.get_stream(yt, self.quality_combo.currentText(), self.audio_only_checkbox.isChecked())
                    stream.download()
                    
                QMessageBox.information(self, 'Download complete', 'Playlist has been downloaded successfully')
            except Exception as e:
                QMessageBox.warning(self, 'Error', str(e))
    
    def get_stream(self, yt, quality, audio_only):
        streams = yt.streams.filter(progressive=not audio_only, file_extension='mp4')
        
        # Sort the streams by resolution
        if quality == 'Highest Resolution':
            stream = streams.order_by('resolution').desc().first()
        elif quality == '720p':
            stream = streams.filter(res='720p').first()
        elif quality == '480p':
            stream = streams.filter(res='480p').first()
        elif quality == '360p':
            stream = streams.filter(res='360p').first()
        elif quality == '240p':
            stream = streams.filter(res='240p').first()
        elif quality == '144p':
            stream = streams.filter(res='144p').first()
        
        return stream
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

