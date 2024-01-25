# -*-coding:utf-8 -*-
"""
:创建时间: 2023/12/23 20:40
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import sys

if False:
    from typing import *

import subprocess
import threading
import io
import enum
import datetime


class TaskStatus(enum.Enum):
    running = 'running'
    success = 'success'
    error = 'error'


class Task(object):
    def __init__(self, name, commands):
        # type: (str, List[str]) -> None
        self.name = name
        self.commands = commands
        self.create_time = datetime.datetime.now()
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.status = TaskStatus.running

    def run(self):
        # type: () -> None
        # 启动子进程运行命令
        process = subprocess.Popen(
            self.commands,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        # 实时读取输出并写入IO流
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                if output.endswith(b'\r\n'):
                    output = output[:-2]
                elif output.endswith(b'\n') or output.startswith(b'\r'):
                    output = output[:-1]
                try:
                    output = output.decode('utf-8')
                except UnicodeDecodeError:
                    output = output.decode('gbk')

                print(output)
                self.stdout.write(output)
                self.stdout.flush()
        self.status = TaskStatus.success if process.poll() == 0 else TaskStatus.error

    def start(self):
        # type: () -> None
        thread = threading.Thread(target=self.run, name=self.name)
        thread.start()


class TaskAD(object):
    def __init__(self):
        self.task_list = list()  # type: List[Task]

    def register_task(self, name, commands):
        # type: (str, List[str]) -> None
        task = Task(name, commands)
        self.task_list.append(task)
        task.start()

    def register_task_python_script(self, name, commands):
        # type: (str, List[str]) -> None
        self.register_task(name, [sys.executable] + commands)

    def find_task_status(self, name):
        # type: (str) -> bool
        for task in self.task_list:
            if task.name == name:
                return task.status

    @property
    def task_info_list(self):
        return [task for task in self.task_list]
