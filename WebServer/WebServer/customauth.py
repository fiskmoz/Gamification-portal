import requests
APIaddr = 'http://127.0.0.1:7000/'

def login(request): 
    if request.method == "POST": 
        r = requests.get(APIaddr + 'auth/', )
    if request.method == "GET": 
        