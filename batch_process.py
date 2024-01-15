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
from processor.sox import *
import sys

video_support_ext = ['.mp4', '.kv', '.avi', '.mov', '.flv', '.wmv', '.webm']
audio_support_ext = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma']

if __name__ == '__main__':
    typ = sys.argv[1]
    input_dir = sys.argv[2]
    output_dir = sys.argv[3]
    noise_reduction_strength = float(sys.argv[4])
    norm_dB = int(sys.argv[5])
    noise_file_path = sys.argv[6]
    if noise_file_path == '':
        noise_file_path = None
    else:
        if os.path.splitext(noise_file_path)[1] in video_support_ext:
            _, noise_file_path = audio_and_video_separation(noise_file_path)

    if typ == 'video':
        all_files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]
        all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in video_support_ext]
        for video_path in all_files:
            output_video_path = os.path.join(output_dir, os.path.basename(video_path))
            video_path, audio_path = audio_and_video_separation(video_path)

            audio_path = audio_noise_reduction(audio_path,
                                               strength=noise_reduction_strength,
                                               noise_audio_fpath=noise_file_path,
                                               )
            audio_path = audio_norm(audio_path, db=norm_dB)
            audio_path = audio_bandpass_filter(audio_path, low=100, high=3000)

            audio_and_video_merge(
                audio_path,
                video_path,
                output_video_path,
            )
    elif typ == 'audio':
        all_files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]
        all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in audio_support_ext]

        for audio_path in all_files:
            output_audio_path = os.path.join(output_dir, os.path.basename(audio_path))
            audio_path = audio_noise_reduction(audio_path,
                                               strength=noise_reduction_strength,
                                               noise_audio_fpath=noise_file_path,
                                               )
            # audio_gain(audio_path, multiple=gain_multiple, audio_out_path=output_audio_path)
            audio_path = audio_norm(audio_path, db=norm_dB)
            audio_path = audio_bandpass_filter(audio_path, low=100, high=3000, audio_out_path=output_audio_path)

    else:
        raise ValueError('Unknown type: {}'.format(typ))
