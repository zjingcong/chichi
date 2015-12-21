# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import pygame
import sys
import ConfigParser
import common
import physic_engine
import random

V = 10
A = 0
G = 0.0005
GROUND = 600
CEIL = 60
WALL_L = 0
WALL_R = 965
COLLISION_COEFFICIENT = 0.99
V0_RANGE = (0.1, 0.5)
X0_RANGE = (450, 550)
Y0_RANGE = (150, 150)
ANGLE_RANGE = (30, 150)
ERROR_T = (0, 30)
SPLIT_TIME = (3, 5)
NUM_RANGE = (10, 20)

zhenglong_pic = (118, 118)
chichi_small_pic = (59, 47)


class good_contact:
    def __init__(self, screen):
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
        self.background = pygame.image.load("%s%sgood_contact_back.png" % (current_dir, image_path)).convert()
        self.zhenglong_1 = pygame.image.load("%s%szhenglong_small.png" % (current_dir, image_path)).convert_alpha()
        self.zhenglong_2 = pygame.image.load("%s%szhenglong_small.png" % (current_dir, image_path)).convert_alpha()
        self.chichi_small = pygame.image.load("%s%schichi_smile_small.png" % (current_dir, image_path)).convert_alpha()

        self.music = common.music(self.music_path)

        self.score = {'left': 0, 'right': 0}

        self.main()

    def display(self):
        [x_1, y_1] = [125, 535]
        [x_2, y_2] = [800, 545]

        group_num = random.randint(NUM_RANGE[0], NUM_RANGE[1])

        t = pygame.time.get_ticks()
        group = physic_engine.group_motion(group_num)
        group.group_motion_init(V0_RANGE, X0_RANGE, Y0_RANGE, ANGLE_RANGE, t, SPLIT_TIME)

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

            self.screen.blit(self.background, [0, 0])

            self.screen.blit(self.zhenglong_1, [x_1, y_1])
            self.screen.blit(self.zhenglong_2, [x_2, y_2])

            group.group_throwing_motion(t, G, GROUND, CEIL, (WALL_L, WALL_R))
            group.group_split()
            group.group_collision(COLLISION_COEFFICIENT)

            print group.num

            chichi_list = group.particle_list

            if self._collision(chichi_list, [x_1, y_1]):
                self.score['left'] += 1
            if self._collision(chichi_list, [x_2, y_2]):
                self.score['right'] += 1

            for item in chichi_list:
                if item.get_property('life') != -2:
                    pos = item.get_pos()
                    self.screen.blit(self.chichi_small, [pos[0], pos[1]])

            pygame.display.update()

            if len(chichi_list) <= 0:
                print "Win!"
                print self.score
                sys.exit()
            pygame.time.delay(5)

    @staticmethod
    def _key_move(v, x, y, key):
        x_bound = [0, screen_l - zhenglong_pic[0]]
        y_bound = [0, screen_h]
        if pygame.key.get_pressed()[key] != 0:
            x, y = motion.linear_motion(v, x, y, 1, "horizontal", x_bound, y_bound)

        return x, y

    @staticmethod
    def _collision(chichi_list, pos_zhenglong):
        for item in chichi_list:
            pos_chichi = item.get_pos()
            if motion.collision_dection(pos_zhenglong, zhenglong_pic[0], zhenglong_pic[1],
                                        pos_chichi, chichi_small_pic[0], chichi_small_pic[1],
                                        ERROR_T):
                item.set_property('life', -2)
                chichi_list.remove(item)

                return True

        return False

    def main(self):
        self.music.play()
        self.display()
