from flask import Flask, render_template, request, send_file
from requests import get
from flask_assets import Environment, Bundle
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_babel import Babel, _
from redis import StrictRedis
import json
from PIL import Image
from io import BytesIO

redis_cli = StrictRedis(
    host='127.0.0.1',
    port=6379,
    charset="utf-8",
    decode_responses=True
)

response = get('https://studies.delpech.info/api/pokemons/dataset/1/png')

redis_cli.delete('pokemon_img_1')

if (redis_cli.exists('pokemon_img_1')):
    print('pokemon img in cache')
    img_data = redis_cli.get('pokemon_img_' + id)
    img_bytes = BytesIO(img_data)
    img = Image.open(img_bytes)
else :
    print('pokemon img not in cache')

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        redis_cli.set('pokemon_img_1',img_bytes.getvalue())
        img_bytes.seek(0)
    else:
        print(response.status_code)

print(send_file(img_bytes, mimetype='image/png'))




#Set your key
# if (redis_cli.exists('pokemons')==0):
#     print('Pokemons non cached')

#     response = get('https://studies.delpech.info/api/pokemons/dataset/json')
#     if response.status_code == 200:
#         redis_cli.set('pokemons', response.json())
#         redis_cli.expire('pokemons',3600)
# else:
#     print('Existant')


# print(redis_cli.get('pokemons')[1])
# #Get the value of inserted key