# -*-coding:utf-8 -*-
"""
:创建时间: 2024/5/19 22:13
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
import os
from processor.ffmpeg import audio_and_video_separation, audio_and_video_merge

# 测试音视频分离, 这部分应当失败
test_files = ['./../test/input/test.mp4']
test_files = [os.path.abspath(file) for file in test_files]

for file in test_files:
    print('=' * 9, 'test fail:', file, '=' * 9)
    try:
        video_out_path = f'./../test/output/{os.path.basename(file).split(".")[0]}.mp4'
        audio_out_path = f'./../test/output/{os.path.basename(file).split(".")[0]}.wav'
        audio_and_video_separation(
            file,
            video_out_path=os.path.abspath(video_out_path),
            audio_out_path=os.path.abspath(audio_out_path),
        )
    except Exception as e:
        import traceback

        print('success fail:', file)
        print(traceback.format_exc())
    print('=' * 24)

# 测试音视频分离
test_files = ['./../test/input/test2.mp4', './../test/input/test3.mp4']
test_files = [os.path.abspath(file) for file in test_files]

for file in test_files:
    print('=' * 9, 'test success:', file, '=' * 9)
    video_out_path = f'./../test/output/{os.path.basename(file).split(".")[0]}.mp4'
    audio_out_path = f'./../test/output/{os.path.basename(file).split(".")[0]}.aac'
    merge_out_path = f'./../test/output/{os.path.basename(file).split(".")[0]}_merge.mp4'
    audio_and_video_separation(
        file,
        video_out_path=os.path.abspath(video_out_path),
        audio_out_path=os.path.abspath(audio_out_path),
    )
    print('=' * 9, 'copyonly', '=' * 9)
    audio_and_video_separation(
        file,
        video_out_path=os.path.abspath(video_out_path),
        audio_out_path=os.path.abspath(audio_out_path),
        is_copy_video=True,
    )
    print('=' * 9, 'merge', '=' * 9)
    audio_and_video_merge(
        video_out_path,
        audio_out_path,
        merge_out_path,
    )
    print('=' * 24)
