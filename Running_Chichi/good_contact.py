# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import sys
import ConfigParser
import common
import physic_engine
import random
import logging
from good_contact_parameters import *


class good_contact:
    def __init__(self, screen, mod):
        logging.info("==========Good Contact MOD %s BEGIN===========" % mod)

        self.mod = mod

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

        self.main()

    def display(self):
        [x_1, y_1] = [125, 535]
        [x_2, y_2] = [800, 545]

        group_left = self._group_init(self.chichi_smile)
        group_right = self._group_init(self.chichi_hung)

        while True:
            t = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

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

            group_left.group_throwing_motion(t, G, GROUND, CEIL, (WALL_L, WALL_R))
            group_left.group_split(SPLIT_COEFFICIENT)
            group_left.group_collision(COLLISION_COEFFICIENT)

            group_right.group_throwing_motion(t, G, GROUND, CEIL, (WALL_L, WALL_R))
            group_right.group_split(SPLIT_COEFFICIENT)
            group_right.group_collision(COLLISION_COEFFICIENT)

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

            for item in group_left.particle_list:
                group_left.clear()
                if item.get_property('end') != -2:
                    pos = item.get_pos()
                    chichi_left = pygame.transform.rotate(item.particle_image, item.rotation)
                    self.screen.blit(chichi_left, [pos[0], pos[1]])

            for item in group_right.particle_list:
                group_right.clear()
                if item.get_property('end') != -2:
                    pos = item.get_pos()
                    chichi_right = pygame.transform.rotate(item.particle_image, item.rotation)
                    self.screen.blit(chichi_right, [pos[0], pos[1]])

            if self.mod['tips']:
                self.screen.blit(group_left.particle_image, [x_1 + 40, y_1 + 145])
                self.screen.blit(group_right.particle_image, [x_2 + 40, y_2 + 135])

            self.screen.blit(self.back_up, [0, 0])
            # ==================================
            # layout end
            # ==================================

            group_left.clear()
            group_right.clear()

            pygame.display.update()

            print "got_num: ", self.got_num
            print "left num: ", group_left.num
            print "right num: ", group_right.num
            print "left collision time: ", group_left.group_collision_time
            print "right collision time: ", group_right.group_collision_time
            print "剩余个数left: ", len(group_left.particle_list)
            print "剩余个数right: ", len(group_right.particle_list)

            # ==================================
            # mod select begin
            # ==================================
            # Mod Endless
            if self.mod['name'] == "endless":
                if len(group_left.particle_list) <= 0:
                    group_left = self._group_init(self.chichi_smile)
                if len(group_right.particle_list) <= 0:
                    group_right = self._group_init(self.chichi_hung)
            # ==================================
            # mod select end
            # ==================================

            if len(group_left.particle_list) + len(group_right.particle_list) >= 20:
                print "Oops! Too many Chichis!"
                sys.exit()

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

    @staticmethod
    def _group_init(particle_image):
        t = pygame.time.get_ticks()

        group_num = random.randint(NUM_RANGE[0], NUM_RANGE[1])
        group = physic_engine.group_motion(group_num, particle_image)
        group.group_motion_init(V0_RANGE, X0_RANGE, Y0_RANGE, ANGLE_RANGE, t, SPLIT_TIME)

        return group

    def main(self):
        self.music.play()
        self.display()
        logging.info("==========Good Contact MOD %s END===========" % self.mod)
