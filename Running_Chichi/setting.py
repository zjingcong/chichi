# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import wrapper
import pygame
import common
from good_contact_parameters import *
import sys


def setting(screen, back_music_obj, clock_now=0):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        setBoard = setting_board(screen, back_music_obj)
        set_out = setBoard.main()

        if set_out == 'back':
            t = pygame.time.get_ticks()
            return clock_now, t


class setting_board(wrapper.module):
    def __init__(self, screen, back_music_obj):
        self.x_start = 377
        self.x_end = 666
        self.back_music_obj = back_music_obj

        self._pre_init()
        super(setting_board, self).__init__(screen)

    def _pre_init(self):
        self.tips = setting_dic.get('tips')
        self.steamer_v = setting_dic.get('v')
        self.back_volume = setting_dic.get('back')
        self.sound_volume = setting_dic.get('sound')

        self.music_x = self._value_to_pos('back', self.back_volume, self.x_start, self.x_end)
        self.sound_x = self._value_to_pos('sound', self.sound_volume, self.x_start, self.x_end)
        self.v_x = self._value_to_pos('v', self.steamer_v, self.x_start, self.x_end)

    def _image_load(self):
        super(setting_board, self)._image_load()

        self.background = pygame.image.load("%s%sgood_contact_back.png" % (self.current_dir, self.image_path)).convert()
        self.board = pygame.image.load("%s%ssetting.png" % (self.current_dir, self.image_path)).convert_alpha()

    def _tone_path_load(self):
        super(setting_board, self)._tone_path_load()

        self.qiu_path = "%s%sqiu.wav" % (self.current_dir, self.tone_path)

    def _button_path_load(self):
        super(setting_board, self)._button_path_load()

        self.back_up = "%s%sbutton_back_up.png" % (self.current_dir, self.button_path)
        self.back_down = "%s%sbutton_back_down.png" % (self.current_dir, self.button_path)
        self.qube = "%s%shuakuai.png" % (self.current_dir, self.button_path)
        self.tips_off = "%s%sbutton_tips_off.png" % (self.current_dir, self.button_path)
        self.tips_on = "%s%sbutton_tips_on.png" % (self.current_dir, self.button_path)

    def _module_init(self):
        super(setting_board, self)._module_init()

        self.qiu = common.tone(self.qiu_path, 0)

        self.button_tips, self.button_back, self.button_music, self.button_sound, self.button_v = self._button_init()
        self.button_list = {}
        self.button_list['tips'] = self.button_tips
        self.button_list['back'] = self.button_back
        self.slip_button_list = {}
        self.slip_button_list['music'] = self.button_music
        self.slip_button_list['sound'] = self.button_sound
        self.slip_button_list['v'] = self.button_v

    def _button_init(self):
        tips = self._tips_button_fresh()
        back = common.button(self.back_up, self.back_down, "back", 462, 655, 116, 49, self.screen)

        back_music = common.slip_button(self.qube, "music", self.music_x, 455, 20, 25,
                                        self.x_start, self.x_end, self.screen)
        sound = common.slip_button(self.qube, "sound", self.sound_x, 527, 20, 25, self.x_start, self.x_end, self.screen)
        v = common.slip_button(self.qube, "v", self.v_x, 603, 20, 25, self.x_start, self.x_end, self.screen)

        return tips, back, back_music, sound, v

    def _tips_button_fresh(self):
        if self.tips:
            tips = common.button(self.tips_on, self.tips_off, "tips_change", 445, 375, 159, 25, self.screen)
        else:
            tips = common.button(self.tips_off, self.tips_on, "tips_change", 445, 375, 159, 25, self.screen)
        self.button_tips = tips

        return self.button_tips

    @staticmethod
    def _value_to_pos(name, value, x_start, x_end):
        width = x_end - x_start
        x = 0
        if name == 'back' or name == 'sound':
            x = value * width + x_start
        elif name == 'v':
            x = value * width / 10 + x_start

        return x

    @staticmethod
    def _pos_to_value(name, pos_x, x_start, x_end):
        width = x_end - x_start
        value = 0
        if name == 'back' or name == 'sound':
            value = float(pos_x - x_start) / width
        elif name == 'v':
            value = (float(pos_x - x_start) / width) * 10

        return value

    def fresh_argv(self):
        self.music_x = self.button_music.x
        self.sound_x = self.button_sound.x
        self.v_x = self.button_v.x

        self.back_volume = self._pos_to_value('back', self.music_x, self.x_start, self.x_end)
        self.sound_volume = self._pos_to_value('sound', self.sound_x, self.x_start, self.x_end)
        self.steamer_v = self._pos_to_value('v', self.v_x, self.x_start, self.x_end)

        if self.slip_button_list['music'].status == 1:
            self.back_music_obj.set_volume(self.back_volume)
        if self.slip_button_list['sound'].status == 1:
            self.qiu.set_volume(self.sound_volume)

    def display(self):
        super(setting_board, self).display()

        self.screen.blit(self.background, [0, 0])
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # test
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print pygame.mouse.get_pos()
                for name in self.button_list:
                    button = self.button_list[name]
                    button.mouse_detection(event)
                for name in self.slip_button_list:
                    slip_button = self.slip_button_list[name]
                    slip_button.mouse_detection(event)

            self.fresh_argv()

            for name in self.button_list:
                button = self.button_list[name]
                if button.out:
                    if button.output == 'tips_change':
                        setting_dic.set('tips', not self.tips)
                        self.button_tips.button_status_reset()
                    elif button.output == 'back':
                        setting_dic.set('back', self.back_volume)
                        setting_dic.set('sound', self.sound_volume)
                        setting_dic.set('v', self.steamer_v)

                        return 'back'

            # ==================================
            # layout begin
            # ==================================
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.board, [0, 0])
            self.button_list['tips'].button_fresh(0)
            self.button_list['back'].button_fresh()
            for name in self.button_list:
                self.button_list[name].button_layout()
            for name in self.slip_button_list:
                slip_button = self.slip_button_list[name]
                slip_button.button_fresh()
                slip_button.button_layout()
            # ==================================
            # layout end
            # ==================================

            pygame.display.update()

    def main(self):
        output = self.display()

        return output

# example for setting
import ConfigParser
import os


def example_main():
    pygame.init()
    current_dir = os.path.split(os.path.abspath(__file__))[0]

    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")
    tone_path = str(conf.get("path", "TONE_PATH"))

    screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
    screen_h = int(conf.get("variable", "SCREEN_HIGH"))
    screen = pygame.display.set_mode([screen_l, screen_h], 0, 32)
    pygame.display.set_caption("test: setting by zjingcong")

    music_path = "%s%sgood contact.mp3" % (current_dir, tone_path)
    back_music_obj = common.tone(music_path)
    back_music_obj.play()

    sb = setting_board(screen, back_music_obj)
    sb.main()

'''
if __name__ == '__main__':
    example_main()
'''
