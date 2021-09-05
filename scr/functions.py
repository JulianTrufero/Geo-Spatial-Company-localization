def getdata_fsq(url, city, venue):
    
    """

    """
    client_id = os.getenv("tok1")
    client_secret = os.getenv("tok2")
    url_ = f'{url}'
    c = city['coordinates'][0]
    c1 = city['coordinates'][1]
    parametros = {"client_id": client_id, "client_secret": client_secret, "v": "20180323", "ll": f'{c}, {c1}',
                  "query": venue, "limit": 55}
    resp = requests.get(url_, params=parametros).json()
    return resp

def datagenerator(url, city, cathegories):

    """

    """
    cath = cathegories
    data_ = []
    for c in cath:
        data = getdata_fsq(url, city, c)
        data_.append(data['response']['venues'])
    return data_


def getFromDict(dic,map_):

    """
    """
    return reduce(operator.getitem, map_, dic)


def type_point(gps):

    """
    """
    return {"type": "Point", "coordinates": gps}

def jsonxport(name, l):

    """
    """
    n = f'{name}.json'
    with open(n, 'w') as f:
        json.dump(l, f)

def jsongenerator(data, name):
    """
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
        ndic['location']= type_point([ndic["latitude"],ndic["longitude"]])
        l.append(ndic)
    return jsonxport(name, l)