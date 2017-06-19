"""
Program:
--------
    Program 2A - DBSCAN

Description:
------------
    This program reads the five cities crime .csv files as a input, take the lat,long postions in each line,
    scales the points and draw the points on the pygame window with different for each regions.
    
Name: Sowjanya Nemani
Date: 18 June 2017
"""

import pygame
import random
from dbscan import *
import sys,os
import pprint as pp
pygame.init()
import time 

"""
Screen Display information
"""
background_colour = (255,255,255)
(width, height) = (1000, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Program 2A')
screen.fill(background_colour)
color=(0,0,0)
pygame.display.flip()
DIRPATH = os.path.dirname(os.path.realpath(__file__))
"""
Taking files[] list to store the file names in order to iterate for every file
"""
files=['filtered_crimes_bronx.csv','filtered_crimes_brooklyn.csv','filtered_crimes_manhattan.csv','filtered_crimes_queens.csv','filtered_crimes_staten_island.csv']
"""
x_s and y_s are lists to hold the orginal latitudes and logitudes
new_x,new_y are the lists to hold the new latitude and logitude after scaling
"""
crimes = []
points=[]
x_s=[]
y_s=[]
new_x=[]
new_y=[]
got_keys = False

"""
for loop for taking the each file and processing and priting the points as per the colour given for every 
borough
"""
for name in files:  
  with open(DIRPATH+'/'+name) as f:   
    if(name=='filtered_crimes_bronx.csv'):
        color=(2,120,120)            
    elif(name=='filtered_crimes_brooklyn.csv'):
      color=(128,22,56)
    elif(name=='filtered_crimes_manhattan.csv'):
      color=(194,35,38)
    elif(name=='filtered_crimes_queens.csv'):
      color=(243,115,56)
    else:
      color=(253,182,50)
    """
    Crimes []  will store every line from the respective file and the crime[19] and crime [20]
    will have the latitute and longitues respectively
    x_s and y_s will have the original values of lats and longs
    new_x,new_y will havd the converted
     
    """  
    
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
           # print(keys)
            got_keys = True
            continue

        crimes.append(line)
    for crime in crimes:    
      if((crime[19]=='')or(crime[20]=='')or(len(crime)==0)):
        pass
      else:
        x = crime[19].strip()
        x= int(x)        
        #print(x)
        x_s.append(x) 
        y =  crime[20].strip()
        y_s.append(int(y))                 
#   max_x1 = max(x_s) 
#   max_y1 = max(y_s)
#   min_x1 = min(x_s)
#   min_y1 = min(y_s)
  max_x1 = 1067226 
  max_y1 = 271820
  min_x1 = 913357
  min_y1 = 121250
  for old_x in x_s:
     x_new=(old_x-min_x1)/(max_x1- min_x1)
     x_new=int (x_new*width)
     new_x.append(x_new)
#print( new_x)    
  for old_y in y_s:
     y_new=1-(old_y-min_y1)/(max_y1- min_y1)
     y_new=int (y_new*height)
     new_y.append(y_new)
#print(new_y)
  for i in range(max((len(new_x),len(new_y)))):
    xandy=(new_x[i],new_y[i])
    points.append(xandy)


  running = True
  while running:             
      for p in points:      
          pygame.draw.circle(screen, color, p, 3, 0)
      """
      clearing every list for new set of values
      """     
      crimes.clear()
      points.clear()
      x_s.clear()
      y_s.clear()
      new_x.clear()
      new_y.clear()
      keys.clear() 
      pygame.display.flip()         
      running = False        
pygame.image.save(screen,'C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Resources\\Dbscan_Ex\\all_buroughs_screen_shot.png')

    
