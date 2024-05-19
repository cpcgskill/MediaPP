# -*-coding:utf-8 -*-
"""
:创建时间: 2022/11/16 13:54
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
import subprocess


def call_command(args, stdout=None, print_to_stdout=True):
    if print_to_stdout:
        print(*args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 实时读取输出并写入IO流
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            if output.endswith(b'\r\n'):
                output = output[:-2]
            elif output.endswith(b'\n') or output.startswith(b'\r'):
                output = output[:-1]
            try:
                output = output.decode('utf-8')
            except UnicodeDecodeError:
                output = output.decode('gbk')
            if print_to_stdout:
                print(output)
            if stdout is not None:
                stdout.write(output+'\n')
    if process.returncode == 0:
        return 0
    else:
        raise subprocess.CalledProcessError(process.returncode, args)


def call_command_return_str(args):
    stdout = io.StringIO()
    call_command(args, stdout, print_to_stdout=False)
    return stdout.getvalue()
