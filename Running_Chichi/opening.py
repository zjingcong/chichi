# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import ConfigParser
import common
import sys


class opening:
    def __init__(self, screen):
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        image_path = str(conf.get("path", "IMAGE_PATH"))
        tone_path = str(conf.get("path", "TONE_PATH"))
        button_path = str(conf.get("path", "BUTTON_PATH"))
        current_dir = common.CURRENT_DIR

        self.screen = screen
        self.music_path = "%s%sopening.mp3" % (current_dir, tone_path)
        self.background_map = pygame.image.load("%s%sfood_map.jpg" % (current_dir, image_path)).convert()
        self.logo = pygame.image.load("%s%slogo.png" % (current_dir, image_path)).convert_alpha()
        self.title = pygame.image.load("%s%stitle.png" % (current_dir, image_path)).convert_alpha()

        self.music = common.music(self.music_path)
        self.button = common.button("%s%splaying.png" % (current_dir, button_path), 362, 590, 300, 100, screen)

        self.main()

    def display(self):
        self.screen.blit(self.background_map, [0, 0])
        pygame.display.update()
        pygame.time.delay(1500)

        flag = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.button.click(x, y):
                        return

            self.screen.blit(self.background_map, [0, 0])
            self.screen.blit(self.title, [212, 90])
            self.button.put()

            if flag == 0:
                logo = pygame.transform.rotate(self.logo, 20)
                self.screen.blit(logo, [130, -55])
                flag = 1
            else:
                logo = pygame.transform.rotate(self.logo, 340)
                self.screen.blit(logo, [130, -55])
                flag = 0

            pygame.display.update()
            pygame.time.delay(1200)

    def main(self):
        self.music.play()
        self.display()
