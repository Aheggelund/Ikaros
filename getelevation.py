#!/usr/bin/python
import csv
import requests
import json
import numpy as np
import time


#make a request to bysykkel API, hopefully get coordinates of stations
def GetStationCoordinates():

    api_url = 'https://oslobysykkel.no/api/v1/stations'

    identifier = '1c7ac3580d3eb75264c85d9f292bc166'

    headers = {'Client-Identifier': identifier}
    #def get_account_info

    print('Connecting to OsloCityBike server...')

    response = requests.get(api_url, headers = headers)

    if response:
        print("Successfully extracted data from OsloCityBike API")
    else:
        print("No connection to internet")
    #print(response.status_code)

    result = response.json()
    stations = result["stations"]

    location       = []
    station_number = []
    station_name   = []
    coordinates    = []

    for i in range(len(stations)):

        location.append(stations[i].get("center"))
        station_number.append(stations[i].get("id"))
        station_name.append(stations[i].get("title"))

    for entry in range(len(location)):

        coordinates.append(str(location[entry].get('latitude'))+','+str(location[entry].get('longitude')))

    return coordinates, station_name, station_number

#requesting response from Google API to get elevation, input is latitude and longitude of stations.
def ElevationCalc(coordinate):

    #ID key for sending requests to elevationAPI server
    key = 'AIzaSyBAss5N7ai3xWRR3owFtnwWyl93FNjRGJM'
    api_elevation = 'https://maps.googleapis.com/maps/api/elevation/'+'json'+'?'+'locations='+coordinate+'&'+'key='+key
    response_GoogleAPI = requests.get(api_elevation)
    elevation = response_GoogleAPI.json()

    return elevation

#Main function, does what a main function does
def Main():

    #Extract coordinates, names of stations and the id of stations from bysykkel API
    coordinates, station_name, station_number = GetStationCoordinates()

    #tripsData = ReadTrips('trips-2018.4.1-2018.4.30.json')

    #startStasjon, endeStasjon, tidsForskjell = OrderTripData(tripsData)

    dict_station = {}
    for i in range(len(coordinates)):
        values_dict = {}

        #find elevation of stations
        values = ElevationCalc(coordinates[i])
        results = values.get("results")
        station_elevation = results[0].get("elevation")

        #place values in dictionary
        values_dict['name']        = station_name[i]
        values_dict['elevation']   = int(station_elevation)
        values_dict['coordinates'] = coordinates[i]
        dict_station[str(station_number[i])] =  values_dict

    with open('stations.json', 'w') as fp:
        json.dump(dict_station, fp)

Main()
