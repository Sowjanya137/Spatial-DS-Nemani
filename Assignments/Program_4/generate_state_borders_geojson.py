import pprint as pp
import os,sys
import json
import collections


f = open("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program_4\\Resources\\state_borders.json","r")

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


for k in data:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = k
        borders = k['borders']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Polygon"
        gj["geometry"]["coordinates"] = borders
        del gj['properties']['borders']
        all_airports.append(gj)
#pp.pprint(all_airports)
del all_airports[999:len(all_airports)-1] 
out = open("C:\\Users\\sowja\\Documents\\SPDS\\Class\\4553-Spatial-DS\\Assignments\\Program_4\\Resources\\state_borders.geojson","w")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()