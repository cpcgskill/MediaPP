# -*-coding:utf-8 -*-
"""
:创建时间: 2022/11/16 14:58
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
import shutil
import atexit

tmp_dir = './.media_pp'

is_initialized = False
is_auto_clean = False


def _get_mid_dir():
    global is_initialized
    if not is_initialized:
        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        if is_auto_clean:
            @atexit.register
            def clean_mid_dir():
                if os.path.isdir(tmp_dir):
                    shutil.rmtree(tmp_dir)

        is_initialized = True
    return tmp_dir


this_file_index = 0


def _get_mid_file_path(ext='txt', prefix='', suffix=''):
    global this_file_index
    try:
        return os.sep.join([
            _get_mid_dir(),
            '{}{}{}.{}'.format(prefix, this_file_index, suffix, ext),
        ])
    finally:
        this_file_index = this_file_index + 1


def _get_tmp_file_path(ext='txt', prefix='', suffix=''):
    return os.sep.join([
        _get_mid_dir(),
        '{}tmp{}.{}'.format(prefix, suffix, ext),
    ])


def _get_sub_dir_path():
    global this_file_index

    sub_dir_path = os.path.join(tmp_dir, '{}'.format(this_file_index))
    this_file_index = this_file_index + 1

    if not os.path.isdir(sub_dir_path):
        os.makedirs(sub_dir_path)
    return sub_dir_path
