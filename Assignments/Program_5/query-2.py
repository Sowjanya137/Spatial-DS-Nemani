"""
Program:
--------
    Program 5- query-1
Description:
------------
    This program takes the command line arguments as:
    feature field filed-value min/max radius lat lon (mandatorily)
    say: earthquakes magnitude 5 min 0 2000 -90.88 14.5 
    the resultant points ploted on pygame window with respective colors
Name: Sowjanya Nemani
Date: 5 July 2017
"""
import sys
from pymongo import MongoClient
import pprint as pp
from math import radians, cos, sin, asin, sqrt
import pygame
import time
from map_helper import*

visited=[]
class mongoHelper(object):
   
    def __init__(self):
        self.client = MongoClient()
        self.db_airports = self.client.world_data.airports
        self.db_states = self.client.world_data.state_borders
        self.db_ap = self.client.world_data.world_cities
        self.db_countries=self.client.world_data.countries
        self.db_earthquakes=self.client.world_data.earthquakes
        self.db_globalterrorism=self.client.world_data.globalterrorism
        self.db_meteorite=self.client.world_data.meteorite
        self.db_volcanos=self.client.world_data.volcanos
    
    def get_doc_by_keyword(self,db_name,field,key):
        if db_name == 'airports':
            res = self.db_airports.find({field : {'$regex' : ".*"+key+".*"}})
        else:
            res = self.states.find({field : {'$regex' : ".*"+key+".*"}})
        
        res_list = []
        for r in res:
            res_list.append(r)
        return res_list

    def mercX(self,lon,zoom = 1):
            lon = math.radians(lon)
            a = (256 / math.pi) * pow(2, zoom)
            b = lon + math.pi
            return a * b

    def mercY(self,lat,zoom = 1):
            lat = math.radians(lat)
            a = (256.0 / math.pi) * pow(2, zoom)
            b = math.tan(math.pi / 4 + lat / 2)
            c = math.pi - math.log(b)
            return (a * c)

    """
    This function goes into respective feature condition and returns the result
    """
    def get_nearest_feature(self,feature,field,field_value,minormax,vcount,rad,vlon,vlat):
        #print("function call:",feature)
        properties_field="'"+feature+"."+field+"'" 
        #print(properties_field)      
        if feature=='volcanos':            
            if minormax=='min':
                vol_res=self.db_volcanos.find( {'geometry' : { '$geoWithin': { '$centerSphere': [[vlon,vlat],rad/3963.2]}},'properties.Altitude' : {'$gte': field_value}})
            else:
                vol_res=self.db_volcanos.find( {'geometry' : { '$geoWithin': { '$centerSphere': [[vlon,vlat],rad/3963.2]}}, 'properties.Altitude': {'$lt': field_value}})    
            return vol_res
        elif feature=='earthquakes':            
            if minormax=='min':
               eqs_res=self.db_earthquakes.find( {'geometry' : { '$geoWithin': { '$centerSphere': [[vlon,vlat],rad/3963.2]}}, 'properties.mag': {'$gte': field_value}})
            else:
                eqs_res=self.db_earthquakes.find( {'geometry' : { '$geoWithin': { '$centerSphere': [[vlon,vlat],rad/3963.2]}}, 'properties.mag': {'$lt': field_value}})    
            return eqs_res
        else:            
            print("function call:",field)
            if minormax=='min':               
                mt_res=self.db_meteorite.find( {'geometry' : { '$geoWithin': { '$centerSphere': [[vlon,vlat],2000/3963.2]}}, 'properties.year': {'$gte':field_value}})
            else:
                mt_res=self.db_meteorite.find( {'geometry' : { '$geoWithin': { '$centerSphere': [[vlon,vlat],rad/3963.2]}}, 'properties.mass': {'$lt': field_value}})    
            return mt_res                        
        
    

def main():
    #getting mandatorily 8 arguments
    if len(sys.argv)<8:
        print("please enter:query-2.py volcanos Altitude 3000 min 3 1000 -90.88 14.5")
        print("or python query-2.py meteorite year 2010 min 0 2000 159.3454 -76.68239")
        print("or python query-2.py earthquakes magnitude 5 min 0 2000 -90.88 14.5")        
    else:     
            points=[]          
            adjusted_points=[]
            count=0   
            feature=sys.argv[1]
            field=sys.argv[2]
            if (field=='magnitude'): #converting the user given field to 'mag' feild
                field='mag'   
            field_range=float(sys.argv[3])    
            min_max=sys.argv[4]   
            values=int(sys.argv[5])   
            radius=float(sys.argv[6])    
            lon= float (sys.argv[7])    
            lat= float (sys.argv[8])    
            mh = mongoHelper()
            res=mh.get_nearest_feature(feature,field,field_range,min_max,values,radius,lon,lat)
            for r in res:
                count=count+1         
                every= float(r['properties'][field])         
                ln=r['geometry']['coordinates'][0]
                ln1=mh.mercX(ln,1)#converting to scren adjustable
                lt=r['geometry']['coordinates'][1]
                lt1=mh.mercY(lt,1)  
                tup=(ln,lt)
                tup1=(ln1,lt1)
                if (values!=0):
                    if((len(adjusted_points))==values):                
                        break
                points.append(tup)
                adjusted_points.append(tup1)
            #print(len(adjusted_points))
            #print(adjusted_points)            
            background_colour = (255,255,255)
            black = (0,0,0)
            (width, height) = (1024,512)
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(feature)
            screen.fill(background_colour)
            pygame.init()
            bg = pygame.image.load("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program5\\main.png")
            running = True
            pygame.time.wait(50)
            point=[]
            if feature=='volcanos':
                color=(255,0,0)
            elif feature=='earthquakes':
                color=(0,0,255)
            else: 
                color=(0,255,0)
            while running:                                        
                    screen.blit(bg, (0, 0))                               
                    for p in adjusted_points:                                                                                                               
                            point.append(p) #appending every point to the list point for displaying all the points
                    for o in point:                                                                                                                                   
                            pygame.draw.circle(screen,color,(int(o[1]),int(o[1])),2,0)                                                                       
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                clean_area(screen,(0,0),width,height,(255,255,255))    
                    running=False                      
            pygame.display.flip()
            pygame.image.save(screen,'C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program5\\Query2_'+feature+'_shot.png')

if __name__=='__main__':
    main()