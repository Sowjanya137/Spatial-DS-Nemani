"""
Program:
--------
    Program 5- query-3
Description:
------------
    This program takes the command line arguments as:
    python query3.py [feature] [min_pts] [eps]
    say:  python query3.py volcanos 10 5
    it fectched the latitude anad longitudes
    uses dbscan to get the clusters and forms the bounding rectangles
    the resultant clusters are ploted on pygame window with respective colors
Name: Sowjanya Nemani
Date: 5 July 2017
"""

from dbscan import *
import sys,os
from pymongo import MongoClient
import pprint as pp
from math import radians, cos, sin, asin, sqrt
import pygame
from map_helper import*
from nyc_file_helper import FileHelper
import json

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

    def calculate_mbrs(self,points, epsilon, min_pts,debug=False):
        """
        Find clusters using DBscan and then create a list of bounding rectangles
        to return.
        """
        mbrs = {}
        clusters =  dbscan(points, epsilon, min_pts,debug=debug)
        extremes = {'max_x':1067226,'max_y':271820,'min_x':913357,'min_y':121250}
        """
        Traditional dictionary iteration to populate mbr list
        Does same as below       """
       
        
        for id,cpoints in clusters.items():            
            xs = []
            ys = []
            for p in cpoints:               
                xs.append(p[0])
                ys.append(p[1])
            max_x = max(xs) 
            max_y = max(ys)
            min_x = min(xs)
            min_y = min(ys)

            if max_x > extremes['max_x']:
                extremes['max_x'] = max_x
            if max_y > extremes['max_y']:
                extremes['max_y'] = max_y
            if min_x < extremes['min_x']:
                extremes['min_x'] = min_x
            if min_y < extremes['min_y']:
                extremes['min_y'] = min_y
            mbrs[id]=[(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)]
        mbrs['extremes'] = extremes
        return mbrs

    def adjust_location_coords(self,mbr_data,width,height):
        """
        Adjust your point data to fit in the screen. 
        Expects a dictionary formatted like `mbrs_manhatten_fraud.json` with extremes in it.
        """
        maxx = float(mbr_data['extremes']['max_x']) # The max coords from bounding rectangles
        minx = float(mbr_data['extremes']['min_x'])
        maxy = float(mbr_data['extremes']['max_y'])
        miny = float(mbr_data['extremes']['min_y'])
        deltax = float(maxx) - float(minx)
        deltay = float(maxy) - float(miny)
        adjusted = {}

        del mbr_data['extremes']

        for id,mbr in mbr_data.items():
            adjusted[id] = []
            for p in mbr:
                x,y = p
                x = float(x)
                y = float(y)
                xprime = (x - minx) / deltax         # val (0,1)
                yprime = 1.0 - ((y - miny) / deltay) # val (0,1)
                adjx = int(xprime*width)
                adjy = int(yprime*height)
                adjusted[id].append((adjx,adjy))
        return adjusted
    """
    funtion to get the points from respective database
    """
    def pull_points(self,feature):
        if(feature=='volcanos'):
            res=self.db_volcanos.find();
        elif(feature=='earthquakes'):
            res=self.db_earthquakes.find();
        elif(feature=='meteorite'):
            res=self.db_meteorite.find(); 
        else:
            print("invalid feature or command line argvalue[1]")
            print("Please enter db names as: volcanos or earthquakes or meteorite")
            sys.exit(0)           
            
        points = []
        for r in res:
            p=[float(r['geometry']['coordinates'][0]),float(r['geometry']['coordinates'][1])] 
            if not p in points:
                points.append(p)
        #pp.pprint(points)        
        return points

def main():
    background_colour = (255,255,255)
    color = (255,0,0)
    (width, height) = (1024,512)
    screen = pygame.display.set_mode((width, height))
    bg = pygame.image.load("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program5\\main.png")
    pygame.display.set_caption('query-3')
    screen.fill(background_colour)
    pygame.display.flip()
    mh=mongoHelper()
    if  len(sys.argv)<4:
        print("Insuffucient arguments given")
        print("Please give commandline arguments as: query3.py [feature] [min_pts] [eps]")
    else: 
        feature=sys.argv[1]
        if(feature=='earthquakes'):
            color=(0,0,255)
        min_pts=int (sys.argv[2])
        eps= int (sys.argv[3])              
        points=mh.pull_points(feature)
        #pp.pprint(points)  
        ## Find the clusters from our NYC data file        
    mbrs = mh.calculate_mbrs(points,min_pts,eps,debug=True)
    # Remove the cluster that contains all the points NOT in a cluster
    del mbrs[-1]
    print("-----------------------------------------------------------------------------------")
    #pp.pprint(mbrs)
    mbrs1 = mh.adjust_location_coords(mbrs,width,height)
    #print(mbrs1)
    running = True
    while running:
        screen.blit(bg, (0, 0))
        for id,mbr in mbrs.items():            
            pygame.draw.polygon(screen,color, mbr, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clean_area(screen,(0,0),width,height,(255,255,255))
                points.append(event.pos)
                mbrs = calculate_mbrs(points, epsilon, min_pts)
        pygame.display.flip()
        pygame.image.save(screen,'C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program5\\Query3_'+feature+'_output.png')
if __name__=='__main__':
    main()