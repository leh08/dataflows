import json

default_locale = 'en-gb'
cached_strings = {}


def refresh():
    global cached_strings
    with open(f'configurations/locales/{default_locale}.json') as file:
        cached_strings = json.load(file)
        
def gettext(name):
    return cached_strings[name]
        
refresh()