The path to store the screen shots has to be modified
and the path to background image has to be modified.

query-1 needs to be executed as follows file name source_airportcode destination_airportcode radius:
example: python query1.py DFW MNL 500
helper files 
1024x512.png
map_helper.py

query-2 needs to be executed as follows:
python query2.py volcanos altitude 3000 min 3 1000
or
python query2.py earthquakes magnitude 5 min 0 200
or
python query2.py meteorite year 2010 min 0 2000
helper files 
1024x512.png
map_helper.py

query-3 takes the command line arguments as:
    python query3.py [feature] [min_pts] [eps]
    say:  python query3.py volcanos 10 5  (works good)
    helper files 
    1024x512.png
    db_scan.py
    map_helper.py
