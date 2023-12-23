# -*-coding:utf-8 -*-
"""
:创建时间: 2023/12/23 21:01
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

from video import *
import sys



def process_file(video_path, output_dir):
    output_video_path = os.path.join(self.output_dir, os.path.basename(video_path))
    video_path, audio_path = audio_and_video_separation(video_path)

    audio_path = audio_noise_reduction(audio_path, strength=self.noise_reduction_strength)
    audio_path = audio_gain(audio_path, multiple=self.gain_multiple)

    audio_and_video_merge(
        audio_path,
        video_path,
        output_video_path,
    )


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    noise_reduction_strength = float(sys.argv[3])
    gain_multiple = int(sys.argv[4])
    support_ext = ['.mp4', '.kv', '.avi', '.mov', '.flv', '.wmv', '.webm']

    all_files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]
    all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in support_ext]
    for video_path in all_files:
        output_video_path = os.path.join(output_dir, os.path.basename(video_path))
        video_path, audio_path = audio_and_video_separation(video_path)

        audio_path = audio_noise_reduction(audio_path, strength=noise_reduction_strength)
        audio_path = audio_gain(audio_path, multiple=gain_multiple)

        audio_and_video_merge(
            audio_path,
            video_path,
            output_video_path,
        )