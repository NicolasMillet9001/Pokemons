from redis import StrictRedis
from requests import get
import json

redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    charset="utf-8",
    decode_responses=True
)

#Set your key
if (redis_cli.exists('pokemons')==0):
    print('Pokemons non cached')

    response = get('https://studies.delpech.info/api/pokemons/dataset/json')
    if response.status_code == 200:
        redis_cli.json().set('pokemons', response.json())
        redis_cli.expire('pokemons',3600)
else:
    print('Existant')


print(redis_cli.get('pokemons')[1])
#Get the value of inserted key