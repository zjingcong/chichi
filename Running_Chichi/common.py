# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import os

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


# bug: sometimes the music don't play
class music:
    def __init__(self, music_path):
        self.track = pygame.mixer.music.load(music_path)
        pygame.time.delay(1000)

    def play(self):
        pygame.mixer.music.play(-1, 0.0)
        if pygame.mixer.music.get_busy() is True:
            print "Playing background music..."


class button:
    def __init__(self, button_path, x, y, l, w, screen):
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.screen = screen
        self.button_icon = pygame.image.load(button_path).convert_alpha()

    def put(self):
        self.screen.blit(self.button_icon, [self.x, self.y])

    def click(self, mouse_x, mouse_y):
        if (mouse_x > self.x) and (mouse_x < (self.x + self.l)) and (mouse_y > self.y) and (mouse_y < (self.y + self.w)):

            return True
