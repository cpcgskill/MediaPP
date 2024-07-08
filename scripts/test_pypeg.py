# -*-coding:utf-8 -*-
"""
:创建时间: 2024/5/19 17:34
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
import unittest

from pypeg import *


class TestPypeg(unittest.TestCase):
    def test_decode_encode(self):

        test_files = ['./../test/input/test.mp4', './../test/input/test2.mp4', './../test/input/test3.mp4'] * 2
        accelerates = []

        format = get_formats('./../test/input/test.mp4')
        print(format)
        accelerates.append(Accelerate.best(format, format))

        accelerates.append(Accelerate.copyonly())

        for accelerate in accelerates:
            print('=' * 9, 'test accelerate: ', accelerate, '=' * 9)
            time_consuming = 0.0
            for file in test_files:
                clock = time.time()
                ffmpeg = FFMpeg(
                    accelerate=accelerate,
                    global_options=GlobalOptions(),
                    input_files=[
                        InputFile(
                            path=file,
                        )
                    ],
                    process_options=[],
                    output_files=[
                        OutputFile(path='./../test/output/test.mp4')
                    ]
                )
                command = ffmpeg.compute()
                print(command)
                call_command_return_str(command)
                time_consuming += time.time() - clock
            print('time consuming:', time_consuming / len(test_files))

    def test_get_video_duration(self):
        from pypeg import get_video_duration
        # video_dir_list = ['./../test/input/']
        video_dir_list = [
            'C:\\Users\\cpcgs\\work\\record\\FixShape\\video\\01 GUI效果',
            'C:\\Users\\cpcgs\\work\\record\\FixShape\\video\\02 业务逻辑',
            'C:\\Users\\cpcgs\\work\\record\\FixShape\\video\\03 Maya部分开发',
            'C:\\Users\\cpcgs\\work\\record\\FixShape\\video\\04 收尾完善',
        ]
        video_list = []
        for video_dir in video_dir_list:
            for file in os.listdir(video_dir):
                if os.path.splitext(file)[-1] in video_support_ext:
                    video_list.append(os.path.join(video_dir, file))
        sum_duration = 0.0
        for video in video_list:
            duration = get_video_duration(video)
            print('video:', video, 'duration:', duration)
            sum_duration += duration
        print('sum_duration:', sum_duration)
