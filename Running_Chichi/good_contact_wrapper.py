#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2015/12/23'


import good_contact
import pygame
import common
import father
import sys


class good_contact_wrapper(father.module):
    def __init__(self, screen):
        super(good_contact_wrapper, self).__init__(screen)

    def _image_load(self):
        super(good_contact_wrapper, self)._image_load()
        self.background = pygame.image.load("%s%sgood_contact_back.png" % (self.current_dir, self.image_path)).convert()
        self.board = pygame.image.load("%s%sgood_contact_board.png"
                                       % (self.current_dir, self.image_path)).convert_alpha()

    def _tone_path_load(self):
        super(good_contact_wrapper, self)._tone_path_load()
        self.music_path = "%s%sgood contact opening.mp3" % (self.current_dir, self.tone_path)

    def _button_path_load(self):
        super(good_contact_wrapper, self)._button_path_load()

        self.mission_up = "%s%sbutton_mission_up.png" % (self.current_dir, self.button_path)
        self.mission_down = "%s%sbutton_mission_down.png" % (self.current_dir, self.button_path)
        self.play_up = "%s%sbutton_play_up.png" % (self.current_dir, self.button_path)
        self.play_down = "%s%sbutton_play_down.png" % (self.current_dir, self.button_path)
        self.record_up = "%s%sbutton_record_up.png" % (self.current_dir, self.button_path)
        self.record_down = "%s%sbutton_record_down.png" % (self.current_dir, self.button_path)

    def _module_init(self):
        super(good_contact_wrapper, self)._module_init()
        self.music = common.music(self.music_path)

        self.button_list = []
        button_play, button_mission, button_record = self._button_init()
        self.button_list.append(button_play)
        self.button_list.append(button_mission)
        self.button_list.append(button_record)

    def _button_init(self):
        screen = self.screen
        play = common.button(self.play_up, self.play_down, "play", 585, 500, 207, 80, screen)
        mission = common.button(self.mission_up, self.mission_down, "mission", 585, 570, 207, 80, screen)
        record = common.button(self.record_up, self.record_down, "record", 585, 640, 207, 80, screen)

        return play, mission, record

    def display(self):
        super(good_contact_wrapper, self).display()

        self.screen.blit(self.background, [0, 0])
        pygame.display.update()
        pygame.time.delay(1500)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # test
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print pygame.mouse.get_pos()
                for button in self.button_list:
                    button.mouse_detection(event)

            for button in self.button_list:
                if button.out:
                    return button.output

            # ==================================
            # layout begin
            # ==================================
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.board, [0, 0])
            for button in self.button_list:
                button.button_fresh()
                button.button_layout()
            # ==================================
            # layout end
            # ==================================

            pygame.display.update()

    def main(self):
        self.music.play()
        output = self.display()

        if output == "play":
            mod_selection = mod_set(self.screen)
            mod_select = mod_selection.main()
            mod = {'tips': True, 'name': mod_select}

            good = good_contact.good_contact(self.screen)
            good.set_mod(mod)
            good.main()
        else:
            print "Waiting..."

        self.music.stop()


class mod_set(father.module):
    def __init__(self, screen):
        super(mod_set, self).__init__(screen)

    def _image_load(self):
        super(mod_set, self)._image_load()

        self.background = pygame.image.load("%s%sgood_contact_back.png" % (self.current_dir, self.image_path)).convert()
        self.board = pygame.image.load("%s%sboard_mod.png" % (self.current_dir, self.image_path)).convert_alpha()

    def _button_path_load(self):
        super(mod_set, self)._button_path_load()

        self.endless_up = "%s%sbutton_endless_up.png" % (self.current_dir, self.button_path)
        self.endless_down = "%s%sbutton_endless_down.png" % (self.current_dir, self.button_path)
        self.timer_up = "%s%sbutton_timer_up.png" % (self.current_dir, self.button_path)
        self.timer_down = "%s%sbutton_timer_down.png" % (self.current_dir, self.button_path)
        self.single_up = "%s%sbutton_single_up.png" % (self.current_dir, self.button_path)
        self.single_down = "%s%sbutton_single_down.png" % (self.current_dir, self.button_path)

    def _module_init(self):
        super(mod_set, self)._module_init()

        self.button_list = []
        button_endless, button_timer, button_single = self._button_init()
        self.button_list.append(button_endless)
        self.button_list.append(button_timer)
        self.button_list.append(button_single)

    def _button_init(self):
        screen = self.screen
        endless = common.button(self.endless_up, self.endless_down, "endless", 240, 385, 207, 80, screen)
        timer = common.button(self.timer_up, self.timer_down, "timer", 240, 485, 207, 80, screen)
        single = common.button(self.single_up, self.single_down, "single", 240, 585, 207, 80, screen)

        return endless, timer, single

    def display(self):
        super(mod_set, self).display()

        self.screen.blit(self.background, [0, 0])
        pygame.display.update()
        # pygame.time.delay(1500)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # test
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print pygame.mouse.get_pos()
                for button in self.button_list:
                    button.mouse_detection(event)

            for button in self.button_list:
                if button.out:
                    return button.output

            # ==================================
            # layout begin
            # ==================================
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.board, [0, 0])
            for button in self.button_list:
                button.button_fresh()
                button.button_layout()
            # ==================================
            # layout end
            # ==================================

            pygame.display.update()

    def main(self):
        output = self.display()
        return output
