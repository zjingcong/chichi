#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2015/12/23'


import ConfigParser
import common
import logging


class module(object):
    def __init__(self, screen):
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        self.image_path = str(conf.get("path", "IMAGE_PATH"))
        self.tone_path = str(conf.get("path", "TONE_PATH"))
        self.button_path = str(conf.get("path", "BUTTON_PATH"))
        self.current_dir = common.CURRENT_DIR
        self.screen = screen

        self._image_load()
        self._tone_path_load()
        self._button_path_load()
        self._module_init()

    def _image_load(self):
        logging.info("-----------IMAGE LOADING----------")

    def _tone_path_load(self):
        logging.info("-----------TONE LOADING----------")

    def _button_path_load(self):
        logging.info("-----------BUTTONLOADING----------")

    def _module_init(self):
        logging.info("-----------MODULE LOADING----------")

    def display(self):
        logging.info("-----------MODULE DISPLAY----------")

    def main(self):
        return
