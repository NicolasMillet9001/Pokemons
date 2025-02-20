from flask import Flask, render_template, request, send_file, Blueprint, jsonify
from requests import get
import json
from redis import StrictRedis
from http import HTTPStatus

page_bp = Blueprint('page', __name__)

redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)


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

    pokemons_data = redis_cli.get('pokemons')
    return render_template('template_liste.html', pokemons=json.loads(pokemons_data)), HTTPStatus.OK       
    

# Page détails des Pokemons
@page_bp.route('/pokemon/<id>')
def pokemon(id):
    response = get('https://studies.delpech.info/api/pokemons/dataset/'+id+'/json')
    
    if response.status_code == HTTPStatus.OK:
        return render_template('template_pokemon.html', pokemon=response.json()), HTTPStatus.OK
    else:
        return HTTPStatus.NOT_FOUND
    
    