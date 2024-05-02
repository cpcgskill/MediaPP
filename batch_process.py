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
from processor.DTLN import DTLN_batch_process
from processor._utils import _get_mid_file_path
from setting import Setting
import sys

video_support_ext = ['.mp4', '.kv', '.avi', '.mov', '.flv', '.wmv', '.webm']
audio_support_ext = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma']


def audio_batch_process(input_files, setting):
    # type: (List[str], Setting) -> List[str]

    print('setting', setting)
    # files = DTLN_batch_process(input_files)
    output_files = []
    for audio_path in input_files:
        print('processing', audio_path)
        if setting.noise_file_path is not None:
            audio_path = audio_noise_reduction(audio_path,
                                               strength=setting.noise_reduction_strength,
                                               noise_audio_fpath=setting.noise_file_path,
                                               )
        audio_path = audio_norm(audio_path, db=setting.norm_dB)
        audio_path = audio_bandpass_filter(
            audio_path,
            low=setting.bandpass_filter_low,
            high=setting.bandpass_filter_high,
        )
        output_files.append(audio_path)
    return DTLN_batch_process(output_files)


if __name__ == '__main__':
    typ = sys.argv[1]
    input_dir = sys.argv[2]
    output_dir = sys.argv[3]
    setting_path = sys.argv[4]

    if not os.path.isfile(setting_path):
        raise ValueError('Setting file not found: {}'.format(setting_path))
    if not os.path.isdir(input_dir):
        raise ValueError('Input dir not found: {}'.format(input_dir))
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    with open(setting_path, 'r', encoding='utf-8') as f:
        setting = Setting.model_validate_json(f.read())
    if setting.noise_file_path is not None:
        if os.path.splitext(setting.noise_file_path)[1] in video_support_ext:
            _, setting.noise_file_path = audio_and_video_separation(setting.noise_file_path)
        tmp_noise_file_path = _get_mid_file_path(os.path.splitext(setting.noise_file_path)[1])
        shutil.copy(setting.noise_file_path, tmp_noise_file_path)
        setting.noise_file_path = tmp_noise_file_path

    all_files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]
    if len(all_files) == 0:
        sys.exit(0)
    if typ == 'video':
        all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in video_support_ext]
        names = [os.path.basename(i) for i in all_files]

        video_paths, audio_paths = zip(*[audio_and_video_separation(i) for i in all_files])
        audio_paths = audio_batch_process(audio_paths, setting)
        for name, video_path, audio_path in zip(names, video_paths, audio_paths):
            output_video_path = os.path.join(output_dir, name)
            audio_and_video_merge(
                audio_path,
                video_path,
                output_video_path,
            )
    elif typ == 'audio':
        all_files = [i for i in all_files if os.path.isfile(i) and os.path.splitext(i)[1] in audio_support_ext]
        names = [os.path.basename(i) for i in all_files]

        audio_paths = audio_batch_process(all_files, setting)

        for name, audio_path in zip(names, audio_paths):
            output_audio_path = os.path.join(output_dir, name)
            shutil.copy(audio_path, output_audio_path)
    else:
        raise ValueError('Unknown type: {}'.format(typ))
