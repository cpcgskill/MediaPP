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

from pypeg import get_audio_streams
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
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    setting_path = sys.argv[3]

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
        raise ValueError('No files found in {}'.format(input_dir))

    video_audio_pair_list = []  # type: List[Tuple[str, str]] # video_path, audio_path
    for file in all_files:
        ext = os.path.splitext(file)[1]
        if ext in video_support_ext:
            if len(get_audio_streams(file)) == 0:
                video_path = file
                audio_path = None
            else:
                video_path, audio_path = audio_and_video_separation(file, is_copy_video=True)
                print('video_path', video_path)
        elif ext in audio_support_ext:
            video_path = None
            audio_path = file
        else:
            raise ValueError('Unknown file type: {}'.format(file))
        video_audio_pair_list.append((video_path, audio_path))

    # 预处理音频
    audio_index_path_list = [(idx, audio_path) for idx, (video_path, audio_path) in enumerate(video_audio_pair_list) if
                             audio_path is not None]
    processed_audio_path_list = audio_batch_process([audio_path for idx, audio_path in audio_index_path_list], setting)
    for (idx, _), processed_audio_path in zip(audio_index_path_list, processed_audio_path_list):
        video_audio_pair_list[idx] = (video_audio_pair_list[idx][0], processed_audio_path)

    # 合并音频
    for orig_media_path, (video_path, audio_path) in zip(all_files, video_audio_pair_list):
        print('processing', video_path, audio_path)
        # 分别处理视频和音频， 如果有一个为None则直接复制， 否则合并
        output_path = os.path.join(output_dir, os.path.basename(orig_media_path))
        if video_path is None:
            shutil.copy(audio_path, output_path)
        elif audio_path is None:
            shutil.copy(video_path, output_path)
        else:
            audio_and_video_merge(audio_path, video_path, output_path)
