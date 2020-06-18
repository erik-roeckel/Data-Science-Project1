import os, sys, argparse
import pandas as pd
from math import cos, asin, sqrt

if len(sys.argv) < 2:
    raise ValueError('You did not provide valid command line arguments.')

baseURL = sys.argv[1]
stationInfoURL = baseURL + '/station_information.json'
stationStatusURL = baseURL + '/station_status.json'
command = sys.argv[2]

def total_bikes():
    df = getData(stationStatusURL)
    stations = df['data'].stations
    availableBikes = 0
    for station in stations:
        availableBikes += station['num_bikes_available']
    print('Command='+ command)
    print('Parameters=')
    print('Output='+ str(availableBikes))

def total_docks():
    df = getData(stationStatusURL)
    stations = df['data'].stations
    availableDocks = 0
    for station in stations:
        availableDocks += station['num_docks_available']
    print('Command='+ command)
    print('Parameters=')
    print('Output='+ str(availableDocks))

def percent_avail(station_id):
    df = getData(stationStatusURL)
    stations = df['data'].stations
    percentageAvailable = 0
    for station in stations:
        if(station_id == station['station_id']):
            percentageAvailable = station['num_docks_available']/(station['num_docks_available'] + station['num_bikes_available'])
    percentageAvailable *= 100      
    print('Command=' + command)
    print('Parameters=' + station_id)
    print('Output='+ str(int(percentageAvailable)) + '%')

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest_stations(latitude, longitude):
    df = getData(stationInfoURL)
    stations = df['data'].stations
    closestStations = [100, 100, 100]
    stationInfo = [None, None, None]
    for station in stations:
        d = distance(float(latitude), float(longitude), station['lat'], station['lon'])
        if(d < closestStations[0] or closestStations[0] == 100):
            closestStations[2] = closestStations[1]
            closestStations[1] = closestStations[0]
            closestStations[0] = d
            stationInfo[2] = stationInfo[1]
            stationInfo[1] = stationInfo[0]
            stationInfo[0] = {'id': station['station_id'], 'name': station['name']}
        elif(d < closestStations[1] or closestStations[1] == 100):
            closestStations[2] = closestStations[1]
            closestStations[1] = d
            stationInfo[2] = stationInfo[1]
            stationInfo[1] = {'id': station['station_id'], 'name': station['name']}
        elif(d < closestStations[2] or closestStations[2] == 100):
            closestStations[2] = d
            stationInfo[2] = {'id': station['station_id'], 'name': station['name']}
    
    print('Command=' + command)
    print('Parameters=' + latitude + ' ' + longitude)
    print('Output= \n'+ stationInfo[0]['id'] + ', ' + stationInfo[0]['name']+ '\n' + stationInfo[1]['id'] + ', ' + stationInfo[1]['name'] + '\n' + stationInfo[2]['id'] + ', ' + stationInfo[2]['name'])

def closest_bike(latitude, longitude):
    df = getData(stationInfoURL)
    dataFrame = getData(stationStatusURL)
    stations = df['data'].stations
    status = dataFrame['data'].stations
    closestDistance = 0
    stationInfo = None
    for station in stations:
        d = distance(float(latitude), float(longitude), station['lat'], station['lon'])
        for st in status:
            if(stationInfo == None and st['station_id'] == station['station_id'] and st['num_bikes_available'] > 0):
                closestDistance = d
                stationInfo = {'id': station['station_id'], 'name': station['name']}
            elif(d < closestDistance and st['station_id'] == station['station_id'] and st['num_bikes_available'] > 0):
                closestDistance = d
                stationInfo = {'id': station['station_id'], 'name': station['name']}
            
    print('Command=' + command)
    print('Parameters=' + latitude + ' ' + longitude)
    print('Output=' + stationInfo['id'] + ', ' + stationInfo['name'])

def station_bike_avail(latitude, longitude):
    df = getData(stationInfoURL)
    dataFrame = getData(stationStatusURL)
    stations = df['data'].stations
    status = dataFrame['data'].stations
    stationInfo = None
    validLatAndLon = False
    for station in stations:
        if(station['lat'] == float(latitude) and station['lon'] == float(longitude)):
            validLatAndLon = True
            for st in status:
                if(station['station_id'] == st['station_id']):
                    stationInfo = {'id': station['station_id'], 'bikes_avail': st['num_bikes_available']}
    if(validLatAndLon == False):
        print('You did not enter a valid station latitude and longitude!')
        return
    
    print('Command=' + command)
    print('Parameters=' + latitude + ' ' + longitude)
    print('Output=' + stationInfo['id'] + ', ' + str(stationInfo['bikes_avail']))

def determine_command(command):
    if(command == 'total_bikes' and len(sys.argv) == 3):
        total_bikes()
    elif(command == 'total_docks' and len(sys.argv) == 3):
        total_docks()
    elif(command == 'percent_avail' and len(sys.argv) == 4):
        percent_avail(sys.argv[3])
    elif(command == 'closest_stations' and len(sys.argv) == 5):
        closest_stations(sys.argv[3], sys.argv[4])
    elif(command == 'closest_bike' and len(sys.argv) == 5):
        closest_bike(sys.argv[3], sys.argv[4])
    elif(command == 'station_bike_avail' and len(sys.argv) == 5):
        station_bike_avail(sys.argv[3], sys.argv[4])
    else:
        print("You did not provide valid command line arguments")
        print("""Correct examples: 
        '1) python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_bikes'
        '2) python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_docks'
        '3) python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ percent_avail 342885
        '4) python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_stations 40.444618 -79.954707'
        '5) python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_bike 40.444618 -79.954707'
        '6) python3 bikepgh.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ station_bike_avail 40.444618 -79.954707'
        """)

def getData(url):
    data = pd.read_json(url)
    df = pd.DataFrame(data)
    return df

determine_command(sys.argv[2])
    
