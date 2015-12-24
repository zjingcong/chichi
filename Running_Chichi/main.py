# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import ConfigParser
import logging
import os

import opening
from good_contact_wrapper import good_contact_wrapper


def init():
    win_x = 180
    win_y = 30
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_x, win_y)

    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")
    screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
    screen_h = int(conf.get("variable", "SCREEN_HIGH"))

    pygame.init()
    global screen
    screen = pygame.display.set_mode([screen_l, screen_h], 0, 32)
    pygame.display.set_caption("Running Chichi V1.0 By zjingcong")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Running_Chichi.log',
                        filemode='w')


def main():
    init()

    logging.info("===========Running Chichi BEGIN===========")
    open_window = opening.opening(screen)
    open_out = open_window.main()

    if open_out == "enter game":
        result = 0
        while result == 0:
            wrapper = good_contact_wrapper(screen)
            result = wrapper.main()

    logging.info("===========Running Chichi END===========")


if __name__ == '__main__':
    main()
