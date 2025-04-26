# -*-coding:utf-8 -*-
"""
:创建时间: 2024/7/24 1:54
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

运行gui.py, 并将输出重定向到Document/MediaPP.log文件中
"""

from __future__ import unicode_literals, print_function, division

if False:
    from typing import *
import os
import sys
import subprocess
import datetime

log_file = os.path.join(os.path.expanduser('~'), 'Documents', 'media_pp.log')
print('log_file:', log_file)
with open(log_file, 'a+', encoding='utf-8') as f:
    print('=' * 6, 'Open MediaPP at', datetime.datetime.now(), '=' * 6, file=f, flush=True)
    process = subprocess.Popen(
        [sys.executable, 'gui.py'],
        stdout=f,
        stderr=f,
    )
    process.wait()
    print('process return:', process.returncode, file=f, flush=True)
    sys.exit(process.returncode)
