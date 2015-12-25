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

    def music_play(self, mod=-1, start=0.0, volume=1):
        pygame.mixer.music.play(mod, start)
        self.set_music_volume(volume)

    # mod = 1: fadeout, mod = 0: stop
    def music_stop(self, mod=1):
        if mod == 1:
            pygame.mixer.music.fadeout(1200)
        if mod == 0:
            pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

# test for music
import ConfigParser
import os
import sys
from pygame.locals import *


def music_init():
    pygame.init()
    current_dir = os.path.split(os.path.abspath(__file__))[0]

    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")
    tone_path = str(conf.get("path", "TONE_PATH"))

    screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
    screen_h = int(conf.get("variable", "SCREEN_HIGH"))
    screen = pygame.display.set_mode([screen_l, screen_h], 0, 32)
    pygame.display.set_caption("test: music by zjingcong")

    music1_path = "%s%sgood contact.mp3" % (current_dir, tone_path)
    music2_path = "%s%sopening.mp3" % (current_dir, tone_path)

    pygame.time.delay(1000)

    pygame.mixer.music.load(music1_path)
    pygame.mixer.music.play(-1, 0.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "lalala"
                pygame.mixer.music.pause()
                # pygame.mixer.music.load(music2_path)
                # pygame.mixer.music.play(-1, 0.0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.mixer.music.unpause()

'''
if __name__ == '__main__':
    music_init()
'''


class sound(object):
    def __init__(self, path):
        pygame.mixer.init()
        pygame.time.delay(1000)

        self.path = path

    def init_sound(self):
        self.sound = pygame.mixer.Sound(self.path)

    # ch_mod = 2: volume change with position_x, ch_mod = -1: left channel, ch_mod = 1: right channel, ch_mod = 0: both
    def sound_play(self, mod=0, start=0.0, ch_mod=0, pos_x=-1, width_x=-1, volume=1):
        channel = self.sound.play(mod, int(start))
        if ch_mod == -1:
            channel.set_volume(1 * volume, 0)
        elif ch_mod == 1:
            channel.set_volume(0, 1 * volume)
        elif ch_mod == 0:
            channel.set_volume(1 * volume, 1 * volume)
        elif ch_mod == 2:
            left, right = self._sound_channel_volume(pos_x, width_x)
            channel.set_volume(left * volume, right * volume)

    @staticmethod
    def _sound_channel_volume(pos_x, width_x):
        right_volume = float(pos_x) / width_x
        left_volume = 1.0 - right_volume

        return left_volume, right_volume

    # mod: 0 set the volume with playing 1: without
    def set_sound_volume(self, volume, mod=0):
        if mod == 0:
            self.sound.play()
            self.sound.set_volume(volume)
        elif mod == 1:
            self.sound.set_volume(volume)
