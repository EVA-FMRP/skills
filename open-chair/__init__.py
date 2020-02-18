# -*- coding: utf-8 -*-
# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import os
import time

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Tiago Chiaveri da Costa'

LOGGER = getLogger(__name__)


class OpenChairSkill(MycroftSkill):
    def __init__(self):
        super(OpenChairSkill, self).__init__(name="OpenChairSkill")

    def initialize(self):
        mouse_off_intent = IntentBuilder("MouseOffIntent"). \
            require("MouseOffKeyword").build()
        self.register_intent(mouse_off_intent, self.handle_mouse_off_intent)

        mouse_on_intent = IntentBuilder("MouseOnIntent"). \
            require("MouseOnKeyword").build()
        self.register_intent(mouse_on_intent, self.handle_mouse_on_intent)


    def handle_mouse_off_intent(self, message):
        self.speak_dialog("mouse.off")
        cmd = "uhubctl -a off -p 2  -l 1-1 -r 100"
        self.speak_dialog("chair")
        os.popen(cmd,)

    def handle_mouse_on_intent(self, message):
        self.speak_dialog("mouse.on")
        cmd = "uhubctl -a on -p 2  -l 1-1 -r 100"
        self.speak_dialog("thank")
        os.popen(cmd,)


    def stop(self):
        pass


def create_skill():
    return OpenChairSkill()
