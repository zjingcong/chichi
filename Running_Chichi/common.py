# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import os
import logging

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


class music:
    def __init__(self, music_path):
        self.track = pygame.mixer.music.load(music_path)
        # pygame.time.delay(1000)

    def play(self, mod=-1, start=0.0):
        pygame.mixer.music.play(mod, start)

    # mod = 1: fadeout
    def stop(self, mod=1):
        if mod == 1:
            pygame.mixer.music.fadeout(1200)


class animation:
    class frame:
        def __init__(self, image, pos, num):
            self.image = image
            self.pos = pos
            self.num = num

    # frame_image_list example:
    # [{'image': image_path, 'pos': (pos_x, pos_y)}, ...]
    # mod: 'endless', 'normal', 'stop'
    def __init__(self, frame_image_list, interval, mod, screen):
        self.frame_num = len(frame_image_list)
        self.interval = interval
        self.screen = screen
        self.mod = mod

        self.clock = interval
        self.current_frame = 0
        self.frame_list = self._init_frame_list(frame_image_list)

    def _init_frame_list(self, frame_image_list):
        frame_list = []
        for i in range(self.frame_num):
            frame = self.frame(frame_image_list[i]['image'], frame_image_list[i]['pos'], i)
            frame_list.append(frame)

        return frame_list

    def display(self):
        if self.mod == 'stop':
            return

        self.clock -= 1
        if self.clock == 0:
            self.clock = self.interval
            self.current_frame += 1
            logging.info("DISPLAY FRAME %d" % self.current_frame)

        if self.mod == 'endless':
            if self.current_frame >= self.frame_num:
                self.current_frame = 0
            frame = self.frame_list[self.current_frame]
            self.screen.blit(frame.image, [frame.pos[0], frame.pos[1]])

        elif self.mod == 'normal':
            if self.current_frame < self.frame_num:
                frame = self.frame_list[self.current_frame]
                self.screen.blit(frame.image, [frame.pos[0], frame.pos[1]])
            else:
                self.mod = 'stop'
        else:
            logging.info("ERROR: No such animation mod.")

# animation class example
import ConfigParser
import sys


def example_init():
    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")
    image_path = str(conf.get("path", "IMAGE_PATH"))
    current_dir = CURRENT_DIR

    screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
    screen_h = int(conf.get("variable", "SCREEN_HIGH"))
    screen = pygame.display.set_mode([screen_l, screen_h], 0, 32)
    pygame.display.set_caption("test: animation by zjingcong")

    logo = pygame.image.load("%s%slogo.png" % (current_dir, image_path)).convert_alpha()
    frame_1 = pygame.transform.rotate(logo, 20)
    frame_2 = pygame.transform.rotate(logo, -20)
    frame_iamge_list = [{'image': frame_1, 'pos': (130, -55)}, {'image': frame_2, 'pos': (130, -55)}]

    anim = animation(frame_iamge_list, 10, 'endless', screen)

    return screen, anim


def example_display(screen, anim):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill([255, 255, 255])
        anim.display()

        pygame.display.update()


def example_main():
    screen, anim = example_init()
    example_display(screen, anim)

'''
if __name__ == '__main__':
    example_main()
'''


class button:
    def __init__(self, button_up_path, button_down_path, output, x, y, l, w, screen):
        self._x = x
        self._y = y
        self._l = l
        self._w = w
        self._screen = screen
        self._button_icon_up = pygame.image.load(button_up_path).convert_alpha()
        self._button_icon_down = pygame.image.load(button_down_path).convert_alpha()
        self.output = output

        self.icon = self._button_icon_up
        self.mouse_pos = (-1, -1)
        self.mouse_status = 'up'
        self.status = -1    # 0: 未触发, 1: down, 0: up
        self.out = False

    def _mouse_on_button(self):
        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]
        if (mouse_x > self._x) and (mouse_x < (self._x + self._l)) \
                and (mouse_y > self._y) and (mouse_y < (self._y + self._w)):
            return True
        else:
            return False

    def mouse_detection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_status = 'down'
            self.mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_status = 'up'
            self.mouse_pos = pygame.mouse.get_pos()

    # mod: 1 mouse up, button up, mod: 0 mouse up, button stay the same
    def button_fresh(self, mod=1):
        if self.status == -1 and self.mouse_status == 'down' and self._mouse_on_button():
            self.status = 1
            self.icon = self._button_icon_down
        elif self.status == 1 and self.mouse_status == 'up' and self._mouse_on_button():
            self.status = 0
            if mod == 1:
                self.icon = self._button_icon_up
            elif mod == 0:
                self.icon = self._button_icon_down

    def button_layout(self):
        self._screen.blit(self.icon, [self._x, self._y])
        if self.status == 0:
            self._button_out()

    def _button_out(self):
        self.out = True
