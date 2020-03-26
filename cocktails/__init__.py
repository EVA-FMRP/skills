from mycroft import MycroftSkill, intent_file_handler, intent_handler, \
                    AdaptIntent
from mycroft.util.log import LOG
import requests
import time


API_KEY = '2432'
API_URL = 'https://www.thecocktaildb.com/api/json/v1/{}/'.format(API_KEY)
SEARCH = API_URL + 'search.php'


def search_cocktail(name):
    r = requests.get(SEARCH, params={'s': name})
    if (200 <= r.status_code < 300 and 'drinks' in r.json() and
            r.json()['drinks']):
        return r.json()['drinks'][0]
    else:
        return None


def ingredients(drink):
    ingredients = []
    for i in range(1, 15):
        if not drink['strIngredient' + str(i)]:
            break
        ingredients.append(' '.join((drink['strMeasure' + str(i)],
                                    drink['strIngredient' + str(i)])))
    return nice_ingredients(ingredients)

def nice_ingredients(ingredients):
    units = {
        'oz': 'ounce',
        '1 tbl': '1 table spoon',
        'tbl': 'table spoons',
        '1 tsp': 'tea spoon',
        'tsp': 'tea spoons',
        'ml ': 'milliliter ',
        'cl ': 'centiliter '
    }
    ret = []
    for i in ingredients:
        for word, replacement in units.items():
            i = i.lower().replace(word, replacement)
        ret.append(i)
    return ret

class CocktailSkill(MycroftSkill):
    @intent_file_handler('Recipie.intent')
    def get_recipie(self, message):
        cocktail = search_cocktail(message.data['drink'])
        if cocktail:
            self.speak_dialog('YouWillNeed', {
                'ingredients': ', '.join(ingredients(cocktail)[:-1]),
                'final_ingredient': ingredients(cocktail)[-1]})
            time.sleep(1)
            self.speak(cocktail['strInstructions'])
            self.set_context('IngredientContext', str(ingredients(cocktail)))
        else:
            self.speak_dialog('NotFound')

    def repeat_ingredients(self, ingredients):
        self.speak(ingredients)

    @intent_file_handler('Needed.intent')
    def get_ingredients(self, message):
        cocktail = search_cocktail(message.data['drink'])
        if cocktail:
            self.speak_dialog('YouWillNeed', {
                'ingredients': ', '.join(ingredients(cocktail)[:-1]),
                'final_ingredient': ingredients(cocktail)[-1]})
            self.set_context('IngredientContext', str(ingredients(cocktail)))
        else:
            self.speak_dialog('NotFound')

    @intent_handler(AdaptIntent().require('Ingredients').require('What')
                                 .require('IngredientContext'))
    def what_were_ingredients(self, message):
        return self.repeat_ingredients(message.data['IngredientContext'])

    @intent_handler(AdaptIntent().require('Ingredients').require('TellMe')
                                 .require('Again')
                                 .require('IngredientContext'))
    def tell_ingredients_again(self, message):
        return self.repeat_ingredients(message.data['IngredientContext'])


def create_skill():
    return CocktailSkill()
