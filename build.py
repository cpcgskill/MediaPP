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

import datetime
import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
import glob

if False:
    from typing import *


def command_exists(command):
    return shutil.which(command) is not None


def check_runtime():
    check_table = [
        (
            'clang++',
            (
                '无法找到clang++编译器，请安装clang++编译器\n'
                'clang++编译器下载地址: https://releases.llvm.org/download.html'
            ),
        ),
        (
            'windres',
            (
                '无法找到windres，请安装windres\n'
                'windres是mingw64的一部分，mingw64是一个windows下的gcc编译器\n'
                'mingw64下载地址: https://sourceforge.net/projects/mingw-w64/files/'
            ),
        ),
        (
            'makensis',
            (
                '无法找到makensis，请安装makensis\n'
                'makensis是一个windows下的安装包制作工具\n'
                'makensis下载地址: https://nsis.sourceforge.io/Download\n'
                'makensis下载地址2: https://sourceforge.net/projects/nsis/\n'
                '同时需要为其添加EnVar插件\n'
                'EnVar插件下载地址: https://nsis.sourceforge.io/EnVar_plug-in\n'
            )
        )
    ]
    full_error_message = ''
    for idx, (command, error_message) in enumerate(check_table):
        if not command_exists(command):
            full_error_message += '{}. {}\n{}\n'.format(idx + 1, command, error_message)

    if full_error_message != '':
        raise RuntimeError(full_error_message)


cache_dir = os.path.abspath(os.path.join(os.path.expanduser('~'), '.mediapp'))


def on_download_python():
    target_dir = os.path.abspath(os.path.join(cache_dir, 'pythons'))

    python_version = '.'.join([str(i) for i in sys.version_info[:3]])
    if sys.platform.startswith('linux'):
        raise NotImplementedError('Linux is not supported yet.')
    elif sys.platform.startswith('darwin'):
        raise NotImplementedError('MacOS is not supported yet.')
    elif sys.platform.startswith('win'):
        arch = 'amd64' if sys.maxsize > 2 ** 32 else 'win32'
        python_zip_name = f'python-{python_version}-embed-{arch}.zip'
        url = f'https://www.python.org/ftp/python/{python_version}/{python_zip_name}'
        target_file = os.path.join(target_dir, python_zip_name)
    else:
        raise NotImplementedError('Unknown platform.')
    print('Download Python from', url, 'to', target_file)

    # download python
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    if os.path.isfile(target_file):
        print('Python already downloaded.')
        return target_file

    print('Downloading Python...')
    urllib.request.urlretrieve(url, target_file + '.tmp')
    print('Downloading done.')

    shutil.move(target_file + '.tmp', target_file)

    return target_file


def on_download_get_pip_script():
    print('Get pip...')
    pip_path = os.path.abspath(os.path.join(cache_dir, 'get-pip.py'))
    if os.path.isfile(pip_path):
        print('Pip already downloaded.')
        return pip_path
    urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', pip_path)
    print('Get pip done.')
    return pip_path


def call_command(args, **kwargs):
    print(' '.join('"{}"'.format(i) for i in args))
    subprocess.run(args, **kwargs)


def main(app_name, version, author, main_script, icon_path, license_path, files, pip_index_url=None):
    check_runtime()

    #
    python_path = on_download_python()

    # download python
    PATH = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(PATH, 'build')
    out_path = os.path.join(build_path, 'out')
    tmp_path = os.path.join(build_path, 'tmp')

    if os.path.isdir(out_path):
        shutil.rmtree(out_path)
    os.makedirs(out_path)

    if os.path.isdir(tmp_path):
        shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

    print('Extracting python...')
    with zipfile.ZipFile(python_path, 'r') as zip_ref:
        zip_ref.extractall('build/out/')
    print('Extracting done.')

    pip_path = on_download_get_pip_script()

    print('Install pip...')
    call_command(['build/out/python.exe', pip_path, '--no-warn-script-location'])
    print('Install pip done.')

    pth_file = 'build/out/python{}{}._pth'.format(sys.version_info[0], sys.version_info[1])
    print('Edit', pth_file, '...')
    with open(pth_file, 'a', encoding='utf-8') as f:
        # f.writelines(['import site'])
        f.write('import site')
    print('Edit', pth_file, 'done.')

    print('Install pip...')
    if pip_index_url is None:
        call_command(
            [
                os.path.abspath('build/out/python.exe'), '-m',
                'pip', 'install', '-r', os.path.abspath('requirements.txt'),
                '--no-warn-script-location',
            ], env=os.environ
        )
    else:
        call_command(
            [
                os.path.abspath('build/out/python.exe'), '-m',
                'pip', 'install', '-r', os.path.abspath('requirements.txt'),
                '--no-warn-script-location'
                '--index-url', pip_index_url,
            ], env=os.environ
        )
    print('Install pip done.')

    print('Copy files...')
    for i in files:
        for j in glob.glob(i):
            if not os.path.isfile(j):
                continue
            if os.path.split(os.path.dirname(j))[-1] == '__pycache__':
                continue
            target = os.path.join(out_path, j)
            print('copy', j, 'to', target)
            if not os.path.isdir(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            shutil.copy(j, target)
    print('Copy files done.')

    print('Make exe...')
    with open('main.cpp', 'r', encoding='utf-8') as f:
        main_cpp = f.read()
        main_cpp = main_cpp.replace('{{{{script}}}}', main_script)

    cpp_code_path = os.path.join(tmp_path, 'main.cpp')
    with open(cpp_code_path, 'w', encoding='utf-8') as f:
        f.write(main_cpp)

    rc_code_path = os.path.join(tmp_path, 'appicon.rc')
    with open(rc_code_path, 'w', encoding='utf-8') as f:
        f.write('appicon ICON {}\n'.format(os.path.abspath(icon_path)))
    res_path = os.path.join(tmp_path, 'appicon.res')
    call_command(['windres', rc_code_path, '-o', res_path])

    #
    call_command([
        'clang++', cpp_code_path, res_path,
        # 最高级别优化
        '-O3',
        #
        '-o', os.path.join(out_path, app_name + '.exe'),
        '-Wl,/SUBSYSTEM:WINDOWS', '-static',
    ])
    print('Make exe done.')

    print('Make install package')
    call_command([
        'makensis',
        '/DI_VERSION_MAJOR={}'.format(version[0]),
        '/DI_VERSION_MINOR={}'.format(version[1]),
        '/DI_APP_NAME={}'.format(app_name),
        '/DI_AUTHOR={}'.format(author),
        '/DI_ICON={}'.format(os.path.abspath(icon_path)),
        '/DI_ICON_NAME={}'.format(os.path.basename(icon_path)),
        '/DI_LICENSE={}'.format(os.path.abspath(license_path)),
        'setup.nsi',
    ])
    print('Make install package done.', datetime.datetime.now())


if __name__ == '__main__':
    main(
        app_name='MediaPP',
        version=(1, 0),
        author='CangSpirit',
        main_script='run.py',
        icon_path='favicon.ico',
        license_path='LICENSE',
        files=[
            '*.py',
            '*.ico',
            'processor/*.py',
            'commands/*.py',
            'bin/*/*',
            'LICENSE',
            'README.md',
            'requirements.txt',
        ],
    )
