# -*-coding:utf-8 -*-
"""
:创建时间: 2024/1/19 23:58
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

根据当前系统环境自动下载对应的Python解释器

"""
from __future__ import unicode_literals, print_function, division

import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
import glob

if False:
    from typing import *

exe_name = 'MediaPP.exe'
main_script = 'gui.py'
files = [
    '*.py',
    '*.ico',
    'processor/*.py',
    'bin/*/*',
    'LICENSE',
    'README.md',
    'requirements.txt',

]
python_version = '.'.join([str(i) for i in sys.version_info[:3]])
if sys.platform.startswith('linux'):
    raise NotImplementedError('Linux is not supported yet.')
elif sys.platform.startswith('darwin'):
    raise NotImplementedError('MacOS is not supported yet.')
elif sys.platform.startswith('win'):
    arch = 'amd64' if sys.maxsize > 2 ** 32 else 'win32'
    url = f'https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-{arch}.zip'
else:
    raise NotImplementedError('Unknown platform.')
print(url)

# download python
PATH = os.path.dirname(os.path.abspath(__file__))
build_path = os.path.join(PATH, 'build')
out_path = os.path.join(build_path, 'out')
tmp_path = os.path.join(build_path, 'tmp')


if os.path.isdir(out_path):
    shutil.rmtree(out_path)
os.makedirs(out_path)

if not os.path.isdir(tmp_path):
    os.makedirs(tmp_path)

print('Downloading python...')
urllib.request.urlretrieve(url, 'build/tmp/python.zip')
print('Extracting python...')
with zipfile.ZipFile('build/tmp/python.zip', 'r') as zip_ref:
    zip_ref.extractall('build/out/')
os.remove('build/tmp/python.zip')
print('Downloading Done.')

print('get pip...')
urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'build/tmp/get-pip.py')
subprocess.run(['build/out/python.exe', 'build/tmp/get-pip.py'])
print('get pip Done.')

print('edit python310._pth...')
with open('build/out/python310._pth', 'a', encoding='utf-8') as f:
    # f.writelines(['import site'])
    f.write('import site')
print('edit python310._pth Done.')

print('install pip...')
subprocess.run([os.path.abspath('build/out/python.exe'), '-m', 'pip', 'install', '-r', os.path.abspath('requirements.txt')])
print('install pip Done.')

print('copy files...')
for i in files:
    for j in glob.glob(i):
        target = os.path.join(out_path, j)
        print('copy', j, 'to', target)
        if not os.path.isdir(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        shutil.copy(j, target)
print('copy files Done.')

print('make exe...')
with open('main.cpp', 'r', encoding='utf-8') as f:
    main_cpp = f.read()
    main_cpp = main_cpp.replace('{{{{script}}}}', main_script)

with open('build/tmp/main.cpp', 'w', encoding='utf-8') as f:
    f.write(main_cpp)

subprocess.run(['clang++', 'build/tmp/main.cpp', '-o', 'build/out/{exe_name}'.format(exe_name=exe_name)])
print('make exe Done.')

print('clean...')
shutil.rmtree(tmp_path)
print('clean Done.')