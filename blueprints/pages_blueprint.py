from flask import render_template, Blueprint
from requests import get
import json
from redis import StrictRedis
from http import HTTPStatus
from marshmallow import Schema, fields

page_bp = Blueprint('page', __name__)

redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)

class PokemonSchema(Schema):
    id = fields.Int()
    name = fields.Dict(keys=fields.Str(), values=fields.Str())
    url = fields.Url()
    lastEdit = fields.Int()


# Page liste des Pokemons
@page_bp.route('/pokemons/')
def pokemons():
    # Si les données des pokemons sont sauvegardées en cache 
    if (redis_cli.exists('pokemons')==0):
        # print('Pokemons in cache')

        response = get('https://studies.delpech.info/api/pokemons/dataset/json')
        if response.status_code == HTTPStatus.OK:
            redis_cli.set('pokemons', json.dumps(response.json()))
            # Durée de la mise en cache : 10 min
            redis_cli.expire('pokemons',600)

        else:
            return HTTPStatus.NOT_FOUND

    else:
        print('Pokemons not in cache')

    # Load les données JSON sur le schema PokemonSchema
    pokemons_data = redis_cli.get('pokemons')
    pokemons_json = json.loads(pokemons_data)
    pokemon_schema = PokemonSchema(many=True)
    pokemons = pokemon_schema.load(pokemons_json)

    return render_template('template_liste.html', pokemons=pokemons), HTTPStatus.OK       
    

# Page détails des Pokemons
@page_bp.route('/pokemon/<id>')
def pokemon(id):
    response = get('https://studies.delpech.info/api/pokemons/dataset/'+id+'/json')
    
    if response.status_code == HTTPStatus.OK:
        return render_template('template_pokemon.html', pokemon=response.json()), HTTPStatus.OK
    else:
        return HTTPStatus.NOT_FOUND
    
    