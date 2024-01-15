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

from cx_Freeze import setup, Executable

target = Executable(
    script="gui.py",
    base="console",
    target_name="MediaPP",
    icon="favicon.ico",
    shortcut_name="Media Processing Program",
    shortcut_dir="MediaPP",
)

setup(
    name="MediaPP",
    version='0.1.1',
    description="MediaPP, 一个基于Python的媒体处理软件",
    author="cpcgskill",
    options={
        'build_exe': {
            'include_files': ["bin"],
            'packages': ['numpy', 'PyQt6', 'scipy', 'qfluentwidgets', 'gui'],
            'include_msvcr': False,
        },
        'bdist_msi': {
            "add_to_path": True,
            "data": {
                "ProgId": [
                    ("Prog.Id", None, None, "一个媒体处理工具， 使用ffmpeg+sox。", "IconId", None),
                ],
                "Icon": [
                    ("IconId", "favicon.ico"),
                ],
            },
            "upgrade_code": "{30360DC6-0DA3-6E80-85F6-9D451A087F1E}",
            "install_icon": "favicon.ico",
            "environment_variables": {},
        }
    },
    executables=[target]
)
# todo: 尝试添加msi支持， 但是仍未完成。