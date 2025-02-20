from flask import Blueprint
from requests import get
from redis import StrictRedis
from http import HTTPStatus

api_bp = Blueprint('api', __name__)

redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    decode_responses=False
)

# Route pour obtenir les détails des pokemons
@api_bp.route('/pokemons/<id>')
def apiPokemons(id):
    response = get('https://studies.delpech.info/api/pokemons/dataset/'+id+'/json')

    if response.status_code == HTTPStatus.OK:
        return response.json(), HTTPStatus.OK
    

# Route pour obtenir les images des pokemons + mise en cache
@api_bp.route('/imgPokemons/<id>')
def apiImgPokemons(id):

    cached_image = redis_cli.get('pokemon_img_' + id)

    # Vérifie si les images sont sauvegardées en cache
    if redis_cli.exists('pokemon_img_' + id):
        # print('Pokemon img in cache')

        return cached_image, HTTPStatus.OK
    
    else:
        # print('Pokemon img not in cache')
        response = get('https://studies.delpech.info/api/pokemons/dataset/' + id + '/png')

        if response.status_code == HTTPStatus.OK:
            img_bytes = response.content
            # Mise en cache de l'image pendant 10 minutes
            redis_cli.set('pokemon_img_' + id, img_bytes, 600)
            return img_bytes, HTTPStatus.OK
        
        else:
            return HTTPStatus.NOT_FOUND