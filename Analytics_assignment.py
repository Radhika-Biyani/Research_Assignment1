# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 16:13:48 2015

@author: INSPIRON
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 15:46:38 2015

@author: INSPIRON
"""

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
    

def cost_transport_each_Location(Latitude,Longitude):
    cost_transport_location=[]
    for i in range(0,len(Longitude)):
          cost=0

          for j in range(0,len(Longitude)):
                d=distance_sph(Latitude[i],Longitude[i],Latitude[j],Longitude[j])
#                print d
                cost=cost+0.00125*d*Production[j]
#                print cost
          cost_transport_location.append(cost)
    return cost_transport_location  

    
def cost_transport_Port(Latitude,Longitude,Latitude_Port,Longitude_Port):
    min_cost_port=[]
    loc_closest_port=[]
    for i in range(0,len(Longitude)):
          cost_trans_port=0
          distance_port=[]
          for j in range(0,len(Longitude_Port)):
                distance_port.append(distance_sph(Latitude[i],Longitude[i],Latitude_Port[j],Longitude_Port[j]))
          cost_trans_port=cost_trans_port+0.00125*min(distance_port)*Production_Total
          loc_closest_port.append(distance_port.index(min(distance_port)))
#          print cost_p
          min_cost_port.append(cost_trans_port)
    return min_cost_port,loc_closest_port 



def minimum_Cost():
    cost_transport_location= cost_transport_each_Location(Latitude,Longitude)
    cost_transport_port,loc_closest_port= cost_transport_Port(Latitude,Longitude,Latitude_Port,Longitude_Port)

    final_cost = [sum(i) for i in zip(cost_transport_location,cost_transport_port)]
    print final_cost;
   

    index_min_cost=final_cost.index(min(final_cost))
   
    print "The location is ",index_min_cost,"And the port is",loc_closest_port[index_min_cost]

print minimum_Cost()

conn.close() 