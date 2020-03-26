#Copyright (C) 2018  danielwine/Daniel Vinkovics

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
from mycroft import MycroftSkill, intent_file_handler
import re
import random
import wikiquote

__author__ = 'danielwine'

class WikiQuoteSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.wikilang = self.lang.split('-')[0]
        self.exclude_list = ['ISBN', 'Citatum']

    def getRandomQuote(self, titles, mostRelevant=False, length=4, filterYear=True):
        quote = None
        quotes = None
        match = None
        counter = 0
        max_sentences = length
        while quote is None or len(quote.split('.')) > max_sentences:
            counter += 1
            if not mostRelevant: title = random.choice(titles)
            else: title = titles[0]
            try:
                quotes = wikiquote.quotes(title, lang=self.wikilang)
            except wikiquote.utils.DisambiguationPageException:
                quotes = None
            if quotes and quotes != []:
                quote = random.choice(quotes)
                if filterYear: match = re.match('.*([1-3][0-9]{3})', quote)
                if match: quote = None
                for word in self.exclude_list:
                    if quote and word in quote: quote = None
            if counter > 5: quote = ''
        return quote, title
        
    @intent_file_handler('specific.intent')
    def handle_specific_quote_intent(self, message):
        subject = message.data.get('subject')
        results = wikiquote.search(subject, lang=self.wikilang)
        if len(results) == 0:
            self.speak_dialog("notfound", {'subject': subject})
        else:
            quote, title = self.getRandomQuote(
                results, mostRelevant=True, length=10, filterYear=False)
            if quote == '': self.speak_dialog("notfound", {'subject': subject})
            else: self.speak(quote + ' (' + title + ')')

    @intent_file_handler('random.intent')
    def handle_random_quote_intent(self, message):
        randomtitles = []
        while randomtitles is None or randomtitles == []:
            randomtitles = wikiquote.random_titles(lang=self.wikilang)
        quote, title = self.getRandomQuote(randomtitles)
        self.speak(quote + ' (' + title + ')')


def create_skill():
    return WikiQuoteSkill()
