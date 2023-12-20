# -*-coding:utf-8 -*-
from __future__ import unicode_literals, print_function, division

import datetime
import os
import random

from processor.ffmpeg import audio_and_video_separation, audio_and_video_merge, add_background_music, \
    add_image_watermark, add_text_watermark
from processor.sox import audio_gain, audio_noise_reduction


def video_base_build(video_path, video_out_path):
    video_path = add_image_watermark(video_path, './logo.png')
    video_path, audio_path = audio_and_video_separation(video_path, is_copy_video=True)

    audio_path = audio_gain(audio_path, multiple=3)
    audio_path = audio_noise_reduction(audio_path, strength=0.005)

    video_path = audio_and_video_merge(audio_path, video_path)
    video_path = add_background_music(video_path, 'E:\\audio\\Bonfire.mp3',
                                      background_music_strength=0.001,
                                      video_out_path=video_out_path)
    return video_path


def video_text_watermark_build(video_path, video_out_path, note=""):
    video_path = add_text_watermark(
        video_path,
        "build time {}: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), note),
        font_point=(100 + random.randint(0, 30), 100 + random.randint(0, 30)),
        font_size=25,
        font_alpha=0.13,
        video_out_path=video_out_path,
    )
    return video_path


def child_files(path):
    path = os.path.abspath(path)
    path_len = len(path.split(os.sep))
    for root, dis, files in os.walk(path):
        for file in files:
            file = os.sep.join([root, file])
            yield os.sep.join(file.split(os.sep)[path_len:])


def all_video_base_build():
    for f in child_files('./video'):
        video_base_build(os.sep.join(['./video', f]), os.sep.join(['./video_out', f]))


def build_main():
    in_dir = './video_out'
    source_files = list(child_files(in_dir))
    target_dir = './video_out_main'
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    for f in source_files:
        video_text_watermark_build(os.sep.join([in_dir, f]),
                                   os.sep.join([target_dir, f]),
                                   note=f'Main, format version 1')


def build_chapter_one(count):
    in_dir = './video_out'
    source_files = list(child_files(in_dir))[:23]
    target_dir = 'video_out_chapter_one_v1'
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    i = 0
    for _ in range(count):

        out_dir = f'{target_dir}/index_{i}'
        while os.path.isdir(out_dir):
            i = i + 1
            out_dir = f'{target_dir}/index_{i}'

        print('build to', out_dir)
        os.mkdir(out_dir)

        for f in source_files:
            # video_base_build(os.sep.join([in_dir, f]),
            #                  os.sep.join([out_dir, f]),
            #                  note=f'Chapter One, release index {i}, format version 1')
            video_text_watermark_build(os.sep.join([in_dir, f]),
                                       os.sep.join([out_dir, f]),
                                       note=f'Chapter One, release index {i}, format version 1')


if __name__ == '__main__':
    all_video_base_build()
    # build_chapter_one(2)
    build_main()
