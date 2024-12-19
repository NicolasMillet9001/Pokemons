from flask import Flask, render_template, request
from requests import get
from flask_assets import Environment, Bundle
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_babel import Babel, _

LANGUAGES = {
    'en': 'English',
    'fr': 'Français'
}

TIMEZONE_DEFAULT = 'Europe/Paris'

app = Flask(__name__)

app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # Langue par défaut
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']  # Langues supportées

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def get_timezone():
    return TIMEZONE_DEFAULT

Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)


# @app.route('/')
# def index():
#     return 'Hello World'




@app.route('/pokemons/')
def pokemons():
    response = get('https://studies.delpech.info/api/pokemons/dataset/json')
    
    if response.status_code == 200:
        #return response.json()

        return render_template('template_liste.html', pokemons=response.json())       
    
    return str(response.status_code)


@app.route('/pokemon/<id>')
def pokemon(id):
    response = get('https://studies.delpech.info/api/pokemons/dataset/'+id+'/json')
    
    if response.status_code == 200:
        return render_template('template_pokemon.html', pokemon=response.json())
    
    return response.status_code


@app.route('/api/pokemons/<id>')
def apiPokemons(id):
    response = get('https://studies.delpech.info/api/pokemons/dataset/'+id+'/json')
    
    if response.status_code == 200:
        return response.json()
    






@app.route('/test')
def test():
    response = get('https://studies.delpech.info/api/pokemons/dataset/json')
    return response.json()    

