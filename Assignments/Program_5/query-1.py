"""
Program:
--------
    Program 5- query-1
Description:
------------
This program takes the command line arguments of source destination and radius and 
get the airport lat-lon points list in between source and target to be ploted on pygame window
Name: Sowjanya Nemani
Date: 5 July 2017
"""
from pymongo import MongoClient
import pprint as pp
from math import radians, cos, sin, asin, sqrt
import pygame
import time
import sys
#from main import*

temp=None
visited=[]
class mongoHelper(object):
   
    def __init__(self):
        self.client = MongoClient()
        self.db_airports = self.client.world_data.airports
        self.db_states = self.client.geo.states
        self.db_ap = self.client.world_data.ap

    def get_airports_in_poly(self,poly):
        """
        Get airports within some polygon
        Params:
            poly (object): geojson poly
        """
        state_airports = self.db_airports.find( { 'loc' : { '$geoWithin' : { '$geometry' : poly } } })

        ap_list = []
        for ap in state_airports:
            ap_list.append(ap)

        return ap_list

    def get_state_poly(self,state):
        state_poly = self.db_states.find_one({'code' : state})
        return(state_poly['loc'])

    def get_afb_airports(self):
        
        res = self.db_airports.find({"type" : "Military"})

        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_doc_by_keyword(self,db_name,field,key):
        if db_name == 'airports':
            res = self.db_airports.find({field : {'$regex' : ".*"+key+".*"}})
        else:
            res = self.states.find({field : {'$regex' : ".*"+key+".*"}})
        
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list
    """
    this function gets the nearest airport 
    and stops fetching when it reaches the target-the destination aiport
    """
    def get_nearest_neighbor(self,lon,lat,dlon,dlat,r,target):
        count=0            
        air_res = self.db_airports.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )
        min = 999999
        distance= self._haversine(float(lon),float(lat),dlon,dlat)        
        closest_ap=None                                           
        for ap in air_res:
            #temp=ap
            count=count+1             
            airport_name=ap['properties']['ap_iata']                       
            if airport_name in visited:                               
                pass
            elif airport_name==target:
                print("Reached")
                closest_ap=ap 
                return closest_ap           
            else:
                    visited.append(airport_name)                                                     
                    lon2 = float(ap['geometry']['coordinates'][0])       
                    lat2 = float(ap['geometry']['coordinates'][1])                    
                    d1=self._haversine(float(dlon),float(dlat),lon2,lat2)#distance from destination                    
                    d = self._haversine(float(lon),float(lat),lon2,lat2) #distance from Source                    
                    temp=ap                   
                    if d1 <distance:            
                        #if d<min:                            
                            min = d                                    
                            closest_ap = ap 
                    else:                                                                                              
                        pass
        if closest_ap is None:                   
             closest_ap = temp           
             return temp  
        else:             
            return closest_ap
              
        
    def get_state_by_point(self,point):
        return self.db_states.find_one({'loc':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def get_state_by_name(self,name):
        pass
    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r


def main():
    mh = mongoHelper()
    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024,512)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Query-1')
    screen.fill(background_colour)
    pygame.init()
    bg = pygame.image.load("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program5\\main.png")
    running = True   
            
    """
    getting the co-ordinates of the Source airport and Destination airports in
    src_lat,src_long and des_lat,des_long """   
    if  len(sys.argv)<4:
        print("Insuffucient arguments given")
        print("Please give commandline arguments as: SRC DES RAD")
    else: 
        source=sys.argv[1]
        target=sys.argv[2]
        radius= 3000   
        visited.append(source)
        res=mh.db_airports.find_one({'properties.ap_iata':source},{'geometry.coordinates':1,'_id':0});          
        for g,c in res.items():
            for k,points in c.items():
                src_lon=points[0]
                src_lat=points[1]                         
        res1=mh.db_airports.find_one({'properties.ap_iata':target},{'geometry.coordinates':1,'_id':0});           
        for g,c in res1.items():
            for k,points in c.items():
                des_long=points[0]
                des_lat=points[1] 
        print("------------------------------------")
        print("Start: ",source)
        points=[]
        adjusted=[]
        while True:            
            tup=(src_lon,src_lat)
            points.append(tup)            
            next_nearest=mh.get_nearest_neighbor(src_lon,src_lat,des_lat,des_long,radius,target)                     
            new_airport=next_nearest['properties']['ap_iata']        
            visited.append(new_airport)                                
            src_lon=next_nearest['geometry']['coordinates'][0]
            src_lat=next_nearest['geometry']['coordinates'][1]                   
            print(next_nearest['properties']['ap_name'])             
            if(new_airport==target):
                tup=(src_lon,src_lat)
                points.append(tup)                       
                break        

        while running:            
            screen.blit(bg, (0, 0))
            closed=False                            
            pygame.draw.aalines(screen,(0,255,0),closed,points,1)           
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clean_area(screen,(0,0),width,height,(255,255,255))    
            running=False                      
        pygame.display.flip()
        pygame.image.save(screen,'C:\\Users\\sowja\\Documents\\SPDS\\query-1.png')
        running=False                  

if __name__=='__main__':
    main()