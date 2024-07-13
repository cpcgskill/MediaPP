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

import enum
import json
import os
import sys
import time
import shutil

import pydantic
from typing import *
from command import call_command, call_command_return_str

PATH = os.path.abspath(os.path.dirname(__file__))
ffmpeg_bin_path = os.path.abspath(os.environ.get('FFMPEG_BIN_PATH', os.path.join(PATH, 'bin', 'ffmpeg')))
ffmpeg_path = os.path.join(ffmpeg_bin_path, 'ffmpeg.exe')
ffprobe_path = os.path.join(ffmpeg_bin_path, 'ffprobe.exe')

if not os.path.isfile(ffmpeg_path):
    ffmpeg_path = shutil.which('ffmpeg')
if not os.path.isfile(ffprobe_path):
    ffprobe_path = shutil.which('ffprobe')

if not os.path.isfile(ffmpeg_path):
    raise FileNotFoundError(ffmpeg_path)
if not os.path.isfile(ffprobe_path):
    raise FileNotFoundError(ffprobe_path)


def get_hwaccels():
    lines = call_command_return_str([ffmpeg_path, '-hwaccels']).splitlines()
    start_line_id = lines.index('Hardware acceleration methods:') + 1
    return [i for i in lines[start_line_id:] if i.strip() != '']


hwaccels = get_hwaccels()


class CoderType(enum.Enum):
    Video = 'V'
    Audio = 'A'
    Subtitle = 'S'


class Coder(pydantic.BaseModel):
    name: str
    coder_type: CoderType
    description: str


def get_encoders():
    lines = call_command_return_str([ffmpeg_path, '-encoders']).splitlines()
    lines = lines[lines.index('Encoders:') + 1:]
    lines = list(map(str.strip, lines))
    encoders = []
    for i in lines[lines.index('------') + 1:]:
        support, name, desc = i.split(' ', 2)
        if support[0] == 'V':
            coder_type = CoderType.Video
        elif support[0] == 'A':
            coder_type = CoderType.Audio
        elif support[0] == 'S':
            coder_type = CoderType.Subtitle
        else:
            continue
        encoders.append(Coder(name=name, coder_type=coder_type, description=desc))
    return encoders


encoders = get_encoders()


def get_decoders():
    lines = call_command_return_str([ffmpeg_path, '-decoders']).splitlines()
    lines = lines[lines.index('Decoders:') + 1:]
    lines = list(map(str.strip, lines))
    decoders = []
    for i in lines[lines.index('------') + 1:]:
        support, name, desc = i.split(' ', 2)
        if support[0] == 'V':
            coder_type = CoderType.Video
        elif support[0] == 'A':
            coder_type = CoderType.Audio
        elif support[0] == 'S':
            coder_type = CoderType.Subtitle
        else:
            continue
        decoders.append(Coder(name=name, coder_type=coder_type, description=desc))
    return decoders


decoders = get_decoders()


def get_formats(file):
    if not os.path.isfile(file):
        raise FileNotFoundError(file)
    streams = json.loads(call_command_return_str(
        [ffprobe_path,
         '-v', 'error',
         '-select_streams', 'v:0',
         '-show_entries', 'stream=codec_name',
         '-of', 'json',
         file]
    ))['streams']
    return streams[0]['codec_name']


def get_audio_streams(file):
    if not os.path.isfile(file):
        raise FileNotFoundError(file)
    # ffprobe -v error -select_streams a -show_entries stream=index -of json input.mp4
    streams = json.loads(call_command_return_str(
        [ffprobe_path,
         '-v', 'error',
         '-select_streams', 'a',
         '-show_format', '-show_streams',
         '-of', 'json',
         file]
    ))['streams']
    return streams


def get_video_duration(file):
    if not os.path.isfile(file):
        raise FileNotFoundError(file)
    # ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
    duration = json.loads(call_command_return_str(
        [ffprobe_path,
         '-v', 'error',
         '-show_entries', 'format=duration',
         '-of', 'json',
         file]
    ))['format']['duration']
    return float(duration)


