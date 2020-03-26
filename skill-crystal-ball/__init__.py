#Copyright (C) 2018  Arc676/Alessandro Vinciguerra <alesvinciguerra@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation (version 3)

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG, getLogger

__author__ = 'Arc676/Alessandro Vinciguerra'
LOGGER = getLogger(__name__)

class CrystalBallSkill(MycroftSkill):

    @intent_handler(IntentBuilder("").require("CrystalBall"))
    def handle_crystalball_intent(self, message):
    	self.answer()

    @intent_handler(IntentBuilder("").require("Query").require("Future"))
    def handle_future_intent(self, message):
    	self.answer()

    def answer(self):
        # Mycroft responds with a random yes/no answer
        self.speak_dialog("random.answer")

def create_skill():
    return CrystalBallSkill()
