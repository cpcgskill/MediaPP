# -*-coding:utf-8 -*-
"""
:创建时间: 2022/11/16 23:58
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import cv2 as cv

from blind_watermark import WaterMark
from command import call_command
from processor._utils import _get_tmp_file_path, _get_mid_file_path, _get_mid_dir


def remake_video(video_file_path, out_video, key):
    cap = cv.VideoCapture(video_file_path)
    out = cv.VideoWriter(
        out_video,
        cv.VideoWriter_fourcc(*'MJPG'),
        int(cap.get(cv.CAP_PROP_FPS)),
        (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))),
    )

    i = 0
    while cap.isOpened():
        i = i + 1

        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = key(i, frame)
        out.write(frame)
    cap.release()
    out.release()


def loop_video(video_file_path, key):
    cap = cv.VideoCapture(video_file_path)

    i = 0
    while cap.isOpened():
        i = i + 1

        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        key(i, frame)
    cap.release()


def write_blind_watermark(video_file_path, data, start_frame=5, interval=1000, out_video=None):
    password = 1
    if out_video is None:
        out_video = _get_mid_file_path('mp4')

    def _write_blind_watermark(i, frame):
        if (i % interval) == start_frame:
            bwm1 = WaterMark(password_img=int(password), password_wm=int(password))

            cv.imwrite(_get_tmp_file_path('png'), frame)
            bwm1.read_img(_get_tmp_file_path('png'))
            # bwm1.read_img(img=frame)
            bwm1.read_wm(data, mode='str')
            bwm1.embed(_get_tmp_file_path('png'))
            frame = cv.imread(_get_tmp_file_path('png'), flags=cv.IMREAD_UNCHANGED)
            print('frame {frame}: wm_size {wm_size}'.format(frame=i, wm_size=bwm1.wm_size))
        return frame

    remake_video(video_file_path, out_video, key=_write_blind_watermark)
    return out_video


def read_blind_watermark(video_file_path, wm_size, start_frame=1):
    password = 1
    call_command([ffmpeg_path, '-ss', '1', '-i', video_file_path, '-y',
                  _get_mid_dir()+'/tmp_%d.png'
                  ])

    def _read_blind_watermark(i, frame):
        if i >= start_frame:
            bwm1 = WaterMark(password_img=int(password), password_wm=int(password))
            # cv.imwrite(_get_tmp_file_path('png', prefix='read_'), frame)
            try:
                wm_extract = bwm1.extract(filename=_get_mid_dir()+'/tmp_{}.png'.format(i),
                                          wm_shape=wm_size, mode='str')
                print('frame {frame} data:'.format(frame=i), wm_extract)
            except ValueError as ex:
                print('frame {frame} error:'.format(frame=i), ex)

    loop_video(video_file_path, key=_read_blind_watermark)

# from blind_watermark import WaterMark
#
# bwm1 = WaterMark(password_img=1, password_wm=1)
# img = bwm1.read_img('test.png')
# wm = '@guofei9987 开源万岁！'
# bwm1.read_wm(wm, mode='str')
# eimg = bwm1.embed('test_out.png')
# len_wm = len(bwm1.wm_bit)
# print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))


# in_img = cv2.imread(in_img, flags=cv2.IMREAD_UNCHANGED)
# cv2.read
#
# wm_extract = bwm1.extract(embed_img=out_img, wm_shape=len_wm, mode='str')
# print(wm_extract)
#
# end2_time = time.time()
# print('解密耗时:', end2_time-end_time)
