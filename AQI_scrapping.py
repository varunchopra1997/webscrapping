import requests
import pandas as pd

def item_flat(item):
    record=[]
    data=[]
    data.append(item['city']['name'])
    data.append(item['aqi'])
    data.append(item['city']['geo'][0])
    data.append(item['city']['geo'][1])
    
    try:
        data.append(item['iaqi']['co']['v'])
    except:
        data.append('None')
    try:
        data.append(item['iaqi']['no2']['v'])
    except:
        data.append('None')
    try:
        data.append(item['iaqi']['o3']['v'])
    except:
        data.append('None')
    try:
        data.append(item['iaqi']['so2']['v'])
    except:
        data.append('None')
    try:
        data.append(item['iaqi']['pm10']['v'])
    except:
        data.append('None')
    try:
        data.append(item['iaqi']['pm25']['v'])
    except:
        data.append('None')
    try:
        data.append(item['time']['s'])
    except:
        data.append('None')


    record+=[data]
    return record



data=[]
record=[]

api_key='95cdbb0758cb209e7485dd3daf69fae76f71fc7e'
endpoint_url='https://api.waqi.info/feed/delhi/?token='
endpoint_url+= api_key


usa=['Montgomery', 'Phoenix', 'Little Rock', 'Sacramento', 'Denver', 'Hartford', 'Tallahassee', 'Atlanta', 'Honolulu', 'Boise', 'Springfield', 'Indianapolis', 'Des Moines', 'Topeka', 'Frankfort', 'Baton Rouge', 'Augusta', 'Boston', 'Lansing', 'Saint Paul', 'Jackson', 'Jefferson City', 'Helena', 'Lincoln', 'Concord', 'Trenton', 'Albany', 'Raleigh', 'Bismarck', 'Columbus', 'Oklahoma City', 'Salem', 'Harrisburg', 'Providence', 'Columbia', 'Nashville', 'Austin', 'Salt Lake City', 'Richmond', 'Olympia', 'Charleston', 'Madison', 'Cheyenne']


for city in usa:
    api_key='95cdbb0758cb209e7485dd3daf69fae76f71fc7e'
    endpoint_url='https://api.waqi.info/feed/'+city+'/?token='
    endpoint_url+= api_key
    response= requests.get(endpoint_url)
    received_data= requests.get(endpoint_url).json()
    data.append(received_data['data'])


output=[]
for item in data:
    output+=item_flat(item)


headers= ['station','aqi','latitude','longitude','co','no2','o3','so2','pm10','pm2.5','time']

df= pd.DataFrame(output,columns=headers)

df.to_csv('aqi_scrapping_data.csv',header=True, index=False)

