# -*-coding:utf-8 -*-
"""
:创建时间: 2022/11/16 14:36
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import io
import os
import shutil
import sys

from command import call_command
from processor._utils import _get_mid_file_path

sox_path = 'bin/sox/sox.exe'
if not os.path.isfile(sox_path):
    sys.exit(1)


def audio_gain(audio_path, multiple=3, audio_out_path=None):
    # type: (str, float, str) -> str
    """
    增益

    :param audio_path:
    :param multiple:
    :param audio_out_path:
    :return:
    """
    if audio_out_path is None:
        audio_out_path = _get_mid_file_path('wav')
    call_command([sox_path, '-v', '{}'.format(multiple), audio_path, audio_out_path])
    return audio_out_path


def audio_channel_count(audio_path):
    # type: (str) -> int
    """
    获取音频通道数

    :param audio_path:
    :return:
    """
    stdout = io.StringIO()
    call_command([sox_path, '--i', '-c', audio_path], stdout=stdout)
    return int(stdout.getvalue().strip())


def audio_noise_reduction(audio_path, strength=0.005, noise_audio_fpath=None, audio_out_path=None):
    # type: (str, float, str) -> str
    """
    自动降噪

    :param audio_path:
    :param strength:
    :param noise_audio_fpath:
    :param audio_out_path:
    :return:
    """
    noise_prof_out_path = _get_mid_file_path('prof')
    if audio_out_path is None:
        audio_out_path = _get_mid_file_path('wav')
    if noise_audio_fpath is None:
        noise_audio_fpath = audio_path
    tmp_noise_audio_fpath = _get_mid_file_path('wav')
    call_command([sox_path, noise_audio_fpath, '-c', '1', tmp_noise_audio_fpath])
    call_command([sox_path, tmp_noise_audio_fpath, '-n', 'noiseprof', noise_prof_out_path])


    channel_count = audio_channel_count(audio_path)
    if channel_count < 1:
        raise ValueError('channel_count < 1')
    processed_audio_out_path = []
    for i in range(channel_count):
        tmp_audio_path = _get_mid_file_path('wav')
        call_command([
            sox_path, audio_path, tmp_audio_path,
            'remix', '{}'.format(i + 1),
        ])
        sub_audio_out_path = _get_mid_file_path('wav')
        call_command([
            sox_path, tmp_audio_path, sub_audio_out_path,
            'noisered', noise_prof_out_path,
            '{}'.format(strength),
        ])
        processed_audio_out_path.append(sub_audio_out_path)

    if len(processed_audio_out_path)>1:
        call_command([
            sox_path, '-m', *processed_audio_out_path, audio_out_path,
        ])
    else:
        shutil.copy(processed_audio_out_path[0], audio_out_path)
    return audio_out_path


def audio_norm(audio_path, audio_out_path=None, db=-3):
    # sox.exe 5.wav output.wav gain -n -3
    if audio_out_path is None:
        audio_out_path = _get_mid_file_path('wav')
    call_command([
        sox_path, audio_path, audio_out_path,
        'gain', '-n', '{}'.format(db),
    ])
    return audio_out_path


def audio_bandpass_filter(audio_path, audio_out_path=None, low=100, high=3000):
    if audio_out_path is None:
        audio_out_path = _get_mid_file_path('wav')
    call_command([
        sox_path, audio_path, audio_out_path,
        'highpass', '{}'.format(low),
        'lowpass', '{}'.format(high),
    ])
    return audio_out_path
