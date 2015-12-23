#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is for scratch card.

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2015/12/21'


import pygame
from numpy import *
import sys
import math


class scratch_card:
    def __init__(self, brush, length, width, pos, color, fluency, screen):
        self.screen = screen

        self.brush = brush
        self.length = length
        self.width = width
        self.pos = pos
        self.color = color
        self.fluency = fluency
        self.complete_status = False

        self.card_bound_x = (pos[0], pos[0] + length - 1)
        self.card_bound_y = (pos[1], pos[1] + width - 1)

        self.pos_last = (self.card_bound_x[0], self.card_bound_y[0])

        self.scratch = ones((length, width), dtype=bool)

    @staticmethod
    def _in_circle(x0, y0, r, x, y):
        l = math.pow((math.pow((x - x0), 2) + math.pow((y - y0), 2)), 0.5)
        if l <= r:
            return True
        else:
            return False

    @staticmethod
    def _interpolation(pos_1, pos_2, n):
        x1 = pos_1[0]
        x2 = pos_2[0]
        y1 = pos_1[1]
        y2 = pos_2[1]
        interval_x = int((x2 - x1) / n)
        interval_y = int((y2 - y1) / n)
        pos_list = []
        for i in range(n - 1):
            pos_x = interval_x * (i + 1) + x1
            pos_y = interval_y * (i + 1) + y1
            pos = (pos_x, pos_y)
            pos_list.append(pos)

        return pos_list

    def _delete(self, pos):
        if (pos[0] <= self.card_bound_x[1]) and (pos[0] >= self.card_bound_x[0]) \
                and (pos[1] <= self.card_bound_y[1]) and (pos[1] >= self.card_bound_y[0]):
                x0 = pos[0] - self.card_bound_x[0] - 1
                y0 = pos[1] - self.card_bound_y[0] - 1

                for i in range(x0 - self.brush, x0 + self.brush):
                    for j in range(y0 - self.brush, y0 + self.brush):
                        if self._in_circle(x0, y0, self.brush, i, j) \
                                and (i < self.length) and (i >= 0) and (j < self.width) and (j >= 0):
                            self.scratch[i][j] = False

    def fresh_status(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pos_last = pygame.mouse.get_pos()

    def display(self):
        if self.complete_status is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos_last = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0] != 0:
                pos = pygame.mouse.get_pos()
                pos_list = self._interpolation(self.pos_last, pos, self.fluency)
                self._delete(pos)
                for pos_interval in pos_list:
                    self._delete(pos_interval)
                self.pos_last = pos

            num = 0
            for i in range(self.length):
                for j in range(self.width):
                    if self.scratch[i][j]:
                        num += 1
                        x = i + self.card_bound_x[0]
                        y = j + self.card_bound_y[0]
                        self.screen.set_at([x, y], self.color)

            if num == 0:
                self.complete_status = True
                print "complete"


# scratch card class example
import ConfigParser


def example_init():
    pygame.init()

    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")

    screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
    screen_h = int(conf.get("variable", "SCREEN_HIGH"))
    screen = pygame.display.set_mode([screen_l, screen_h], 0, 32)
    pygame.display.set_caption("test: scratch card by zjingcong")

    scratch = scratch_card(20, 300, 200, (362, 250), [128, 128, 128], 5, screen)

    return screen, scratch


def example_layout(scratch, screen):
    while True:
        screen.fill([0, 0, 0])

        scratch.display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            scratch.fresh_status(event)

        pygame.display.update()


def example_main():
    screen, scratch = example_init()
    example_layout(scratch, screen)

'''
if __name__ == '__main__':
    example_main()
'''
