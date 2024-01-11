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
import threading
import subprocess

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from qfluentwidgets import PlainTextEdit
from qfluentwidgets import Theme, setTheme

from setting import Setting
from setting import Theme as SettingTheme

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

        self.thread = threading.Thread(target=self.run_gui)
        self.thread.start()

    def run_gui(self):
        process = subprocess.Popen(
            [sys.executable, 'gui.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.appendPlainText(output)
                self.ensureCursorVisible()
                self.repaint()
        exit(process.poll())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())