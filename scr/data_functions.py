import json
from dotenv import load_dotenv
from functools import reduce
import numpy as np
import operator
import os
import pandas as pd
import requests
load_dotenv()

def getdata_fsq(url, city, venue, client_id, client_secret):
    """
    Toma como argumentos la url de la API, un par de coordenadas, una cateogoría y los tokens correspondientes
    para la API. Con esos argumentos define los parámetros de la request y devuelve un fichero json con 
    los lugares registrados en foursquare para esas coordenadas.
    """
    url_ = f'{url}'
    c = city['coordinates'][0]  
    c1 = city['coordinates'][1]
    parametros = {"client_id": client_id, "client_secret": client_secret, "v": "20180323", "ll": f'{c}, {c1}',
                  "query": venue, "limit": 55}
    resp = requests.get(url_, params=parametros).json()
    return resp

def datagenerator(url, city, cathegories, client_id, client_secret):
    """
    Toma como argumentos la url de la API, un par de coordenadas, una lista de cateogorías y los tokens correspondientes
    para la API. Por cada categoría, realiza una llamada a la API y devuelve una lista, donde cada 
    elemento es una lista de diccionarios por categoria
    """
    cath = cathegories
    data_ = []
    for c in cath:
        data = getdata_fsq(url, city, c, client_id, client_secret)
        data_.append(data['response']['venues'])
    return data_


def getFromDict(dic,map_):
    """
    Toma como argumento un diccionario, y una o varias keys del mismo. Y devuelve los valores correspondientes
    a las keys seleccionadas 
    """
    return reduce(operator.getitem, map_, dic)

def type_point(gps):
    """
    Toma como argumento un par de coordenadas, y devuelve un diccionario "type point"
    """
    return {"type": "Point", "coordinates": gps}

def jsonxport(name, l):
    """
    Toma como argumentos un nombre cualquiera, y una lista. Devuelve un fichero en formato json con el 
    nombre dado y la lista de base
    """
    n = f'{name}.json'
    with open(n, 'w') as f:
        json.dump(l, f)


def jsongenerator(data, name):
    """
    Toma como argumentos una lista de diccionarios y el nombre de una categoría. Genera una nueva lista de diccionarios
    con las keys especificadas más abajo y los valores que obtenemos del diccionario de entrada mediante la
    función getFromDict, y con esa nueva lista, genera un fichero json
    """
    d = data
    map_name = ['name']
    map_categories = ['categories']
    map_lat = ['location', 'lat']
    map_long = ['location', 'lng']
    l = []
    for dic in d:
        ndic = {}
        ndic['name']= getFromDict(dic,map_name)
        ndic['categories']= getFromDict(dic,map_categories)
        ndic['latitude']= getFromDict(dic,map_lat)
        ndic['longitude']= getFromDict(dic,map_long)
        if ndic['latitude'] < 0:
            ndic['location']= type_point([ndic["longitude"],ndic["latitude"]])
        else:
            ndic['location']= type_point([ndic["latitude"],ndic["longitude"]])
        l.append(ndic)
    return jsonxport(name, l)

def jsonsparis():
    """
    Genera un fichero json por cada categoría específicada en la lista de categorías utilizando los diccionarios
    de la ciudad de París generados con la función datagenerator.
    """
    cathegories_= ['veganp', 'airportp', 'garep', 'starbucksp', 'veterinairep', 'basketballp', 'ecolep']
    for l, c in zip(range(len(cathegories_)), cathegories_) :
         j = jsongenerator(paris[l], c)
    return j


def jsonsmelbourne():
    """
    Genera un fichero json por cada categoría específicada en la lista de categorías utilizando los diccionarios
    de la ciudad de Melbourne generados con la función datagenerator.
    """
    cathegories_= ['veganm', 'airportm', 'stationm', 'starbuckm', 'veterinarym', 'basketballm', 'schoolsm', 'nurseriesm']
    for l, c in zip(range(len(cathegories_)), cathegories_) :
         j = jsongenerator(melbourne[l], c)
    return j


def jsonssaopaulo():
    """
    Genera un fichero json por cada categoría específicada en la lista de categorías utilizando los diccionarios
    de la ciudad de Sao Paulo generados con la función datagenerator.
    """
    cathegories_= ['vegansp', 'airportsp', 'stationsp', 'starbucksp', 'veterinarysp', 'basketballsp', 'schoolssp']
    for l, c in zip(range(len(cathegories_)), cathegories_) :
         j = jsongenerator(sao_paulo[l], c)
    return j


def geoquering(cathegory, distance, collection, city):
    """
    Toma como argumentos una categoría, una distancia especificada en metros, el nombre de la colleción sobre 
    la que vamos a hacer la query y las coordenadas de la ciudad donde vamos a realizar la query.
    Nos devuelve una lista con los diccionarios de los sitios encontrados para esa categoría y en el radio
    de la distancia especificada
    """
    c = f'{cathegory}'
    cond1 = {'categories.name': c}
    cond2 = {"location": {"$near": {"$geometry": city, "$minDistance": 0 ,"$maxDistance": int(distance)}}}
    
    gquery = {'$and': [cond1, cond2]}
    l = list(collection.find(gquery))
    return l