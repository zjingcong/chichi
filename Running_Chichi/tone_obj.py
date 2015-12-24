#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2015/12/24'

import pygame


class music(object):
    def __init__(self, path):
        pygame.mixer.init()
        pygame.time.delay(1000)

        self.path = path

    def init_music(self):
        pygame.mixer.music.load(self.path)

    def music_play(self, mod=-1, start=0.0):
        pygame.mixer.music.play(mod, start)

    # mod = 1: fadeout, mod = 0: stop
    def music_stop(self, mod=1):
        if mod == 1:
            pygame.mixer.music.fadeout(1200)
        if mod == 0:
            pygame.mixer.music.stop()


class sound(object):
    def __init__(self, path):
        pygame.mixer.init()
        pygame.time.delay(1000)

        self.path = path

    def init_sound(self):
        self.sound = pygame.mixer.Sound(self.path)

    # ch_mod = 2: volume change with position_x, ch_mod = -1: left channel, ch_mod = 1: right channel, ch_mod = 0: both
    def sound_play(self, mod=0, start=0.0, ch_mod=0, pos_x=-1, width_x=-1):
        channel = self.sound.play(mod, int(start))
        if ch_mod == -1:
            channel.set_volume(1, 0)
        elif ch_mod == 1:
            channel.set_volume(0, 1)
        elif ch_mod == 0:
            channel.set_volume(1, 1)
        elif ch_mod == 2:
            left, right = self._sound_channel_volume(pos_x, width_x)
            channel.set_volume(left, right)

    @staticmethod
    def _sound_channel_volume(pos_x, width_x):
        right_volume = float(pos_x) / width_x
        left_volume = 1.0 - right_volume

        return left_volume, right_volume
