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

import json
import os

if False:
    from typing import *
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentWindow,
                            SubtitleLabel, ToolButton, PrimaryPushButton, LineEdit,
                            TitleLabel, DoubleSpinBox, SpinBox, BodyLabel,
                            CardWidget, InfoBadge, InfoLevel, PushButton, SmoothScrollArea, TeachingTip,
                            TeachingTipTailPosition, TeachingTipView, ComboBox, TextEdit, PopupTeachingTip
                            )
from qfluentwidgets import FluentIcon, Theme, setTheme

import task
from video import *

task_ad = task.TaskAD()


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

        # help label
        self.help_label = BodyLabel('''对视频批量进行降噪和增益处理''', self)
        self.main_layout.addWidget(self.help_label)

        # Input Dir and Output Dir
        self.input_dir_box = PathBox(is_dir=True)
        self.output_dir_box = PathBox(is_dir=True)

        self.main_layout.addWidget(SubtitleLabel('Input Dir', self))
        self.main_layout.addWidget(self.input_dir_box)
        self.main_layout.addWidget(SubtitleLabel('Output Dir', self))
        self.main_layout.addWidget(self.output_dir_box)

        self.setting_layout = QHBoxLayout()
        # 降噪强度
        self.noise_reduction_strength = DoubleSpinBox()
        self.noise_reduction_strength.setRange(0, 1)
        self.noise_reduction_strength.setSingleStep(0.01)
        self.noise_reduction_strength.setValue(0.01)
        self.setting_layout.addWidget(SubtitleLabel('Noise Reduction Strength', self))
        self.setting_layout.addWidget(self.noise_reduction_strength)

        # 增益倍数
        self.gain_multiple = SpinBox()
        self.gain_multiple.setRange(0, 100)
        self.gain_multiple.setSingleStep(1)
        self.gain_multiple.setValue(5)
        self.setting_layout.addWidget(SubtitleLabel('Gain Multiple', self))
        self.setting_layout.addWidget(self.gain_multiple)

        self.main_layout.addLayout(self.setting_layout)

        # Process Button
        self.process_bn = PrimaryPushButton('Process')
        self.process_bn.clicked.connect(self.process)
        self.main_layout.addWidget(self.process_bn)

        self.main_layout.addStretch()

    @property
    def rootWidget(self):
        now_widget = self
        while now_widget.parentWidget():
            now_widget = now_widget.parentWidget()
        return now_widget

    def process(self):
        task_ad.register_task(
            'Batch processing',
            ['python', 'batch_process_video.py', self.input_dir_box.path, self.output_dir_box.path,
             str(self.noise_reduction_strength.value()), str(self.gain_multiple.value())],
        )
        MessageBox('Success', 'Task added', self.rootWidget).exec()


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
            audio_path = audio_noise_reduction(audio_path, strength=0.01)
            # audio_noise_reduction(audio_path,
            #                       audio_out_path=output_audio_path,
            #                       strength=0.005)
            audio_gain(audio_path, multiple=5, audio_out_path=output_audio_path)

        except Exception as e:
            import traceback
            traceback.print_exc()
            MessageBox('Error', str(e), self).exec()


class OutputWidget(QFrame):
    closeSignal = pyqtSignal()
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('OutputWidget')

        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(TitleLabel('Output', self))

        self.output_text = TextEdit(self)
        self.output_text.setReadOnly(True)
        self.main_layout.addWidget(self.output_text)

        self.copy_bn = PushButton('Copy')
        self.copy_bn.clicked.connect(lambda: QApplication.clipboard().setText(text))
        self.copy_bn.clicked.connect(self.closeSignal.emit)
        self.main_layout.addWidget(self.copy_bn, alignment=Qt.AlignmentFlag.AlignRight)

        self.output_text.setText(text)


class TaskItemWidget(CardWidget):
    def __init__(self, task_inf, parent=None):
        # type: (task.Task, QWidget) -> None
        super().__init__(parent=parent)
        self.task_inf = task_inf

        self.main_layout = QHBoxLayout(self)

        self.task_name_label = BodyLabel(self.task_inf.name, self)
        self.task_name_label.setObjectName('task_name_label')
        self.main_layout.addWidget(self.task_name_label)

        self.create_time_label = BodyLabel(self.task_inf.create_time.strftime('%Y-%m-%d %H:%M:%S'), self)
        self.create_time_label.setObjectName('create_time_label')
        self.main_layout.addWidget(self.create_time_label)

        self.main_layout.addStretch()

        status = self.task_inf.status
        if status == task.TaskStatus.running:
            self.task_status_label = InfoBadge("Running", self, InfoLevel.ATTENTION)
        if status == task.TaskStatus.success:
            self.task_status_label = InfoBadge("Success", self, InfoLevel.SUCCESS)
        if status == task.TaskStatus.error:
            self.task_status_label = InfoBadge("Error", self, InfoLevel.ERROR)

        self.main_layout.addWidget(self.task_status_label)

        # 打印输出
        self.print_output_bn = PushButton('Show output', self)
        self.print_output_bn.clicked.connect(self.show_output)
        self.main_layout.addWidget(self.print_output_bn)

        # 打印命令行
        self.print_command_bn = PushButton('Show command', self)
        self.print_command_bn.clicked.connect(self.show_command)
        self.main_layout.addWidget(self.print_command_bn)

    @property
    def rootWidget(self):
        now_widget = self
        while now_widget.parentWidget():
            now_widget = now_widget.parentWidget()
        return now_widget

    def show_output(self):
        # MessageBox('Output', self.task_inf.stdout.getvalue(), self.rootWidget).exec()
        view = OutputWidget(self.task_inf.stdout.getvalue())

        # add widget to view
        tip = PopupTeachingTip.make(view, target=self.print_output_bn, duration=-1, parent=self)
        view.closeSignal.connect(tip.close)

    def show_command(self):
        position = TeachingTipTailPosition.BOTTOM
        view = OutputWidget(' '.join(self.task_inf.commands))

        # add widget to view
        tip = PopupTeachingTip.make(view, target=self.print_command_bn, duration=-1, tailPosition=position, parent=self)
        view.closeSignal.connect(tip.close)


class TaskIndexWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('TaskIndexWidget')

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addStretch()

    def update_task_list(self):
        # clear task item
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        # add task item
        for task_inf in task_ad.task_info_list:
            item = TaskItemWidget(task_inf, self)
            self.main_layout.insertWidget(0, item)


class TaskWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('TaskWidget')

        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(TitleLabel('Task', self))

        self.scroll_area = SmoothScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet('border: none; background: transparent;')
        self.main_layout.addWidget(self.scroll_area)

        self.index_widget = TaskIndexWidget(self)
        self.scroll_area.setWidget(self.index_widget)

    def showEvent(self, e):
        super(TaskWidget, self).showEvent(e)
        self.index_widget.update_task_list()


class SettingWidget(QFrame):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent=parent)
        self.setObjectName('SettingWidget')

        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(TitleLabel('Setting', self))

        self.theme_layout = QHBoxLayout()
        self.theme_layout.addWidget(SubtitleLabel('Theme', self))
        self.theme_box = ComboBox(self)
        self.theme_box.addItems(['Auto', 'Light', 'Dark'])
        self.theme_box.setCurrentText('Auto')
        self.theme_box.currentTextChanged.connect(self.change_theme)
        self.theme_layout.addWidget(self.theme_box)
        self.theme_layout.addStretch()
        self.main_layout.addLayout(self.theme_layout)

        # export and import setting
        self.export_import_layout = QHBoxLayout()
        self.export_bn = PrimaryPushButton('Export')
        self.export_bn.clicked.connect(self.export_setting)
        self.export_import_layout.addWidget(self.export_bn)
        self.import_bn = PrimaryPushButton('Import')
        self.import_bn.clicked.connect(self.import_setting)
        self.export_import_layout.addWidget(self.import_bn)
        self.export_import_layout.addStretch()
        self.main_layout.addLayout(self.export_import_layout)

        self.main_layout.addStretch()

        self.load()

    @staticmethod
    def change_theme(theme):
        if theme == 'Auto':
            setTheme(Theme.AUTO)
        elif theme == 'Light':
            setTheme(Theme.LIGHT)
        elif theme == 'Dark':
            setTheme(Theme.DARK)

    def save(self):
        with open('setting.json', 'w') as f:
            json.dump({
                'theme': self.theme_box.currentText()
            }, f)

    def load(self):
        if os.path.exists('setting.json'):
            with open('setting.json', 'r') as f:
                setting = json.load(f)
                self.theme_box.setCurrentText(setting['theme'])
                self.change_theme(setting['theme'])

    def export_setting(self):
        path = QFileDialog.getSaveFileName(self, 'Export setting', 'setting.json', 'JSON File (*.json)')[0]
        if path:
            with open(path, 'w') as f:
                json.dump({
                    'theme': self.theme_box.currentText()
                }, f)

    def import_setting(self):
        path = QFileDialog.getOpenFileName(self, 'Import setting', '', 'JSON File (*.json)')[0]
        if path:
            import shutil
            shutil.copy(path, 'setting.json')
            self.load()


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.videoInterface = VideoWidget(self)
        self.musicInterface = MusicWidget(self)
        self.taskInterface = TaskWidget(self)
        self.settingInterface = SettingWidget(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.videoInterface, FluentIcon.VIDEO, 'Video')
        self.addSubInterface(self.musicInterface, FluentIcon.MUSIC, 'Music')
        self.addSubInterface(self.taskInterface, FluentIcon.CHECKBOX, 'Task', position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings',
                             position=NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setWindowTitle('MediaPP')

    def saveState(self):
        self.settingInterface.save()

    def closeEvent(self, e):
        super().closeEvent(e)
        msg = MessageBox('Exit', 'Are you sure you want to exit?', self)
        msg.yesSignal.connect(lambda: (e.accept(), self.saveState()))
        msg.cancelSignal.connect(lambda: e.ignore())
        msg.exec()


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
