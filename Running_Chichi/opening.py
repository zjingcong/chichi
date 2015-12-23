# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import common
import sys
import father


class opening(father.module):
    def __init__(self, screen):
        super(opening, self).__init__(screen)

    def _image_load(self):
        super(opening, self)._image_load()
        self.background = pygame.image.load("%s%sfood_map.jpg" % (self.current_dir, self.image_path)).convert()
        self.title = pygame.image.load("%s%stitle.png" % (self.current_dir, self.image_path)).convert_alpha()
        self.logo = pygame.image.load("%s%slogo.png" % (self.current_dir, self.image_path)).convert_alpha()

    def _tone_path_load(self):
        super(opening, self)._tone_path_load()
        self.music_path = "%s%sopening.mp3" % (self.current_dir, self.tone_path)

    def _button_path_load(self):
        super(opening, self)._button_path_load()
        self.button_up = "%s%splaying_up.png" % (self.current_dir, self.button_path)
        self.button_down = "%s%splaying_down.png" % (self.current_dir, self.button_path)

    def _module_init(self):
        super(opening, self)._module_init()
        self.music = common.music(self.music_path)
        self.logo_anim = self._logo_anim_init()
        self.button = self._button_init()

    def _logo_anim_init(self):
        screen = self.screen
        logo = self.logo
        frame_1 = pygame.transform.rotate(logo, 20)
        frame_2 = pygame.transform.rotate(logo, -20)
        frame_iamge_list = [{'image': frame_1, 'pos': (130, -55)}, {'image': frame_2, 'pos': (130, -55)}]

        anim = common.animation(frame_iamge_list, 140, 'endless', screen)

        return anim

    def _button_init(self):
        button_up = self.button_up
        button_down = self.button_down
        screen = self.screen
        button = common.button(button_up, button_down, "enter game", 370, 590, 300, 100, screen)

        return button

    def display(self):
        super(opening, self).display()

        self.screen.blit(self.background, [0, 0])
        pygame.display.update()
        pygame.time.delay(1500)

        while True:
            for event in pygame.event.get():
                # print event.type
                if event.type == pygame.QUIT:
                    sys.exit()
                self.button.mouse_detection(event)

            if self.button.out:
                return self.button.output

            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.title, [212, 90])
            self.button.button_fresh(0)
            self.button.button_layout()

            self.logo_anim.display()

            pygame.display.update()

    def main(self):
        self.music.play()
        output = self.display()
        self.music.stop()
        return output
