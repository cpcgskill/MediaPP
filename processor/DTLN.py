# -*-coding:utf-8 -*-
"""
:创建时间: 2024/1/23 3:20
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import shutil

if False:
    from typing import *
import os
import sys

from command import call_command
from processor._utils import _get_sub_dir_path

eval_path = 'bin/DTLN/run_evaluation.py'
model_path = 'bin/DTLN/DTLN_norm_500h.h5'

if not os.path.isfile(eval_path) or not os.path.isfile(model_path):
    sys.exit(1)


def DTLN_batch_process(input_files):
    in_tmp_dir = _get_sub_dir_path()
    out_tmp_dir = _get_sub_dir_path()
    in_files = []
    for i in input_files:
        if os.path.isfile(i):
            in_files.append(shutil.copy(i, in_tmp_dir))
    call_command([sys.executable, eval_path, '-i', in_tmp_dir, '-o', out_tmp_dir, '-m', model_path])
    return [os.path.join(out_tmp_dir, os.path.basename(i)) for i in in_files]
