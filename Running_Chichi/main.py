# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import ConfigParser
import opening
import good_contact


def init():
    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")
    screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
    screen_h = int(conf.get("variable", "SCREEN_HIGH"))

    pygame.init()
    global screen
    screen = pygame.display.set_mode([screen_l, screen_h], 0, 32)
    pygame.display.set_caption("Running Chichi V1.0 By zjingcong")

    return


def main():
    init()
    # opening.opening(screen)
    good_contact.good_contact(screen)

if __name__ == '__main__':
    main()
