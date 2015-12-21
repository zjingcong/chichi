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
        v_x = v0_x
        v_y = v0_y

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
    class particle:
        def __init__(self):
            self.argv_dict = {'x': 0, 'y': 0, 'v_x': 0, 'v_y': 0,
                              'v0_x': 0, 'v0_y': 0, 'x0': 0, 'y0': 0,
                              'life': -1, 'start': -1, 'stop': (True, ""), "split_time": 0}
            self.pos = self.get_pos()

        def get_property(self, name):
            if name in self.argv_dict:
                return self.argv_dict[name]
            else:
                print "ERROR: No Attribution."

        def set_property(self, name, value):
            if name in self.argv_dict:
                self.argv_dict[name] = value
            else:
                print "ERROR: No Attribution."

        def fresh_properties(self, argv_dict_new):
            self.argv_dict = argv_dict_new

            return self.argv_dict

        def set_split_time(self, split_time_range):
            split_time = random.randint(split_time_range[0], split_time_range[1])
            self.set_property('split_time', split_time)

            return split_time

        def get_pos(self):
            x = self.get_property('x')
            y = self.get_property('y')
            self.pos = (x, y)

            return self.pos

    def __init__(self, num):
        self.num = num
        self.particle_list = []
        self._init_group(self.num, self.particle_list)
        self.motion_func = motion()

    def _init_group(self, num, particle_list):
        for i in range(num):
            p = self.particle()
            particle_list.append(p)

    def group_motion_init(self, range_v, range_x, range_y, range_angle, t_start, split_time_range):
        global split_range
        split_range = split_time_range

        for item in self.particle_list:
            [v0, x0, y0, angle0, split_time] = self.motion_func.random(range_v, range_x, range_y,
                                                                       range_angle, split_time_range)

            item.set_property('x0', x0)
            item.set_property('y0', y0)

            angle_pi = angle0 * math.pi / 180
            v0_x = v0 * math.cos(angle_pi)
            v0_y = v0 * math.sin(angle_pi)

            item.set_property('v0_x', v0_x)
            item.set_property('v0_y', v0_y)
            item.set_property('life', 0)
            item.set_property('start', t_start)
            item.set_property('stop', (False, ""))
            item.set_property('split_time', split_time)

        return self.particle_list

    def group_throwing_motion(self, time_now, g, ground, ceil, wall):
        for item in self.particle_list:
            if item.get_property('stop')[0] is not True:
                item.set_property('life', (time_now - item.get_property('start')))

                v0_x = item.get_property('v0_x')
                v0_y = item.get_property('v0_y')
                x0 = item.get_property('x0')
                y0 = item.get_property('y0')
                t = item.get_property('life')

                [x, y, v_x, v_y] = self.motion_func.throwing_motion(v0_x, v0_y, x0, y0, g, t)

                item.set_property('v_x', v_x)
                item.set_property('v_y', v_y)

                detect_horizontal = False
                detect_vertical = False

                if (y > ground) or (y < ceil):
                    detect_horizontal = True
                if (x > wall[1]) or (x < wall[0]):
                    detect_vertical = True

                if (not detect_horizontal) and (not detect_vertical):
                    item.set_property('stop', (False, ""))
                    item.set_property('y', y)
                    item.set_property('x', x)
                else:
                    if detect_horizontal:
                        item.set_property('stop', (True, "horizontal"))
                    elif detect_vertical:
                        item.set_property('stop', (True, "vertical"))

        return self.particle_list

    def group_split(self):
        split_list = []
        for item in self.particle_list:
            if item.get_property('stop')[0] is True:
                item.set_property('split_time', item.get_property('split_time') - 1)
                if item.get_property('split_time') == 0:
                    self.num += 1

                    if item.get_property('stop')[1] == "horizontal":
                        split_item = self.particle()

                        split_item.set_property('x', item.get_property('x'))
                        split_item.set_property('y', item.get_property('y'))
                        split_item.set_property('v_x', 0 - item.get_property('v_x'))
                        split_item.set_property('v_y', item.get_property('v_y'))
                        split_item.set_property('life', 0)
                        split_item.set_property('start', item.get_property('start') + item.get_property('life'))
                        split_item.set_property('stop', (True, "horizontal"))
                        split_item.set_split_time(split_range)

                        split_list.append(split_item)

                    elif item.get_property('stop')[1] == "vertical":
                        split_item = self.particle()

                        split_item.set_property('x', item.get_property('x'))
                        split_item.set_property('y', item.get_property('y'))
                        split_item.set_property('v_x', item.get_property('v_x'))
                        split_item.set_property('v_y', 0 - item.get_property('v_y'))
                        split_item.set_property('life', 0)
                        split_item.set_property('start', item.get_property('start') + item.get_property('life'))
                        split_item.set_property('stop', (True, "vertical"))
                        split_item.set_split_time(split_range)

                        split_list.append(split_item)

        self.particle_list.extend(split_list)

        return self.particle_list

    def group_collision(self, coefficient):
        motion_func = motion()

        for item in self.particle_list:
            if item.get_property('stop')[0] is True:
                if (item.get_property('stop')[1] == "horizontal") or (item.get_property('stop')[1] == "vertical"):
                    v_x, v_y = motion_func.collision(item.get_property('v_x'),
                                                     item.get_property('v_y'),
                                                     coefficient,
                                                     item.get_property('stop')[1])

                    item.set_property('stop', (False, ""))
                    item.set_property('x0', item.get_property('x'))
                    item.set_property('y0', item.get_property('y'))
                    item.set_property('v0_x', v_x)
                    item.set_property('v0_y', v_y)
                    item.set_property('start', item.get_property('start') + item.get_property('life'))
                    item.set_property('life', 0)

        return self.particle_list
