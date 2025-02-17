from flask import Flask, render_template, request, send_file, redirect
from requests import get
from flask_assets import Environment, Bundle
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_babel import Babel, _
from redis import StrictRedis
import json
from PIL import Image
from blueprints.api_blueprint import api_bp
from blueprints.pages_blueprint import page_bp

app = Flask(__name__)
babel = Babel(app)

app.register_blueprint(api_bp)
app.register_blueprint(page_bp, url_prefix='/page/')

from assets import set_bundles

set_bundles(app)


#region redis
redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)
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
    return redirect('/page/pokemons')

# @app.route('/test')
# def test():
#     response = get('https://studies.delpech.info/api/pokemons/dataset/json')
#     return response.json()    

