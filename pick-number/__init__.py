# This pick number skill is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The Pick Number skill is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util.log import LOG
import re
import random

__author__ = 'PCWii'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class PickNumberSkill(MycroftSkill):

    # The constructor of the skill, which calls Mycroft Skill's constructor
    def __init__(self):
        super(PickNumberSkill, self).__init__(name="PickNumberSkill")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))
        pick_number_intent = IntentBuilder("PickNumberIntent").\
            require("PickKeyword").\
            require("NumberKeyword").\
            require("BetweenKeyword").\
            require("AndKeyword").build()
        self.register_intent(pick_number_intent, self.handle_pick_number_intent)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_pick_number_intent(self, message):
        str_remainder = str(message.utterance_remainder())
        str_limits = re.findall('\d+', str_remainder)
        LOG.info('returned: ' + str(str_limits))
        if len(str_limits) == 2:
            int_first = int(str(str_limits[0]))
            int_second = int(str(str_limits[1]))
            if int_first < int_second:
                low_number = int_first
                high_number = int_second
            else:
                low_number = int_second
                high_number = int_first
            my_number = random.randint(low_number, high_number)
            self.speak_dialog("pick.number", data={"number": str(my_number)})
        else:
            self.speak_dialog("error")
       
    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return PickNumberSkill()
