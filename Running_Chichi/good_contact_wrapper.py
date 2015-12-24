#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2015/12/23'

"""
EXAMPLE:
import good_contact_wrapper as wp

good_contact = wp(screen)
result = good_contact.main()

# result = 0: back to menu
# result = 1: go to waiting page
"""


import good_contact
import pygame
import common
import wrapper
import sys
from scratch_card import scratch_card as card


class good_contact_wrapper(wrapper.module):
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
        self.music = common.tone(self.music_path)

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

    def _game(self, mod):
        good = good_contact.good_contact(self.screen)
        good.set_mod(mod)
        out, score = good.main()
        good.music.stop()
        if out == -1:
            sys.exit()

        score_out_obj = score_out(self.screen, out, score)
        score_output = score_out_obj.main()

        if score_output == "score":
            scratch_card = score_card(self.screen, score)
            card_out = scratch_card.main()
            score_out_obj.music.stop()
            if card_out == "menu":
                return 0
            if card_out == "again":
                self._game(mod)

    def main(self):
        self.music = common.tone(self.music_path)
        self.music.play()
        output = self.display()

        if output == "play":
            mod_selection = mod_set(self.screen)
            mod_select = mod_selection.main()
            mod = {'tips': True, 'name': mod_select}
            self.music.stop()
            result = self._game(mod)

        else:
            print "Waiting..."
            self.music.stop()
            result = 1

        # result 0: back to menu 1: go to waiting page
        return result


class mod_set(wrapper.module):
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


class score_out(wrapper.module):
    def __init__(self, screen, out, score):
        self.out = out
        self.score = score
        super(score_out, self).__init__(screen)

    # 0: win, 1: too many Chichis, 2: time out
    def init(self, out, score):
        self.out = out
        self.score = score

    def _image_load(self):
        super(score_out, self)._image_load()

        self.background = pygame.image.load("%s%sgood_contact_back.png" % (self.current_dir, self.image_path)).convert()
        self.bag = pygame.image.load("%s%slucky_bag.png" % (self.current_dir, self.image_path)).convert_alpha()

        self._text_image_load()

    def _text_image_load(self):
        if self.out == 0:
            self.text = pygame.image.load("%s%swin.png" % (self.current_dir, self.image_path)).convert_alpha()
        elif self.out == 1:
            self.text = pygame.image.load("%s%sgame_over.png" % (self.current_dir, self.image_path)).convert_alpha()
        elif self.out == 2:
            self.text = pygame.image.load("%s%stime_out.png" % (self.current_dir, self.image_path)).convert_alpha()

    def _tone_path_load(self):
        super(score_out, self)._tone_path_load()
        self.music_path = "%s%sout.mp3" % (self.current_dir, self.tone_path)

    def _button_path_load(self):
        super(score_out, self)._button_path_load()

        self.score_up = "%s%sbutton_score_up.png" % (self.current_dir, self.button_path)
        self.score_down = "%s%sbutton_score_down.png" % (self.current_dir, self.button_path)

    def _module_init(self):
        super(score_out, self)._module_init()
        self.music = common.tone(self.music_path)
        self.button = self._button_init()

    def _button_init(self):
        screen = self.screen
        score = common.button(self.score_up, self.score_down, "score", 435, 255, 172, 211, screen)

        return score

    def display(self):
        super(score_out, self).display()

        pygame.display.update()
        pygame.time.delay(1500)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # test
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print pygame.mouse.get_pos()
                self.button.mouse_detection(event)

            if self.button.out:
                return self.button.output

            # ==================================
            # layout begin
            # ==================================
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.bag, [0, 0])
            self.screen.blit(self.text, [0, 0])
            self.button.button_fresh(0)
            self.button.button_layout()
            # ==================================
            # layout end
            # ==================================

            pygame.display.update()

    def main(self):
        self.music.play()
        output = self.display()
        print output
        return output


