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
from pygame.locals import *
import wrapper
import sys
import setting


class good_contact(wrapper.module):
    def __init__(self, screen):
        logging.info("==========Good Contact BEGIN===========")

        self.mod = {}
        self.v_steamer = setting_dic.get('v')

        global screen_l, screen_h
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        screen_l = int(conf.get("variable", "SCREEN_LENGTH"))
        screen_h = int(conf.get("variable", "SCREEN_HIGH"))

        self.got_num = {'left': 0, 'right': 0}
        self.score_total = 0
        self.score_extra = 0
        self.score_time = 0  # single mod > 0
        self.score = {'total': 0, 'extra': 0, 'left': 0, 'right': 0, 'time': 0}
        self.out = -1   # 0: win, 1: too many Chichis, 2: time out, -1: interruption
        self.tips_off_time = 0

        super(good_contact, self).__init__(screen)

    def _image_load(self):
        super(good_contact, self)._image_load()

        current_dir = self.current_dir
        image_path = self.image_path

        self.back_up = pygame.image.load("%s%sgood_contact_back_up.png" % (current_dir, image_path)).convert_alpha()
        self.back_down = pygame.image.load("%s%sgood_contact_back_down.png" % (current_dir, image_path)).convert_alpha()
        self.zhenglong_1 = pygame.image.load("%s%szhenglong_small.png" % (current_dir, image_path)).convert_alpha()
        self.zhenglong_2 = pygame.image.load("%s%szhenglong_small.png" % (current_dir, image_path)).convert_alpha()
        self.chichi_smile = pygame.image.load("%s%schichi_smile_small.png" % (current_dir, image_path)).convert_alpha()
        self.chichi_hung = pygame.image.load("%s%schichi_hungry_small.png" % (current_dir, image_path)).convert_alpha()

    def _tone_path_load(self):
        super(good_contact, self)._tone_path_load()

        current_dir = self.current_dir
        tone_path = self.tone_path

        self.music_path = "%s%sgood contact.mp3" % (current_dir, tone_path)
        self.qiu_path = "%s%sqiu.wav" % (current_dir, tone_path)

    def _module_init(self):
        super(good_contact, self)._module_init()

        self.music = common.tone(self.music_path)
        self.qiu = common.tone(self.qiu_path, 0)

    def set_mod(self, mod):
        self.mod = mod
        logging.info("select MOD as %s" % mod)

        return mod

    def display(self):
        super(good_contact, self).display()

        clock_start = 0
        t = pygame.time.get_ticks()
        clock_now = clock_start

        [x_1, y_1] = [125, 530]
        [x_2, y_2] = [800, 540]

        group_left = self._group_init(self.chichi_smile, clock_start)
        group_right = self._group_init(self.chichi_hung, clock_start)

        group_left_list = []
        group_right_list = []
        group_left_list.append(group_left)
        group_right_list.append(group_right)

        while True:
            t, clock_now = self._clock_fresh(t, clock_now)
            if setting_dic.get('tips') is not True:
                self.tips_off_time += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    print event.key
                    if event.key == pygame.K_SPACE:
                        clock_now, t = self._pause(clock_now)
                    if event.key == pygame.K_w:
                        clock_now, t = setting.setting(self.screen, self.music, clock_now)

            global motion
            motion = physic_engine.motion()
            self.v_steamer = setting_dic.get('v')
            # key: a
            x_1, y_1 = self._key_move(-self.v_steamer, x_1, y_1, pygame.K_a)
            # key: s
            x_1, y_1 = self._key_move(self.v_steamer, x_1, y_1, pygame.K_s)
            # key: k
            x_2, y_2 = self._key_move(-self.v_steamer, x_2, y_2, pygame.K_k)
            # key: l
            x_2, y_2 = self._key_move(self.v_steamer, x_2, y_2, pygame.K_l)

            coefficient = COLLISION_COEFFICIENT

            for group_left in group_left_list:
                group_left.group_throwing_motion(clock_now, G, GROUND, CEIL, (WALL_L, WALL_R))
                group_left.group_split(SPLIT_COEFFICIENT)
                group_left.group_collision(coefficient)

            for group_right in group_right_list:
                group_right.group_throwing_motion(clock_now, G, GROUND, CEIL, (WALL_L, WALL_R))
                group_right.group_split(SPLIT_COEFFICIENT)
                group_right.group_collision(coefficient)

            # ==================================
            # collision detection begin
            # ==================================
            if self._collision(group_left, [x_1, y_1]):
                self.qiu.play(ch_mod=2, pos_x=x_1, width_x=screen_l, volume=setting_dic.get('sound'))
                self.got_num['left'] += 1
            if self._collision(group_right, [x_2, y_2]):
                self.qiu.play(ch_mod=2, pos_x=x_2, width_x=screen_l, volume=setting_dic.get('sound'))
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

            # --------------TIPS----------------
            if setting_dic.get('tips'):
                self.screen.blit(group_left.particle_image, [x_1 + 40, y_1 + 150])
                self.screen.blit(group_right.particle_image, [x_2 + 40, y_2 + 140])
            # --------------TIPS----------------

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
            # out: 0: win, 1: too many Chichis, 2: time out
            # Mod Endless
            if self.mod['name'] == "endless":
                # new group
                t, clock_now = self._clock_fresh(t, clock_now)
                self._new_group(num_active_left, num_active_right, group_left_list, group_right_list, clock_now)

            if (num_active_left + num_active_right >= DEAD_ACTIVE) or (num_block_left + num_block_right >= DEAD_BLOCK):
                clock_end = pygame.time.get_ticks()
                self.score_time = clock_end - clock_start
                self.score_total = int(self.score_time / 10000)
                self.out = 1
                self._score_wrapper(self.score_time)

                return self.out, self.score

            # Mod Timer
            if self.mod['name'] == "timer":
                # new group
                t, clock_now = self._clock_fresh(t, clock_now)
                self._new_group(num_active_left, num_active_right, group_left_list, group_right_list, clock_now)

                t, clock_now = self._clock_fresh(t, clock_now)
                if clock_now - clock_start >= 30000:       # 30s
                    self.out = 2
                    self._score_wrapper(30000)

                    return self.out, self.score

            # Mod Single
            if self.mod['name'] == "single":
                t, clock_now = self._clock_fresh(t, clock_now)
                self.score_time = clock_now - clock_start
                self.score_total = 1000000 / self.score_time

                if (num_active_left + num_active_right >= DEAD_ACTIVE + 5) \
                        or (num_block_left + num_block_right >= DEAD_BLOCK):
                    self.out = 1
                    self._score_wrapper(self.score_time)

                    return self.out, self.score

                if num_active_left + num_active_right == 0:
                    self.out = 0
                    if num_block_left + num_block_right == 0:
                        self.score_extra = 100
                    elif self.got_num['left'] + self.got_num['right'] > 0:
                        self.score_extra = 0
                    else:
                        self.score_extra = -100

                    self._score_wrapper(self.score_time)
                    return self.out, self.score
            # ==================================
            # mod select end
            # ==================================

    @staticmethod
    def _clock_fresh(t, clock_now):
        t_now = pygame.time.get_ticks()
        clock_now = t_now - t + clock_now
        t = t_now

        return t, clock_now

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

    def _group_init(self, particle_image, t, v0_range=V0_RANGE, split_time=SPLIT_TIME, num_range=NUM_RANGE):
        if self.mod['name'] == "timer" or self.mod['name'] == "endless":
            group_num = random.randint(num_range[0], num_range[1])
            group = physic_engine.group_motion(group_num, particle_image)
            group.group_motion_init(v0_range, X0_RANGE, Y0_RANGE, ANGLE_RANGE, t, split_time)

        if self.mod['name'] == "single":
            group_num = random.randint(NUM_RANGE_LARGE[0], NUM_RANGE_LARGE[1])
            group = physic_engine.group_motion(group_num, particle_image)
            group.group_motion_init(v0_range, X0_RANGE, Y0_RANGE, ANGLE_RANGE, t, split_time)

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

    def _score_wrapper(self, time_total):
        self.score_extra += float(self.tips_off_time) * 500 / time_total

        self.score['total'] = self.score_total + self.score_extra + 10 * (self.got_num['left'] + self.got_num['right'])
        self.score['extra'] = self.score_extra
        self.score['left'] = self.got_num['left']
        self.score['right'] = self.got_num['right']
        self.score['time'] = self.score_time

        return self.score

    def _new_group(self, num_active_left, num_active_right, group_left_list, group_right_list, t):
        l_left = len(group_left_list)
        l_right = len(group_right_list)

        # 速度逐渐加快（每轮+0.1）
        v0_range_left = (V0_RANGE[0] + (float(l_left) / 10 * 0.1), V0_RANGE[1] + (float(l_left) / 10 * 0.1))
        v0_range_right = (V0_RANGE[0] + (float(l_right) / 10 * 0.1), V0_RANGE[1] + (float(l_right) / 10 * 0.1))

        # 分裂需要撞击的次数逐渐减少直到为1
        split_time_left = (SPLIT_TIME[0] - int(float(l_left) / 10 * 0.5),
                           SPLIT_TIME[1] - int(float(l_left) / 10 * 0.5))
        split_time_right = (SPLIT_TIME[0] - int(float(l_right) / 10 * 0.5),
                            SPLIT_TIME[1] - int(float(l_right) / 10 * 0.5))
        if split_time_right[0] <= 0:
            split_time_right = 1
        if split_time_right[1] <= 0:
            split_time_right = 1
        if split_time_left[0] <= 0:
            split_time_left = 1
        if split_time_left[1] <= 0:
            split_time_left = 1

        # 数量逐渐增多（每20轮+1）
        num_left = (int(NUM_RANGE[0] + int(float(l_left) / 10 * 0.8)),
                    int(NUM_RANGE[1] + int(float(l_left) / 10 * 0.8)))
        num_right = (int(NUM_RANGE[0] + int(float(l_right) / 10 * 0.8)),
                     int(NUM_RANGE[1] + int(float(l_right) / 10 * 0.8)))

        # t = pygame.time.get_ticks()
        if num_active_left <= 0:
            group_left = self._group_init(self.chichi_smile, t, v0_range=v0_range_left,
                                          split_time=split_time_left, num_range=num_left)
            group_left_list.append(group_left)
        if num_active_right <= 0:
            group_right = self._group_init(self.chichi_hung, t, v0_range=v0_range_right,
                                           split_time=split_time_right, num_range=num_right)
            group_right_list.append(group_right)

    @staticmethod
    def _pause(clock_now):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        t = pygame.time.get_ticks()
                        return clock_now, t

    def main(self):
        self.music.play()
        self.display()

        logging.info("==========Good Contact END===========")

        return self.out, self.score
