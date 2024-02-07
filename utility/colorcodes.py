#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>
# https://github.com/martin-ueding/python-colorcodes

import subprocess

__docformat__ = "restructuredtext en"

class Colorcodes(object):
    """
    Provides ANSI terminal color codes which are gathered via the ``tput``
    utility. That way, they are portable. If there occurs any error with
    ``tput``, all codes are initialized as an empty string.

    The provided fields (plain strings, i. e. unicode) are listed below.

    Control:

    - bold
    - reset

    Colors:

    - blue
    - green
    - orange
    - red

    :license: MIT
    """
    def __init__(self):
        try:
            self.bold = subprocess.check_output("tput bold".split()).decode()
            self.reset = subprocess.check_output("tput sgr0".split()).decode()

            self.red = subprocess.check_output("tput setaf 1".split()).decode()
            self.green = subprocess.check_output("tput setaf 2".split()).decode()
            self.orange = subprocess.check_output("tput setaf 3".split()).decode()
            self.blue = subprocess.check_output("tput setaf 4".split()).decode()
            self.purple = subprocess.check_output("tput setaf 5".split()).decode()
            self.cyan = subprocess.check_output("tput setaf 6".split()).decode()
            self.white = subprocess.check_output("tput setaf 7".split()).decode()

            # Modification: Added background colors
            self.background_red = subprocess.check_output("tput setab 1".split()).decode()
            self.background_green = subprocess.check_output("tput setab 2".split()).decode()
            self.background_blue = subprocess.check_output("tput setab 4".split()).decode()

        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.reset = ""

            self.blue = ""
            self.green = ""
            self.orange = ""
            self.red = ""
            self.cyan = ""
            self.purple = ""
            self.white = ""

            # Modification: Added background colors
            self.background_red = ""
            self.background_green = ""
            self.background_blue = ""