class score_card(wrapper.module):
    def __init__(self, screen, score):
        self.score = score
        super(score_card, self).__init__(screen)

    def _image_load(self):
        super(score_card, self)._image_load()

        self.background = pygame.image.load("%s%sgood_contact_back.png" % (self.current_dir, self.image_path)).convert()
        self.scratch_card = pygame.image.load("%s%sscratch_card.png"
                                              % (self.current_dir, self.image_path)).convert_alpha()

    def _button_path_load(self):
        super(score_card, self)._button_path_load()

        self.again_up = "%s%sbutton_again_up.png" % (self.current_dir, self.button_path)
        self.again_down = "%s%sbutton_again_down.png" % (self.current_dir, self.button_path)
        self.menu_up = "%s%sbutton_menu_up.png" % (self.current_dir, self.button_path)
        self.menu_down = "%s%sbutton_menu_down.png" % (self.current_dir, self.button_path)

    def _font_path_load(self):
        super(score_card, self)._font_path_load()

        self.font_total = '%s%sBROADW_0.TTF' % (self.current_dir, self.font_path)

    def _module_init(self):
        super(score_card, self)._module_init()

        self.button_list = []
        button_again, button_menu = self._button_init()
        self.button_list.append(button_again)
        self.button_list.append(button_menu)

        self.scratch = card(15, 300, 200, (370, 417), [128, 128, 128], 6, self.screen)

        self._text_score()

    def _text(self, message, font_type, color, num):
        font = pygame.font.Font(font_type, num)
        text_content = message
        score_text = font.render(text_content, False, color)
        textRect = score_text.get_rect()
        textRect.centerx = 520

        return score_text, textRect

    def _text_score(self):
        self.score_total_text, self.total_textRect = self._text("TOTAL: %d" % self.score['total'],
                                                                self.font_total, [97, 57, 33], 35)
        self.total_textRect.centery = 445

        self.score_extra_text, self.extra_textRect = self._text("EXTRA: %d" % self.score['extra'],
                                                                self.font_total, [97, 57, 33], 30)
        height_extra = self.extra_textRect[3]
        self.extra_textRect.centery = self.total_textRect.centery + height_extra

        self.score_left_text, self.left_textRect = self._text("LEFT: %d * 10" % self.score['left'],
                                                              self.font_total, [97, 57, 33], 30)
        height_left = self.left_textRect[3]
        self.left_textRect.centery = self.extra_textRect.centery + height_left

        self.score_right_text, self.right_textRect = self._text("RIGHT: %d * 10" % self.score['right'],
                                                                self.font_total, [97, 57, 33], 30)
        height_right = self.right_textRect[3]
        self.right_textRect.centery = self.left_textRect.centery + height_right

        self.score_time_text, self.time_textRect = self._text("TIME: %d s" % (self.score['time'] / 1000),
                                                              self.font_total, [97, 57, 33], 30)
        height_time = self.time_textRect[3]
        self.time_textRect.centery = self.right_textRect.centery + height_time

    def _button_init(self):
        screen = self.screen
        again = common.button(self.again_up, self.again_down, "again", 260, 630, 161, 93, screen)
        menu = common.button(self.menu_up, self.menu_down, "menu", 600, 630, 191, 95, screen)

        return again, menu

    def display(self):
        super(score_card, self).display()

        self.screen.blit(self.background, [0, 0])
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # test
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print pygame.mouse.get_pos()
                for button in self.button_list:
                    button.mouse_detection(event)
                self.scratch.fresh_status(event)

            for button in self.button_list:
                if button.out:
                    return button.output

            # ==================================
            # layout begin
            # ==================================
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(self.scratch_card, [0, 0])

            self.screen.blit(self.score_total_text, self.total_textRect)
            self.screen.blit(self.score_extra_text, self.extra_textRect)
            self.screen.blit(self.score_left_text, self.left_textRect)
            self.screen.blit(self.score_right_text, self.right_textRect)
            self.screen.blit(self.score_time_text, self.time_textRect)

            self.scratch.display()
            for button in self.button_list:
                button.button_fresh(0)
                button.button_layout()
            # ==================================
            # layout end
            # ==================================

            pygame.display.update()

    def main(self):
        output = self.display()

        return output
