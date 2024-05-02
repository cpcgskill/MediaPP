# -*-coding:utf-8 -*-
"""
:创建时间: 2024/4/28 21:22
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

from processor.ffmpeg import add_image_watermark, audio_and_video_separation, audio_and_video_merge
from processor._utils import _get_mid_file_path
from setting import Setting
import sys, os

video_support_ext = ['.mp4', '.kv', '.avi', '.mov', '.flv', '.wmv', '.webm']

if __name__ == '__main__':
    image_file_path = sys.argv[1]
    input_dir = sys.argv[2]
    location = sys.argv[3]
    output_dir = sys.argv[4]
    setting_path = sys.argv[5]

    if not os.path.isfile(setting_path):
        raise ValueError('Setting file not found: {}'.format(setting_path))
    with open(setting_path, 'r', encoding='utf-8') as f:
        setting = Setting.model_validate_json(f.read())
    if not os.path.isfile(image_file_path):
        raise ValueError('Image file not found: {}'.format(image_file_path))
    if not os.path.isdir(input_dir):
        raise ValueError('Input dir not found: {}'.format(input_dir))
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    all_files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]
    files = [i for i in all_files if os.path.splitext(i)[1] in video_support_ext]

    for video_path in files:
        print('processing', video_path)

        add_image_watermark(video_path, image_file_path, location, os.path.join(output_dir, os.path.basename(video_path)))
