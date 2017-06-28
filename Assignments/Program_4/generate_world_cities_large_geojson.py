import pprint as pp
import os,sys
import json
import collections


f = open("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program_4\\Resources\\world_cities_large.json","r")

data = f.read()

data = json.loads(data)


all_airports = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''


for k,v in data.items():
    for obj in v:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = obj
        lat = obj['lat']
        lon = obj['lon']
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
              lon,
              lat
            ]
        all_airports.append(gj)

del all_airports[999:len(all_airports)-1] 
out = open("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program_4\\Resources\\world_cities_large.geojson","w")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()