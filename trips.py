#!/usr/bin/python
import time
import json
import numpy as np
import math
import matplotlib.pyplot as plt

def ReadTrips(name_of_file):

    with open(name_of_file) as tripdict:
        return(json.load(tripdict))

    close(name_of_file)

def FixTime(tiden):

    pattern = '%Y-%m-%d %H:%M:%S'
    transfertime = int(time.mktime(time.strptime(tiden ,pattern)))

    return transfertime

def OrderTripData(i, dataFile):

    trips = dataFile['trips']

    tid1 = FixTime(trips[i]['start_time'][:-6])
    tid2 = FixTime(trips[i]['end_time'][:-6])

    start_station = trips[i]['start_station_id']
    end_station = trips[i]['end_station_id']

    timeDifference = tid2 - tid1


    return start_station, end_station, timeDifference

def TransformPos(r, lat, lon):
    #Straight from tha undaground! neida, kopiert fra internett
   return(r*math.cos(lat)*math.cos(lon), r*math.cos(lat)*math.sin(lon), r*math.sin(lat))

def FindDistance(startcoord, endcoord, startheight, endheight):

    earth_radius = 6371*1000 #meter

    latStart = float(startcoord[0])*math.pi/180
    lonStart = float(startcoord[1])*math.pi/180

    a1,b1,c1 = TransformPos(startheight+earth_radius, latStart, lonStart)

    latEnd = float(endcoord[0])*math.pi/180
    lonEnd = float(endcoord[1])*math.pi/180

    a2,b2,c2 = TransformPos(endheight+earth_radius, latEnd, lonEnd)

    #calculate distance from euclidean points:
    distance = math.sqrt((a2-a1)**2 + (b2-b1)**2 + (c2-c1)**2)

    return distance

def main():

    tripsData = ReadTrips('trips-2018.4.1-2018.4.30.json')
    stationData = ReadTrips('stations.json')

    distance_array = []

    for i in range(len(tripsData['trips'])):

        startStasjon, endeStasjon, tidsForskjell = OrderTripData(i, tripsData)

        start = stationData.get(str(startStasjon))
        end = stationData.get(str(endeStasjon))

        if start and end != None:
            start_station = start.get('name')
            end_station = end.get('name')

            heightStart = start.get('elevation')
            heightEnd   = end.get('elevation')
            heightDiff = heightStart - heightEnd

            coordStart = start.get('coordinates')
            coordEnd   = end.get('coordinates')

            coordStart = coordStart.rsplit(',')
            coordEnd   = coordEnd.rsplit(',')

            distance = FindDistance(coordStart, coordEnd, heightStart, heightEnd)
            if distance != 0:
                distance_array.append(distance)

        elif start == None:
            print('\nStasjon ', startStasjon, ' er ute av drift...\n')
        elif end == None:
            print('\nStasjon ', endeStasjon, ' er ute av drift...\n')

        #print('\nTur fra ', start_station, ' til ', end_station, ' som varte i: ', tidsForskjell/60, ' minutter ', '\nHøydeforskjell: '
        #    , heightDiff, '\n', 'Lengde: ', distance, 'm\n')

    plt.hist(distance_array, bins=100)
    plt.title('Distance of trips in Oslo')
    plt.xlabel('distance in meters')
    plt.ylabel('number of trips')
    plt.show()


main()