class Accelerate(pydantic.BaseModel):
    hwaccel: Union[str, None] = None
    vide_decoder: Union[str, None] = None
    audio_decoder: Union[str, None] = None
    vide_encoder: Union[str, None] = None
    audio_encoder: Union[str, None] = None

    @staticmethod
    def best(in_format: str = None, out_format: str = None) -> 'Accelerate':
        """返回最好的硬件加速"""
        accelerate = Accelerate()

        if 'cuda' in hwaccels:
            accelerate.hwaccel = 'cuda'
            if in_format and in_format + '_cuvid' in [i.name for i in decoders if i.coder_type == CoderType.Video]:
                accelerate.vide_decoder = in_format + '_cuvid'
            if out_format and out_format + '_nvenc' in [i.name for i in encoders if i.coder_type == CoderType.Video]:
                accelerate.vide_encoder = out_format + '_nvenc'
        elif 'qsv' in hwaccels:
            accelerate.hwaccel = 'qsv'
            if in_format and in_format + '_qsv' in [i.name for i in decoders if i.coder_type == CoderType.Video]:
                accelerate.vide_decoder = in_format + '_qsv'
            if out_format and out_format + '_qsv' in [i.name for i in encoders if i.coder_type == CoderType.Video]:
                accelerate.vide_encoder = out_format + '_qsv'
        else:
            accelerate.hwaccel = 'auto'
        return accelerate

    @staticmethod
    def copyonly() -> 'Accelerate':
        return Accelerate(
            vide_encoder='copy',
            audio_encoder='copy',
        )

    def hwaccel_args(self) -> List[str]:
        if self.hwaccel is not None:
            return ['-hwaccel', self.hwaccel]
        return []

    def video_decoder_args(self) -> List[str]:
        if self.vide_decoder is not None:
            return ['-c:v', self.vide_decoder]
        return []

    def audio_decoder_args(self) -> List[str]:
        if self.audio_decoder is not None:
            return ['-c:a', self.audio_decoder]
        return []

    def video_encoder_args(self) -> List[str]:
        if self.vide_encoder is not None:
            return ['-c:v', self.vide_encoder]
        return []

    def audio_encoder_args(self) -> List[str]:
        if self.audio_encoder is not None:
            return ['-c:a', self.audio_encoder]
        return []


class GlobalOptions(pydantic.BaseModel):
    loglevel: Union[str, None] = None
    overwrite: bool = True

    def compute(self):
        args = []
        if self.loglevel is not None:
            args += ['-loglevel', self.loglevel]
        if self.overwrite:
            args += ['-y']
        else:
            args += ['-n']
        return args


video_support_ext = ['.mp4', '.kv', '.avi', '.mov', '.flv', '.wmv', '.webm']
audio_support_ext = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma', '.aac']


class InputFile(pydantic.BaseModel):
    path: str
    accelerate: Accelerate = Accelerate()
    options: List[str] = []

    def compute(self):
        args = self.accelerate.hwaccel_args()
        if os.path.splitext(self.path)[1] in video_support_ext:
            args += self.accelerate.video_decoder_args()
        elif os.path.splitext(self.path)[1] in audio_support_ext:
            args += self.accelerate.audio_decoder_args()
        for i in self.options:
            args += i.split()
        args += ['-i', self.path]
        return args


class OutputFile(pydantic.BaseModel):
    path: str
    accelerate: Accelerate = Accelerate()
    options: List[str] = []

    def compute(self):
        args = []
        if os.path.splitext(self.path)[1] in video_support_ext:
            args += self.accelerate.video_encoder_args()
        elif os.path.splitext(self.path)[1] in audio_support_ext:
            args += self.accelerate.audio_encoder_args()
        for i in self.options:
            args += i.split()
        args += [self.path]
        return args


class FFMpeg(pydantic.BaseModel):
    """
    ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...
    """
    accelerate: Accelerate = Accelerate()
    global_options: GlobalOptions = GlobalOptions()
    input_files: List[InputFile]
    process_options: List[str] = []
    output_files: List[OutputFile]

    def compute(self):
        accelerate = self.accelerate
        args = [ffmpeg_path]
        args += self.global_options.compute()
        for i in self.input_files:
            args += accelerate.hwaccel_args() + accelerate.video_decoder_args() + i.compute()
        args += self.process_options
        for i in self.output_files:
            args += accelerate.video_encoder_args() + i.compute()
        return args
