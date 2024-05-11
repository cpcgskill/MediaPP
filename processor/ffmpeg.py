# -*-coding:utf-8 -*-
"""
:创建时间: 2022/11/16 14:25
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import os
import sys
from typing import *
from command import call_command
from processor._utils import _get_mid_file_path

ffmpeg_path = 'bin/ffmpeg/ffmpeg.exe'
if not os.path.isfile(ffmpeg_path):
    sys.exit(1)


def audio_and_video_separation(
        video_file_path,
        video_out_path=None, audio_out_path=None,
        is_copy_video=False,
):
    # type: (str, str, str, bool) -> (str, str)
    """
    分离音频和视频

    :param video_file_path:
    :param video_out_path:
    :param audio_out_path:
    :param is_copy_video:
    :return:
    """
    if video_out_path is None:
        video_out_path = _get_mid_file_path('mp4')
    aac_audio_out_path = _get_mid_file_path('aac')
    if audio_out_path is None:
        audio_out_path = _get_mid_file_path('wav')
    call_command(
        [ffmpeg_path, '-i', video_file_path, '-an', '-y'] +
        (['-c:v', 'copy'] if is_copy_video else [])
        + [video_out_path]
    )
    call_command([ffmpeg_path, '-i', video_file_path, '-vn', '-y', aac_audio_out_path])
    call_command([ffmpeg_path, '-i', aac_audio_out_path, '-vn', '-y', audio_out_path])
    return video_out_path, audio_out_path


def audio_and_video_merge(audio_file_path, video_file_path, video_out_path=None):
    """
    合并音频和视频

    :param audio_file_path:
    :param video_file_path:
    :param video_out_path:
    :return:
    """
    if video_out_path is None:
        video_out_path = _get_mid_file_path('mp4')
    call_command([
        ffmpeg_path, '-i', video_file_path,
        '-i', audio_file_path,
        '-y', '-c:v', 'copy', '-c:a',
        'aac', '-strict', 'experimental', video_out_path,
    ])
    return video_out_path


def add_background_music(video_file_path, background_music_file_path, background_music_strength=0.01,
                         video_out_path=None):
    """
    添加背景音乐

    :param video_file_path:
    :param background_music_file_path:
    :param background_music_strength:
    :param video_out_path:
    :return:
    """
    if video_out_path is None:
        video_out_path = _get_mid_file_path('mp4')
    call_command([
        ffmpeg_path,
        '-i', video_file_path,
        '-i', background_music_file_path,
        '-filter_complex',
        #                                             下面是强度
        '[1:a]aloop=loop=-1:size=2e+09[out];[out]volume={}[out];[out][0:a]amix'.format(background_music_strength),

        '-shortest', '-y', '-c:v', 'copy', video_out_path,
    ])
    return video_out_path


def add_image_watermark(
        video_file_path,
        image_file_path,
        location='left-top',
        video_out_path=None,
):
    """
    添加图片水印

    :param video_file_path:
    :param image_file_path:
    :type location: str
    :param location:  ['left-top', 'left-bottom', 'right-top', 'right-bottom']
    :param video_out_path:
    :return:
    """
    if video_out_path is None:
        video_out_path = _get_mid_file_path('mp4')
    # old = 'overlay=x=0:y=H-h'
    overlay_str = 'overlay='
    if location == 'left-top':
        overlay_str += 'x=0:y=0'
    elif location == 'left-bottom':
        overlay_str += 'x=0:y=H-h'
    elif location == 'right-top':
        overlay_str += 'x=W-w:y=0'
    elif location == 'right-bottom':
        overlay_str += 'x=W-w:y=H-h'
    else:
        raise ValueError('location must be one of ["left-top", "left-bottom", "right-top", "right-bottom"]')
    call_command([
        ffmpeg_path,
        '-hwaccel', 'auto',
        '-i', video_file_path,
        '-i', image_file_path,
        '-filter_complex', overlay_str,
        '-shortest', '-y', video_out_path,
    ])
    return video_out_path


def add_text_watermark(
        video_file_path,
        text,
        font_point=(0, 0),
        font_size=30,
        font_file='lazy.ttf',
        font_color='808080',
        font_alpha=0.2,
        video_out_path=None,
):
    """
    添加文字水印

    :param video_file_path:
    :param text:
    :param font_point:
    :param font_size:
    :param font_file:
    :param font_color:
    :param font_alpha:
    :param video_out_path:
    :return:
    """
    text = text.replace(':', '\\:')
    if video_out_path is None:
        video_out_path = _get_mid_file_path('mp4')
    call_command([
        ffmpeg_path,
        '-i', video_file_path,
        '-vf',
        (
            f"drawtext="
            f"fontsize={font_size}:"
            f"fontfile={font_file}:"
            f"text='{text}':"
            f"x={font_point[0]}:"
            f"y={font_point[1]}:"
            f"fontcolor={font_color}@{font_alpha}"
        ),
        video_out_path,
    ])
    return video_out_path
