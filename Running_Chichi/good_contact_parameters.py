#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2015/12/22'

import logging

G = 0.0005

GROUND = 605
CEIL = 140
WALL_L = 0
WALL_R = 965     # 蒸笼的速度 # bug here: when laptop is charged, V is lower than it when laptop is uncharged

COLLISION_COEFFICIENT = 0.93
SPLIT_COEFFICIENT = 1.1

V0_RANGE = (0.1, 0.3)
X0_RANGE = (420, 580)
Y0_RANGE = (180, 200)
ANGLE_RANGE = (30, 150)
ERROR_T = (0, 30)
SPLIT_TIME = (3, 5)
NUM_RANGE = (1, 3)

NUM_RANGE_LARGE = (4, 6)

zhenglong_pic = (118, 118)
chichi_small_pic = (59, 47)

DEAD_ACTIVE = 17
DEAD_BLOCK = 10


class settingDic:
    def __init__(self):
        # v: 蒸笼的速度
        # bug here: when laptop is charged, V is lower than it when laptop is uncharged
        self.argv = {'tips': True, 'back': 1, 'sound': 1, 'v': 5}

    def get(self, name):
        if name in self.argv:
            return self.argv[name]
        else:
            logging.info("ERROR: [GET FAILURE] %s is not in setting_dic" % name)

    def set(self, name, value):
        if name in self.argv:
            self.argv[name] = value
        else:
            logging.info("ERROR: [SET FAILURE] %s is not in setting_dic" % name)

setting_dic = settingDic()
