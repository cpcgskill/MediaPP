# -*-coding:utf-8 -*-
"""
:创建时间: 2023/12/21 1:40
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

if False:
    from typing import *

import cx_Freeze
from cx_Freeze import setup, Executable

target = Executable(
    script="gui.py",
    base="Win32GUI",
    target_name="MediaPP",
    icon="favicon.ico"
)

setup(
    name="MediaPP",
    version='0.1.0',
    description="MediaPP, 一个基于Python的媒体处理软件",
    author="cpcgskill",
    options={
        'build_exe': {
            'include_files': ["bin"],
            'packages': ['numpy', 'PyQt6', 'scipy', 'qfluentwidgets'],
            'include_msvcr': False,
        }
    },
    executables=[target]
)
