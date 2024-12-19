from flask import Flask, render_template, request
from requests import get
from flask_assets import Environment, Bundle
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_babel import Babel, _
from redis import StrictRedis
import json

app = Flask(__name__)

#region redis
redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    charset="utf-8",
    decode_responses=True
)

# Set your key
# if (redis_cli.exists('pokemons')==0):
#     print('Pokemons non cached')

#     response = get('https://studies.delpech.info/api/pokemons/dataset/json')
    
#     if response.status_code == 200:
#         redis_cli.set('pokemons', response.json())
#         redis_cli.expire('pokemons',3600)

# else:
#     print('Pokemons cached')

#endregion

#region traduction
LANGUAGES = {
    'en': 'English',
    'fr': 'Français'
}

TIMEZONE_DEFAULT = 'Europe/Paris'


app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # Langue par défaut
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']  # Langues supportées

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def get_timezone():
    return TIMEZONE_DEFAULT

Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
#endregion

@app.route('/')
def index():
    pokemons()




@app.route('/pokemons/')
def pokemons():
    # response = get('https://studies.delpech.info/api/pokemons/dataset/json')
    
    # if response.status_code == 200:
    # #     return response.json()

    
    #Set your key
    if (redis_cli.exists('pokemons')==0):
        print('Pokemons non cached')

        response = get('https://studies.delpech.info/api/pokemons/dataset/json')
        if response.status_code == 200:
            redis_cli.set('pokemons', json.dumps(response.json()))
            redis_cli.expire('pokemons',3600)

        else:
            return str(response.status_code)

    else:
        print('Pokemons cached')

    pokemons_data = redis_cli.get('pokemons')
    return render_template('template_liste.html', pokemons=json.loads(pokemons_data))       
    


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

