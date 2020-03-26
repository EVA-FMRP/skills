from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_number
import re
from . import brion_pysin_lib

class CutUp(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.string_to_frag = {'sentance':'sent'}
        if ( not self.settings.get('frag_type') ) or self.settings.get('frag_type') == 'None':
            self.settings['frag_type'] = 'word';
        if ( not self.settings.get('min_chunk') ) or self.settings.get('min_chunk') == 'None':
            self.settings['min_chunk'] = 1
        if ( not self.settings.get('max_chunk') ) or self.settings.get('max_chunk') == 'None':
            self.settings['max_chunk'] = 2
        if ( not self.settings.get('randomness') ) or self.settings.get('randomness') == 'None':
            self.settings['randomness'] = 75

    @intent_handler(IntentBuilder('CutUpSetFragmentType').require('CutUp').require('Set').require('FragmentType'))
    def handle_pysin_brion_set_frag(self, message):
        poss_frag = message.data.get('FragmentType')
        frag_type = self.string_to_frag.get( poss_frag, poss_frag ) # lib defaults to "char" ;)
        self.settings['frag_type'] = frag_type
        self.speak_dialog('frag_type.set', data={'frag_type':frag_type })

    @intent_handler(IntentBuilder('CutUpSetMinimum').require('CutUp').require('Set').require('Minimum'))
    def handle_pysin_brion_set_min(self, message):
        self.settings['min_chunk'] = extract_number( message.data.get('utterance') ) 
        self.speak_dialog('minimum.set', data={'min': extract_number( message.data.get('utterance') ) })

    @intent_handler(IntentBuilder('CutUpSetMaximum').require('CutUp').require('Set').require('Maximum'))
    def handle_pysin_brion_set_max(self, message):
        self.settings['max_chunk'] = extract_number( message.data.get('utterance') ) 
        self.speak_dialog('maximum.set', data={'max': extract_number( message.data.get('utterance') ) })

    @intent_handler(IntentBuilder('CutUpSetRandomness').require('CutUp').require('Set').require('Randomness'))
    def handle_pysin_brion_set_rand(self, message):
        self.settings['randomness'] = extract_number( message.data.get('utterance') ) 
        self.speak_dialog('randomness.set', data={'rand': extract_number( message.data.get('utterance') ) })

    # The normal use
    @intent_handler(IntentBuilder('CutUpSay').require('CutUp').require('Say'))
    def handle_pysin_brion(self, message):
        cutup = brion_pysin_lib.traditional_cutup( message.data.get('Say'), self.settings['frag_type'], self.settings['min_chunk'], self.settings['max_chunk'], self.settings['randomness'] )
        self.speak(cutup.strip())

def create_skill():
    return CutUp()

