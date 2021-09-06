import json
from dotenv import load_dotenv
from functools import reduce
import operator
import os
import requests
import sys
sys.path.append('../')
import scr.data_functions as cf

load_dotenv()

client_id = os.getenv("tok1")
client_secret = os.getenv("tok2")

#### PARIS: Palais Garnier 

paris_ = {'type': 'Point', 'coordinates': [48.87241163769417,2.3317031342524017]}

cathegories_p = ['vegan', 'airport', 'gare', 'starbucks', 'veterinaire', 'basketball', 'ecole']

paris = cf.datagenerator('https://api.foursquare.com/v2/venues/search', paris_, cathegories_p, client_id, client_secret)

cf.jsonsparis()

#### MELBOURNE CBD

melbourne_cbd = {'type': 'Point', 'coordinates': [-37.81227175879301,144.96262186884945]}

cathegories_m = ['vegan', 'airport', 'station', 'starbucks', 'veterinary', 'basketball', 'school', 'daycare']

melbourne = cf.datagenerator('https://api.foursquare.com/v2/venues/search', melbourne_cbd, cathegories_m, client_id, client_secret)

cf.jsonsmelbourne()

#### SAO PAULO: Zona Central

sao_paulo_zc = {'type': 'Point', 'coordinates': [-23.533215960575276,-46.639408758375076]}

cathegories_s = ['vegan', 'airport', 'estacao', 'starbucks', 'veterinaria', 'basketball', 'escola']

sao_paulo = cf.datagenerator('https://api.foursquare.com/v2/venues/search', sao_paulo_zc, cathegories_s, client_id, client_secret)

cf.jsonssaopaulo()