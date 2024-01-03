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

import os
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


def audio_noise_reduction(audio_path, strength=0.005, audio_out_path=None):
    # type: (str, float, str) -> str
    """
    自动降噪

    :param audio_path:
    :param strength:
    :param audio_out_path:
    :return:
    """
    noise_prof_out_path = _get_mid_file_path('prof')
    if audio_out_path is None:
        audio_out_path = _get_mid_file_path('wav')
    call_command([sox_path, audio_path, '-n', 'noiseprof', noise_prof_out_path])
    call_command([
        sox_path, audio_path, audio_out_path,
        'noisered', noise_prof_out_path,
        '{}'.format(strength),
    ])
    return audio_out_path
