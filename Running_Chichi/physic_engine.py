# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import random
import math


class motion:
    @staticmethod
    def linear_motion(v0, x0, y0, delta_t, mod, x_bound, y_bound):
        l = v0 * delta_t

        if mod == "vertical":
            y = y0 + l
            if (y > y_bound[0]) and (y < y_bound[1]):
                y0 = y
        if mod == "horizontal":
            x = x0 + l
            if (x > x_bound[0]) and (x < x_bound[1]):
                x0 = x

        return x0, y0

    @staticmethod
    def random(range_v, range_x, range_y, range_angle, split_time_range):
        v = random.uniform(range_v[0], range_v[1])
        x = random.randint(range_x[0], range_x[1])
        y = random.randint(range_y[0], range_y[1])
        angle_1 = random.randint(0, range_angle[0])  # 这里指与x轴的夹角, 单位为°
        angle_2 = random.randint(range_angle[1], 180)
        angle_3 = random.randint(range_angle[0], range_angle[1])
        angle = random.choice([angle_1, angle_2, angle_3])
        split_time = random.randint(split_time_range[0], split_time_range[1])

        return v, x, y, angle, split_time

    @staticmethod
    def throwing_motion(v0_x, v0_y, x0, y0, g, t):
        x = x0 + v0_x * t
        y = y0 + v0_y * t + 0.5 * g * t * t

        v_x = v0_x
        v_y = v0_y + g * t

        return x, y, v_x, v_y

    @staticmethod
    def collision(v0_x, v0_y, coefficient, mod):
        if mod == "vertical":
            v_x = 0 - (coefficient * v0_x)
            v_y = coefficient * v0_y
        if mod == "horizontal":
            v_x = coefficient * v0_x
            v_y = 0 - (coefficient * v0_y)

        return v_x, v_y

    @staticmethod
    def collision_dection(pos_1, l_1, h_1, pos_2, l_2, h_2, error_tolerance):
        situation1 = (pos_2[1] + h_2) > (pos_1[1] + error_tolerance[1])
        situation2 = pos_2[0] > (pos_1[0] + error_tolerance[0])
        situation3 = (pos_2[0] + l_2) < (pos_1[0] + l_1 - error_tolerance[0])
        if situation1 and situation2 and situation3:
            return True
        else:
            return False


class group_motion:
    def __init__(self, num):
        self.num = num
        self.particle_list = []
        self._init_group(self.num, self.particle_list)

    @staticmethod
    def _init_group(num, particle_list):
        for i in range(num):
            argv_dict = {'x': 0, 'y': 0, 'v_x': 0, 'v_y': 0,
                         'v0_x': 0, 'v0_y': 0, 'x0': 0, 'y0': 0,
                         'life': -1, 'start': -1, 'stop': (True, ""), "split_time": 0}
            particle_list.append(argv_dict)
            particle_list[i]['num'] = i

    def group_throwing_motion_init(self, range_v, range_x, range_y, range_angle, t_start, split_time_range):
        motion_func = motion()
        global split_range
        split_range = split_time_range

        for item in self.particle_list:
            [v0,
             item['x0'],
             item['y0'],
             angle0,
             split_time] = \
                motion_func.random(range_v, range_x, range_y, range_angle, split_time_range)

            angle_pi = angle0 * math.pi / 180
            v0_x = v0 * math.cos(angle_pi)
            v0_y = v0 * math.sin(angle_pi)

            item['v0_x'] = v0_x
            item['v0_y'] = v0_y
            item['life'] = 0
            item['start'] = t_start
            item['stop'] = (False, "")
            item['split_time'] = split_time

        return self.particle_list

    def group_throwing_motion(self, time_now, g, ground, ceil, wall):
        motion_func = motion

        for item in self.particle_list:
            if item['stop'][0] is not True:
                item['life'] = time_now - item['start']

                v0_x = item['v0_x']
                v0_y = item['v0_y']
                x0 = item['x0']
                y0 = item['y0']
                t = item['life']
                [x, y, v_x, v_y] = motion_func.throwing_motion(v0_x, v0_y, x0, y0, g, t)

                item['v_y'] = v_y
                item['v_x'] = v_x

                detect_horizontal = False
                detect_vertical = False

                if (y > ground) or (y < ceil):
                    detect_horizontal = True
                if (x > wall[1]) or (x < wall[0]):
                    detect_vertical = True

                if (not detect_horizontal) and (not detect_vertical):
                    item['stop'] = (False, "")
                    item['y'] = y
                    item['x'] = x
                else:
                    if detect_horizontal:
                        item['stop'] = (True, "horizontal")
                    elif detect_vertical:
                        item['stop'] = (True, "vertical")

        return self.particle_list

    def group_split(self):
        split_list = []
        for item in self.particle_list:
            if item['stop'][0] is True:
                item['split_time'] -= 1
                if item['split_time'] == 0:
                    split_time = random.randint(split_range[0], split_range[1])
                    self.num += 1
                    if item['stop'][1] == "horizontal":
                        item_bk = {'x': item['x'], 'y': item['y'], 'v_x': (0 - item['v_x']), 'v_y': item['v_y'],
                                   'v0_x': 0, 'v0_y': 0, 'x0': 0, 'y0': 0,
                                   'life': 0, 'start': item['start'] + item['life'],
                                   'stop': (True, "horizontal"), 'split_time': split_time}
                        split_list.append(item_bk)
                    elif item['stop'][1] == "vertical":
                        item_bk = {'x': item['x'], 'y': item['y'], 'v_x': item['v_x'], 'v_y': (0 - item['v_y']),
                                   'v0_x': 0, 'v0_y': 0, 'x0': 0, 'y0': 0,
                                   'life': 0, 'start': item['start'] + item['life'],
                                   'stop': (True, "vertical"), 'split_time': split_time}
                        split_list.append(item_bk)

        self.particle_list.extend(split_list)

        return self.particle_list

    def group_collision(self, coefficient):
        motion_func = motion()

        for item in self.particle_list:
            if item['stop'][0] is True:
                if (item['stop'][1] == "horizontal") or (item['stop'][1] == "vertical"):
                    v_x, v_y = motion_func.collision(item['v_x'],
                                                     item['v_y'],
                                                     coefficient,
                                                     item['stop'][1])

                    item['stop'] = (False, "")
                    item['x0'] = item['x']
                    item['y0'] = item['y']
                    item['v0_x'] = v_x
                    item['v0_y'] = v_y
                    item['start'] = item['start'] + item['life']
                    item['life'] = 0

        return self.particle_list
