"""
Program:
--------
    Program 3- DBscan - Earthquake Data
Description:
------------
    This program reads the quake-1960-adjusted.json file of every yeasr as a input, take the lat,long postions in each line,
    in the list points and draw the points on the pygame window.
    
Name: Sowjanya Nemani
Date: 18 June 2017
"""

import pygame
import sys,os
import json
import time
import random

def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)
years = [x for x in range(1960,2017)]
if __name__=='__main__':    
    background_colour = (255,255,255)
    black = (0,0,0)
    (width, height) = (1024,512)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MBRs')
    screen.fill(background_colour)
    pygame.display.flip()
    point=[]
    colors=[(0,0,250),(250,0,0),(0,250,0),(255,255,255)]
    i=0
    """
    Runnung the loop for all the years
    """
    for y in years:
        f = open('quake-'+str(y)+'-adjusted.json','r')
        points = json.loads(f.read())
        pygame.init()
        bg = pygame.image.load("map.png")
        running = True
        pygame.time.wait(50)
        while running:            
            screen.blit(bg, (0, 0))                               
            for p in points:                                                                                            
                    point.append(p) #appending every point to the list point for displaying all the points                                         
            for o in point:                                                                
                    pygame.draw.circle(screen,(0,255,0), o, 1,0)                                                                       
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clean_area(screen,(0,0),width,height,(255,255,255))    
            running=False                      
            pygame.display.flip()
    pygame.image.save(screen,'C:\\Users\\sowja\\Documents\\SPDS\\all_quakes_screen_shot.png')
           
