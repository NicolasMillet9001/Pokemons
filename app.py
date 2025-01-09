from flask import Flask, render_template, request, send_file
from requests import get
from flask_assets import Environment, Bundle
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_babel import Babel, _
from redis import StrictRedis
import json
from PIL import Image



app = Flask(__name__)

from assets import set_bundles

set_bundles(app)

#region redis
redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
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
        print('Pokemons in cache')

        response = get('https://studies.delpech.info/api/pokemons/dataset/json')
        if response.status_code == 200:
            redis_cli.set('pokemons', json.dumps(response.json()))
            redis_cli.expire('pokemons',600)

        else:
            return str(response.status_code)

    else:
        print('Pokemons not in cache')

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
    

@app.route('/api/imgPokemons/<id>')
def apiImgPokemons(id):
    redis_cli.delete('pokemon_img_' + id)
    cached_image = redis_cli.get('pokemon_img_' + id)
    if redis_cli.exists('pokemon_img_' + id):
        print('Pokemon img in cache')

        return cached_image
    else:
        print('Pokemon img not in cache')
        response = get('https://studies.delpech.info/api/pokemons/dataset/' + id + '/png')
        if response.status_code == 200:
            img_bytes = response.content
            redis_cli.set('pokemon_img_' + id, img_bytes, 600)
            return img_bytes
        else:
            return response.status_code






@app.route('/test')
def test():
    response = get('https://studies.delpech.info/api/pokemons/dataset/json')
    return response.json()    

