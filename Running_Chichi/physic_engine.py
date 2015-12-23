# -*- coding: utf-8 -*-
# author: zjingcong
# v_1.0

import random
import math
import logging


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
        situation2 = pos_2[1] < pos_1[1]
        situation3 = pos_2[0] > (pos_1[0] + error_tolerance[0])
        situation4 = (pos_2[0] + l_2) < (pos_1[0] + l_1 - error_tolerance[0])
        if situation1 and situation2 and situation3 and situation4:
            return True
        else:
            return False

    @staticmethod
    def detect_on_the_ground(v_y, g, error_tolerance):
        l = math.pow(v_y, 2) / (2 * g)
        if l <= error_tolerance:
            return True
        else:
            return False


COLLISION_ROTATION_RANGE = (-30, 30)


class group_motion:
    class particle:
        def __init__(self, particle_image):
            self.particle_image = particle_image
            self.argv_dict = {'x': 0, 'y': 0, 'v_x': 0, 'v_y': 0,
                              'v0_x': 0, 'v0_y': 0, 'x0': 0, 'y0': 0,
                              'rotation': 0,
                              'end': -1, 'start': -1, 'life': -1,
                              'stop': (True, ""), "split_time": 0}
            self.rotation = self.argv_dict['rotation']
            self.pos = self.get_pos()

        def get_property(self, name):
            if name in self.argv_dict:
                return self.argv_dict[name]
            else:
                logging.warning("ERROR: No Attribution.")

        def set_property(self, name, value):
            if name in self.argv_dict:
                self.argv_dict[name] = value
            else:
                logging.warning("ERROR: No Attribution.")

        def fresh_properties(self, argv_dict_new):
            self.argv_dict = argv_dict_new

            return self.argv_dict

        def set_split_time(self, split_time_range):
            split_time = random.randint(split_time_range[0], split_time_range[1])
            self.set_property('split_time', split_time)

            return split_time

        def set_rotation(self):
            rotation = random.randint(COLLISION_ROTATION_RANGE[0], COLLISION_ROTATION_RANGE[1])
            self.set_property('rotation', rotation + self.get_property('rotation'))
            self.rotation = rotation

            return rotation

        def get_pos(self):
            x = self.get_property('x')
            y = self.get_property('y')
            self.pos = (x, y)

            return self.pos

    def __init__(self, num, particle_image):
        self.num = num
        self.particle_list = []
        self.particle_image = particle_image
        self.motion_func = motion()
        self.particle_image = particle_image
        self.group_collision_time = 0
        self._init_group(self.num, self.particle_list)

    def _init_group(self, num, particle_list):
        for i in range(num):
            p = self.particle(self.particle_image)
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
            item.set_property('end', 0)
            item.set_property('start', t_start)
            item.set_property('stop', (False, ""))
            item.set_property('split_time', split_time)

        return self.particle_list

    def group_throwing_motion(self, time_now, a, ground, ceil, wall):
        global A_g
        A_g = a

        for item in self.particle_list:
            if item.get_property('stop')[0] is not True:
                item.set_property('end', (time_now - item.get_property('start')))
                item.set_property('life',
                                  (item.get_property('end') - item.get_property('start') + item.get_property('life')))

                v0_x = item.get_property('v0_x')
                v0_y = item.get_property('v0_y')
                x0 = item.get_property('x0')
                y0 = item.get_property('y0')
                t = item.get_property('end')

                [x, y, v_x, v_y] = self.motion_func.throwing_motion(v0_x, v0_y, x0, y0, a, t)

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

    def group_split(self, coefficient):
        self.clear()
        split_list = []
        for item in self.particle_list:
            if (item.get_property('stop')[0] is True) and (item.get_property('end') != -3):
                item.set_property('split_time', item.get_property('split_time') - 1)
                if item.get_property('split_time') == 0:
                    self.num += 1
                    logging.info("----------Particle split BEGIN----------")
                    logging.info("BEFORE %s" % str(item.argv_dict))

                    if item.get_property('stop')[1] == "horizontal":
                        split_item = self.particle(item.particle_image)

                        split_item.set_property('x', item.get_property('x'))
                        split_item.set_property('y', item.get_property('y'))
                        split_item.set_property('v_x', 0 - coefficient * item.get_property('v_x'))
                        split_item.set_property('v_y', coefficient * item.get_property('v_y'))
                        split_item.set_property('end', 0)
                        split_item.set_property('start', item.get_property('start') + item.get_property('end'))
                        split_item.set_property('stop', (True, "horizontal"))
                        split_item.set_split_time(split_range)

                        split_list.append(split_item)

                    elif item.get_property('stop')[1] == "vertical":
                        split_item = self.particle(item.particle_image)

                        split_item.set_property('x', item.get_property('x'))
                        split_item.set_property('y', item.get_property('y'))
                        split_item.set_property('v_x', item.get_property('v_x'))
                        split_item.set_property('v_y', 0 - item.get_property('v_y'))
                        split_item.set_property('end', 0)
                        split_item.set_property('start', item.get_property('start') + item.get_property('end'))
                        split_item.set_property('stop', (True, "vertical"))
                        split_item.set_split_time(split_range)

                        split_list.append(split_item)

                    logging.info("AFTER [OLD] %s" % str(item.argv_dict))
                    logging.info("AFTER [NEW] %s" % str(split_item.argv_dict))
                    logging.info("----------Particle split END----------")

        self.particle_list.extend(split_list)

        return self.particle_list

    def group_collision(self, coefficient):
        self.clear()
        for item in self.particle_list:
            if (item.get_property('stop')[0] is True) and (item.get_property('end') != -3):
                if (item.get_property('stop')[1] == "horizontal") or (item.get_property('stop')[1] == "vertical"):
                    self.group_collision_time += 1
                    logging.info("----------Particle collision BEGIN----------")
                    logging.info("BEFORE %s" % str(item.argv_dict))

                    v_x, v_y = self.motion_func.collision(item.get_property('v_x'),
                                                     item.get_property('v_y'),
                                                     coefficient,
                                                     item.get_property('stop')[1])

                    item.set_property('stop', (False, ""))
                    item.set_property('x0', item.get_property('x'))
                    item.set_property('y0', item.get_property('y'))
                    item.set_property('v0_x', v_x)
                    item.set_property('v0_y', v_y)
                    item.set_property('v_x', v_x)
                    item.set_property('v_y', v_y)
                    item.set_property('start', item.get_property('start') + item.get_property('end'))
                    item.set_property('end', 0)
                    item.set_rotation()

                    logging.info("AFTER %s" % str(item.argv_dict))
                    logging.info("----------Particle collision END----------")

        return self.particle_list

    def clear_particle(self, item):
        if item in self.particle_list:
            info = "REMOVE ITEM: %d%s" % (self.particle_list.index(item), str(item.argv_dict))
            self.particle_list.remove(item)
            logging.info(info)
        else:
            logging.warning("ERROR: Particle is not in the list.")

    def clear(self):
        for item in self.particle_list:
            if ((item.get_property('stop')[0]) is True)\
                    and (item.get_property('stop')[1] == "horizontal")\
                    and (item.get_property('y') > 300):
                v_y = item.get_property('v_y')
                if self.motion_func.detect_on_the_ground(v_y, A_g, 50):
                    item.set_property('end', -3)
