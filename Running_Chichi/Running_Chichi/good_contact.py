# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import ConfigParser
import common
import physic_engine
import random
import logging
from good_contact_parameters import *


class good_contact:
    def __init__(self, screen):
        logging.info("==========Good Contact BEGIN===========")

        self.mod = {}

        global screen_l, screen_h

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        image_path = str(conf.get("path", "IMAGE_PATH"))
        tone_path = str(conf.get("path", "TONE_PATH"))
        screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
        screen_h = int(conf.get("variable", "SCREEN_HIGH"))
        current_dir = common.CURRENT_DIR

        self.screen = screen
        self.music_path = "%s%sgood contact.mp3" % (current_dir, tone_path)

        self.back_up = pygame.image.load("%s%sgood_contact_back_up.png" % (current_dir, image_path)).convert_alpha()
        self.back_down = pygame.image.load("%s%sgood_contact_back_down.png" % (current_dir, image_path)).convert_alpha()
        self.zhenglong_1 = pygame.image.load("%s%szhenglong_small.png" % (current_dir, image_path)).convert_alpha()
        self.zhenglong_2 = pygame.image.load("%s%szhenglong_small.png" % (current_dir, image_path)).convert_alpha()
        self.chichi_smile = pygame.image.load("%s%schichi_smile_small.png" % (current_dir, image_path)).convert_alpha()
        self.chichi_hung = pygame.image.load("%s%schichi_hungry_small.png" % (current_dir, image_path)).convert_alpha()

        self.music = common.music(self.music_path)

        self.got_num = {'left': 0, 'right': 0}

    def set_mod(self, mod):
        self.mod = mod
        logging.info("select MOD as %s" % mod)

        return mod

    def display(self):
        t_start = pygame.time.get_ticks()

        [x_1, y_1] = [125, 530]
        [x_2, y_2] = [800, 540]

        group_left = self._group_init(self.chichi_smile)
        group_right = self._group_init(self.chichi_hung)

        group_left_list = []
        group_right_list = []
        group_left_list.append(group_left)
        group_right_list.append(group_right)

        while True:
            t = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                # test
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print pygame.mouse.get_pos()

            global motion
            motion = physic_engine.motion()
            # key: a
            x_1, y_1 = self._key_move(-V, x_1, y_1, 97)
            # key: s
            x_1, y_1 = self._key_move(V, x_1, y_1, 115)
            # key: k
            x_2, y_2 = self._key_move(-V, x_2, y_2, 107)
            # key: l
            x_2, y_2 = self._key_move(V, x_2, y_2, 108)

            coefficient = COLLISION_COEFFICIENT

            for group_left in group_left_list:
                group_left.group_throwing_motion(t, G, GROUND, CEIL, (WALL_L, WALL_R))
                group_left.group_split(SPLIT_COEFFICIENT)
                group_left.group_collision(coefficient)

            for group_right in group_right_list:
                group_right.group_throwing_motion(t, G, GROUND, CEIL, (WALL_L, WALL_R))
                group_right.group_split(SPLIT_COEFFICIENT)
                group_right.group_collision(coefficient)

            # ==================================
            # collision detection begin
            # ==================================
            if self._collision(group_left, [x_1, y_1]):
                self.got_num['left'] += 1
            if self._collision(group_right, [x_2, y_2]):
                self.got_num['right'] += 1
            # ==================================
            # collision detection end
            # ==================================

            # ==================================
            # layout begin
            # ==================================
            self.screen.blit(self.back_down, [0, 0])
            self.screen.blit(self.zhenglong_1, [x_1, y_1])
            self.screen.blit(self.zhenglong_2, [x_2, y_2])

            for group_left in group_left_list:
                for item in group_left.particle_list:
                    group_left.clear()
                    if item.get_property('end') != -2:
                        pos = item.get_pos()
                        chichi_left = pygame.transform.rotate(item.particle_image, item.rotation)
                        self.screen.blit(chichi_left, [pos[0], pos[1]])

            for group_right in group_right_list:
                for item in group_right.particle_list:
                    group_right.clear()
                    if item.get_property('end') != -2:
                        pos = item.get_pos()
                        chichi_right = pygame.transform.rotate(item.particle_image, item.rotation)
                        self.screen.blit(chichi_right, [pos[0], pos[1]])

            if self.mod['tips']:
                self.screen.blit(group_left.particle_image, [x_1 + 40, y_1 + 150])
                self.screen.blit(group_right.particle_image, [x_2 + 40, y_2 + 140])

            self.screen.blit(self.back_up, [0, 0])
            # ==================================
            # layout end
            # ==================================

            num_active_left, num_block_left, num_active_right, num_block_right = 0, 0, 0, 0

            for group_left in group_left_list:
                group_left.clear()
                active_left, block_left = self._cal_num(group_left)
                num_active_left += active_left
                num_block_left += block_left
            for group_right in group_right_list:
                group_right.clear()
                active_right, block_right = self._cal_num(group_right)
                num_active_right += active_right
                num_block_right += block_right

            pygame.display.update()

            # ==================================
            # mod select begin
            # ==================================
            # Mod Endless
            if self.mod['name'] == "endless":
                if num_active_left <= 0:
                    group_left = self._group_init(self.chichi_smile)
                    group_left_list.append(group_left)
                if num_active_right <= 0:
                    group_right = self._group_init(self.chichi_hung)
                    group_right_list.append(group_right)

                # score for endless mod
                score = 10 * (self.got_num['left'] + self.got_num['right'])

            if (num_active_left + num_active_right >= 50) or (num_block_left + num_block_right >= 70):
                print "Oops! Too many Chichis!"
                print "SCORE: ", score
                return

            # Mod Timer
            if self.mod['name'] == "timer":
                if num_active_left <= 0:
                    group_left = self._group_init(self.chichi_smile)
                    group_left_list.append(group_left)
                if num_active_right <= 0:
                    group_right = self._group_init(self.chichi_hung)
                    group_right_list.append(group_right)

                t_end = pygame.time.get_ticks()

                if t_end - t_start >= 30000:
                    score = 10 * (self.got_num['left'] + self.got_num['right'])
                    print "Oops! Time out!"
                    print "SCORE: ", score
                    return

            # Mod Single
            if self.mod['name'] == "single":
                t_end = pygame.time.get_ticks()
                score = 1000 / (t_end - t_start) + 10 * (self.got_num['left'] + self.got_num['right'])
                if (num_active_left + num_active_right >= 50) or (num_block_left + num_block_right >= 70):
                    print "Oops! Too many Chichis!"
                    print "SCORE: ", score
                    return
                if num_active_left + num_active_right == 0:
                    if num_block_left + num_block_right == 0:
                        print "PERFECT!"
                        print num_block_right, num_block_left
                        score_extra = 100
                    elif self.got_num['left'] + self.got_num['right'] > 0:
                        print "Good!"
                        score_extra = 0
                    else:
                        print "Oops! Got nothing!"
                        score_extra = -100
                    print "SCORE: ", score + score_extra
                    return
            # ==================================
            # mod select end
            # ==================================

    @staticmethod
    def _key_move(v, x, y, key):
        x_bound = [0, screen_l - zhenglong_pic[0]]
        y_bound = [0, screen_h]
        if pygame.key.get_pressed()[key] != 0:
            x, y = motion.linear_motion(v, x, y, 1, "horizontal", x_bound, y_bound)

        return x, y

    @staticmethod
    def _collision(group, pos_zhenglong):
        for item in group.particle_list:
            pos_chichi = item.get_pos()
            if motion.collision_dection(pos_zhenglong, zhenglong_pic[0], zhenglong_pic[1],
                                        pos_chichi, chichi_small_pic[0], chichi_small_pic[1],
                                        ERROR_T):
                item.set_property('end', -2)
                group.clear_particle(item)

                return True

        return False

    def _group_init(self, particle_image):
        t = pygame.time.get_ticks()

        if self.mod['name'] == "timer" or self.mod['name'] == "endless":
            group_num = random.randint(NUM_RANGE[0], NUM_RANGE[1])
            group = physic_engine.group_motion(group_num, particle_image)
            group.group_motion_init(V0_RANGE, X0_RANGE, Y0_RANGE, ANGLE_RANGE, t, SPLIT_TIME)

        if self.mod['name'] == "single":
            group_num = random.randint(NUM_RANGE_LARGE[0], NUM_RANGE_LARGE[1])
            group = physic_engine.group_motion(group_num, particle_image)
            group.group_motion_init(V0_RANGE, X0_RANGE, Y0_RANGE, ANGLE_RANGE, t, SPLIT_TIME)

        return group

    @staticmethod
    def _cal_num(group):
        num_active = 0
        num_block = 0
        for item in group.particle_list:
            if (item.get_property('end') != -3) and (item.get_property('end') != -2):
                num_active += 1
            elif item.get_property('end') == -3:
                num_block += 1

        return num_active, num_block

    def main(self):
        self.music.play()
        self.display()
        logging.info("==========Good Contact END===========")
