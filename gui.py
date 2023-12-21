# -*-coding:utf-8 -*-
"""
:创建时间: 2023/12/21 1:45
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import os

if False:
    from typing import *
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, ToolButton, PrimaryPushButton, LineEdit, TitleLabel,
                            VBoxLayout)
from qfluentwidgets import FluentIcon

from video import *

setTheme(Theme.AUTO)


class PathBox(QWidget):

    def __init__(self, is_dir=True, parent=None):
        self.is_dir = is_dir
        super().__init__(parent=parent)
        self.setAcceptDrops(True)

        # add buttons to layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.path_line = LineEdit()
        if self.is_dir:
            self.path_line.setPlaceholderText('可拖拽文件夹到此处')
        else:
            self.path_line.setPlaceholderText('可拖拽文件到此处')

        self.bn = ToolButton()
        self.bn.setIcon(FluentIcon.FOLDER)
        self.bn.clicked.connect(self.select_file)

        self.open_dir_bn = ToolButton()
        self.open_dir_bn.setIcon(FluentIcon.LINK)
        self.open_dir_bn.clicked.connect(self.open_dir)

        self.main_layout.addWidget(self.path_line)
        self.main_layout.addWidget(self.bn)
        self.main_layout.addWidget(self.open_dir_bn)

    def select_file(self):
        if self.is_dir:
            path = QFileDialog.getExistingDirectory()
        else:
            path = QFileDialog.getOpenFileName()[0]
        if path:
            self.path_line.setText(path)
        else:
            self.path_line.setText('')

    @property
    def rootWidget(self):
        now_widget = self
        while now_widget.parentWidget():
            now_widget = now_widget.parentWidget()
        return now_widget

    def open_dir(self):
        if not self.path_line.text():
            root_widget = self.rootWidget
            MessageBox('Error', 'Path is empty', root_widget).exec()
            return
        if self.path_line.text():
            os.startfile(self.path_line.text() if self.is_dir else os.path.dirname(self.path_line.text()))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            local_path = url.toLocalFile()
            if self.is_dir:
                if not os.path.isdir(local_path):
                    event.ignore()
                    return
            else:
                if not os.path.isfile(local_path):
                    event.ignore()
                    return
            self.path_line.setText(local_path)
        else:
            event.ignore()

    @property
    def path(self):
        return self.path_line.text()


class VideoWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('VideoWidget')

        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(TitleLabel('Batch processing', self))

        self.input_dir_box = PathBox(is_dir=True)
        self.output_dir_box = PathBox(is_dir=True)
        self.process_bn = PrimaryPushButton('Process')
        self.process_bn.clicked.connect(self.process)

        self.main_layout.addWidget(SubtitleLabel('Input Dir', self))
        self.main_layout.addWidget(self.input_dir_box)
        self.main_layout.addWidget(SubtitleLabel('Output Dir', self))
        self.main_layout.addWidget(self.output_dir_box)
        self.main_layout.addWidget(self.process_bn)

        self.main_layout.addStretch()

    # 支持主要视频格式
    support_ext = ['.mp4', '.kv', '.avi', '.mov', '.flv', '.wmv', '.webm']

    def process(self):
        all_files = [os.path.join(self.input_dir_box.path, i) for i in os.listdir(self.input_dir_box.path)]
        all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in self.support_ext]
        for file in all_files:
            self.process_file(file)

    def process_file(self, video_path):
        try:
            output_video_path = os.path.join(self.output_dir_box.path, os.path.basename(video_path))
            video_path, audio_path = audio_and_video_separation(video_path)

            audio_path = audio_gain(audio_path, multiple=3)
            audio_path = audio_noise_reduction(audio_path, strength=0.005)

            audio_and_video_merge(
                audio_path,
                video_path,
                output_video_path,
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            MessageBox('Error', str(e), self).exec()


class MusicWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('MusicWidget')

        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(TitleLabel('Batch processing', self))

        self.input_dir_box = PathBox(is_dir=True)
        self.output_dir_box = PathBox(is_dir=True)
        self.process_bn = PrimaryPushButton('Process')
        self.process_bn.clicked.connect(self.process)

        self.main_layout.addWidget(SubtitleLabel('Input Dir', self))
        self.main_layout.addWidget(self.input_dir_box)
        self.main_layout.addWidget(SubtitleLabel('Output Dir', self))
        self.main_layout.addWidget(self.output_dir_box)
        self.main_layout.addWidget(self.process_bn)

        self.main_layout.addStretch()

    # 支持主要音频格式
    support_ext = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma']

    def process(self):
        all_files = [os.path.join(self.input_dir_box.path, i) for i in os.listdir(self.input_dir_box.path)]
        all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in self.support_ext]
        for file in all_files:
            self.process_file(file)

    def process_file(self, audio_path):
        try:
            output_audio_path = os.path.join(self.output_dir_box.path, os.path.basename(audio_path))
            audio_path = audio_gain(audio_path, multiple=3)
            audio_noise_reduction(audio_path,
                                  audio_out_path=output_audio_path,
                                  strength=0.005)
        except Exception as e:
            import traceback
            traceback.print_exc()
            MessageBox('Error', str(e), self).exec()


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 60)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.videoInterface = VideoWidget(self)
        self.musicInterface = MusicWidget(self)
        self.settingInterface = Widget('Setting', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.videoInterface, FluentIcon.VIDEO, 'Video')
        self.addSubInterface(self.musicInterface, FluentIcon.MUSIC, 'Music')
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings',
                             position=NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(FluentIcon.TAG.path()))
        self.setWindowTitle('MediaPP')


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
