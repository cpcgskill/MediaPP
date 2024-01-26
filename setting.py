# -*-coding:utf-8 -*-
"""
:创建时间: 2024/1/12 0:16
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import enum
from typing import *

import dataclasses
import json
import pydantic


class Theme(enum.Enum):
    AUTO = 'Auto'
    DARK = 'Dark'
    LIGHT = 'Light'


class Setting(pydantic.BaseModel):
    theme: Theme = Theme.AUTO
    noise_file_path: Optional[str] = None
    noise_reduction_strength: float = 0.3
    norm_dB: int = -3
    bandpass_filter_low: int = 100
    bandpass_filter_high: int = 3000


__all__ = ['Setting', 'Theme']

if __name__ == '__main__':
    print(Setting(theme=Theme.DARK).model_dump_json())
    Setting.model_validate_json(json.dumps({'theme': 'Dark'}))
