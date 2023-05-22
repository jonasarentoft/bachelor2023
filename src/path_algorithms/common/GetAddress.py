import requests

def GetAddress(lon, lat):
    print(lon,lat)
    api_key = 'c2eeab87a4caca6efddfddae36b56875'
    url = f'http://api.positionstack.com/v1/reverse?access_key={api_key}&query={lon},{lat}&output=json'
    response = requests.get(url).json()
    data = response['data'][0]
    city = data['administrative_area']
    country = data['country']
    
    return city