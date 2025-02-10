from flask import Flask, render_template, request, send_file, Blueprint, jsonify
from requests import get
import json
from redis import StrictRedis

page_bp = Blueprint('page', __name__)

redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)



@page_bp.route('/pokemons/')
def pokemons():
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
    


@page_bp.route('/pokemon/<id>')
def pokemon(id):
    response = get('https://studies.delpech.info/api/pokemons/dataset/'+id+'/json')
    
    if response.status_code == 200:
        return render_template('template_pokemon.html', pokemon=response.json())
    
    return response.status_code