# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 16:13:48 2015

@author: INSPIRON
"""

import math
import sqlite3

conn = sqlite3.connect('C:/Users/INSPIRON/Downloads/renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM location;") # execute a SQL command
Latitude=[]
Longitude=[]
Production=[]
Latitude_Port=[]
Longitude_Port=[]
for row in c:
    Longitude.append(row[0])
    Latitude.append(row[1])
    Production.append(row[2])
  
c.execute("SELECT * from ports;")
for row in c:
    Longitude_Port.append(row[0])
    Latitude_Port.append(row[1])
Production_Total=sum(Production)

print Longitude,Latitude,Production,Longitude_Port,Latitude_Port

def distance_sph(lat1, long1, lat2, long2):
    #Converting Latitude and longitude to radians
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    
#    637100 is the radius of the earth  

    distance=arc*6371000 
    return distance

print distance_sph(Latitude[0],Longitude[0],Latitude[1],Longitude[1])    
print distance_sph(Latitude[1],Longitude[1],Latitude[1],Longitude[1])    
print distance_sph(Latitude[1],Longitude[1],Latitude[2],Longitude[2])
print distance_sph(Latitude[0],Longitude[0],Latitude_Port[1],Longitude_Port[1])    


conn.close() 