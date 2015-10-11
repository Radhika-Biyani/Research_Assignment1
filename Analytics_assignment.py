# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 15:46:38 2015

@author: Radhika Biyani (15204406)
"""


#Importing the modules to be used further
import math
import sqlite3


#Creating a connection to the SQLite3 module to access the database

conn = sqlite3.connect('C:/Users/INSPIRON/Downloads/renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM location;") # Selecting all elements of the table Location

#Creating Lists for storing the various elements of the the two tables respectively
Latitude=[]
Longitude=[]
Production=[]
Latitude_Port=[]
Longitude_Port=[]

#Storing the first column as longitude , 2nd as Latitude and  Last as Production from the location Table
for row in c:
    Longitude.append(row[0])
    Latitude.append(row[1])
    Production.append(row[2])
  
c.execute("SELECT * from ports;") # Selecting all elements of the table Ports

#Storing the first column as longitude_Port , 2nd as Latitude_Port  from the Ports Table

for row in c:
    Longitude_Port.append(row[0])
    Latitude_Port.append(row[1])
    
#Finding the total Production    
Production_Total=sum(Production)


#Finding the Distances Using Longitude and Latitude by the haversine Formula
def distance_sph(lat1, long1, lat2, long2):
    #Converting Latitude and longitude to radians
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates 
   
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    
    #    6371 is the radius of the earth in km  
    #Distance= ArcLength* radius 


    distance=arc*6371
    return distance
    
#Function to calculate the cost of transportation of Wood to a particular location from all the other locations
def cost_transport_each_Location(Latitude,Longitude):
    cost_transport_location=[] #List to store total cost of materials transported to that particular location
    for i in range(0,len(Longitude)):
          cost=0 
          for j in range(0,len(Longitude)):
                #Calculating distance to i-th location from every other location (j)
                d=distance_sph(Latitude[i],Longitude[i],Latitude[j],Longitude[j])
                
                #Assuming cost of transporting as 80.25 Euro per km for each truck which has a capacity of 40 tons.
                cost=cost+8.25*d*(Production[j]/40.0)
#                print cost
          cost_transport_location.append(cost)
    return cost_transport_location  


#Function to calculate the cost of transportation to the nearest port from any location.     
def cost_transport_Port(Latitude,Longitude,Latitude_Port,Longitude_Port):
    min_cost_port=[] #List to store the minimum cost to transport to port
    loc_closest_port=[] #List to store the indexes of the closest port from each location
    
    for i in range(0,len(Longitude)):
          cost_trans_port=0
          distance_port=[]
          for j in range(0,len(Longitude_Port)):
              #Storing the distance to every Port from each location in the list distance_port
                distance_port.append(distance_sph(Latitude[i],Longitude[i],Latitude_Port[j],Longitude_Port[j]))
          
          #Assuming same transport costs as above , but only calculating the transport cost to closest location
          
          cost_trans_port=cost_trans_port+8.25*min(distance_port)*(Production_Total/40.0)
          
          #Adding the closest ports location only to the list
          loc_closest_port.append(distance_port.index(min(distance_port)))
          min_cost_port.append(cost_trans_port)
    return min_cost_port,loc_closest_port 


#Function to find the least cost of transportation
def minimum_Cost():
    cost_transport_location= cost_transport_each_Location(Latitude,Longitude)
    cost_transport_port,loc_closest_port= cost_transport_Port(Latitude,Longitude,Latitude_Port,Longitude_Port)

    #The total final cost of transporting= Cost of Transport to location + Cost of transport to nearest port
    final_cost = [sum(i) for i in zip(cost_transport_location,cost_transport_port)]
    
    print "The total total cost to bring all material to each location and to transport to nearrest port is", final_cost;
   
   #Where the cost total is least , that location is selected as the final location
    index_min_cost=final_cost.index(min(final_cost))
   
   #Printing the final location , along with its corresponding ports location       
    print "The best location is location number",index_min_cost+1 ,"with longitude  and latitude as",Longitude[index_min_cost] ," ",Latitude[index_min_cost]
    print "And the best port for the above location is",loc_closest_port[index_min_cost]+1,"with longitude and latitude as" , Longitude_Port[loc_closest_port[index_min_cost]]," ",Latitude_Port[loc_closest_port[index_min_cost]]

#Printing the minimum Cost
print minimum_Cost()

conn.close() #Closing the sqlite connection