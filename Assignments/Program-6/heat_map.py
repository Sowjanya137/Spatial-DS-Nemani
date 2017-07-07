"""
Program:
--------
    Program 6 - HeatMaps.
Description:
------------
    This program takes the global atacks data from the attacks.json
    and to create the heatmaps based on the intensity of attacks.
    
Name: Sowjanya Nemani
Date: 7 July 2017
"""

import operator
import json
import sys
import pprint as pp
from mercator_py import *
import math
from Color_Mapping import*
import pygame
import time
EPSILON = sys.float_info.epsilon


"""
This block of code is for reading the data from file and collecting into data 
and creats it into Lat_lon list-the tupeles of all lat longs
This code also creates a grid of 512(height) columns 
and 1024 rows(width)
lat_lon-list of tuples of latitudes anad longitudes
"""

def main():    
    lon_lat=[]
    height=512
    width=1024    
    get_colors1={}
    adjusted=[]  
    f=open('C:\\data\\attacks\\attacks.json','r')
    count=[]
    data=f.read()
    data=json.loads(data)
    grid=[]
    for i in range(512):
        grid.append([0 for x in range(1024)])    
    for i in range(height):
        for j in range(width): 
            grid[i][j]=0
    for country,coun_places in data.items():              
                for place,geometry in coun_places.items():
                        tup=()
                        tup=tup+(geometry['geometry']['coordinates'][0],)
                        tup=tup+(geometry['geometry']['coordinates'][1],)
                        #print(tup)
                        lon_lat.append(tup)
    #pp.pprint(lon_lat)#check point for list of lat,longs
    #===========================================================
    """
    This block of code takes the every point from lat_lon list and adjusts
    it to screen locations for display
    It uses method adjust_point from the file mercator_py and creates a list adjusted
    """
    for p in lon_lat:
        x,y=adjust_point(p,width,height)
        p=x,y
        adjusted.append(p)
    #pp.pprint(adjusted)
    """
    The code below gets the each tuple from the adjusted list and takes it as integer to 
    assign in the corresponding row and column of grid value as 1
    Say x=868 y=242
    grid[868][242]=1
    max vaiable contains the maximum value
    count list contains the sequence of non zero values in every cell of grid
    """
    for p in adjusted:
        x=int(p[1])      
        y=int(p[0])      
        grid[x][y]=grid[x][y]+1
    max=1#this 
    for i in range(height):
            for j in range(width):   
                if(grid[i][j]>0):
                    if(grid[i][j]>=max):
                        max=grid[i][j]   
                        #print(max,end=' ')
                        if max in count:
                            pass
                        else:
                            count.append(max)

    """
    Min_count and max_count will contain the maximum value and minimum vales of 
    number of attacks from the count list which are taken from corresponding grid index
    function: get_colors(min_count,max_count) is taken from the Color_Mapping file
    and variables min_count aand max_count are passed to get colors the step size 
    inside the fucntion is taken as 31 constant value.
    Args:Min_count and max_count
    returns: dictionary with keys as count of attacks and values as corresponding
    r,g,b tuple
    This dictionary is used to pick the color asa per the value of grid
    to draw circle
    """
    #print(count)
    min_count=count[0]
    max_count=count[-1]
    #print(min_count,max_count)
    get_colors1=get_colors(min_count,max_count)
    #print(get_colors1)
    """
    The code below sets the attributes for screen window 
    for the display and uses a background map.png image.

    It runs a while loop for the plotting the circles of 
    lat, longs taking the indices of grid as j and i

    It picks the color as per the value in the index poisition
    Say grid[i][j]=1, the corresponding color is picked from the
    dictionary get_colors1   
    """
    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024,512)
    screen = pygame.display.set_mode((1024,512))
    pygame.display.set_caption('heat_map')
    screen.fill(background_colour) 
    pygame.init()
    bg = pygame.image.load("map.png")
    running = True
    point1=[]
    pygame.time.wait(50)
    while running:            
        screen.blit(bg, (0, 0))                               
        for i in range(height):
            for j in range(width):                                 
                    if(grid[i][j]>0):                        
                            radius=grid[i][j]
                            for k,v in get_colors1.items():
                                if k==grid[i][j]:
                                    color1=v
                                    width1=1
                                    # if radius>50:
                                    #     width1=2                                                         
                                    pygame.draw.circle(screen,color1,(j,i),radius,width1)                      
        for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            clean_area(screen,(0,0),width,height,(255,255,255))  
        pygame.display.flip()
    pygame.image.save(screen,'C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\10-Program-6\\heat_map.png')                    
if __name__=='__main__':
    main()
                    
           