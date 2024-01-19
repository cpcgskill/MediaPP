# -*-coding:utf-8 -*-
"""
:创建时间: 2024/1/12 2:23
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import os.path

if False:
    from typing import *

import sys
sys.path.append('./win32')
sys.path.append('./win32com')
sys.path.append('./win32comext')
import threading
import subprocess
import logging

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from qfluentwidgets import PlainTextEdit
from qfluentwidgets import Theme, setTheme

from setting import Setting
from setting import Theme as SettingTheme

if False:
    import gui
print(sys.executable)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('MediaPP.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ]
)
class MainThread(QThread):
    close_signal = pyqtSignal(int)
    output_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainThread, self).__init__(parent)
        self.process = subprocess.Popen(
            [sys.executable, 'gui.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def run(self):
        while True:
            output = self.process.stdout.readline()
            if output == b'' and self.process.poll() is not None:
                break
            if output:
                output = output.decode('utf-8')
                if output.endswith('\r\n'):
                    output = output[:-2]
                if output.endswith('\n'):
                    output = output[:-1]
                self.output_signal.emit(output)
        self.close_signal.emit(self.process.poll())

    def kill(self):
        self.process.kill()


class MainWindow(PlainTextEdit):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Output')
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setWindowIcon(QIcon('favicon.ico'))
        if os.path.isfile('setting.json'):
            with open('setting.json', 'r') as f:
                setting = Setting.model_validate_json(f.read())
                if setting.theme == SettingTheme.AUTO:
                    setTheme(Theme.AUTO)
                elif setting.theme == SettingTheme.DARK:
                    setTheme(Theme.DARK)
                elif setting.theme == SettingTheme.LIGHT:
                    setTheme(Theme.LIGHT)

        self.thread = MainThread(self)
        self.thread.output_signal.connect(self.output)
        self.thread.close_signal.connect(self.exit)

        self.thread.start()

    def closeEvent(self, a0):
        # stop thread
        self.thread.kill()
        self.thread.wait()
        super(MainWindow, self).closeEvent(a0)

    def output(self, text):
        logging.info(text)
        self.appendPlainText(text)

    def exit(self, code):
        self.output("程序退出， 退出码: {}".format(code))
        if code == 0:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
