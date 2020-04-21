#%%

from ast import literal_eval
import geojson as gj
import json

with open('data/logv2.log') as f:
    content = f.readlines()

content = [x.strip() for x in content] 

content = [x[14:] for x in content]

content = [x[5:] if x[0] == '(' else x for x in content]

def retype(x):
    if x[0] == '[':
        x = literal_eval(x)
    else:
        try:
            x = float(x)
        except:
            x = str(x)
    return (x)

content = [retype(x) for x in content]

height = []
min_height = []
geo_type = []
coords = []


add = 'yes'
item_coords = []
for x in content:
    if isinstance(x, str):
        geo_type.append(x)
    elif isinstance(x, list):
        item_coords.append(tuple(x))
    else:
        if add == 'yes':
            height.append(int(x))
            add = 'no'
            coords.append(item_coords)
            item_coords = []
        else:
            min_height.append(int(x))
            add = 'yes'

features = []

for h, m, c in zip(height, min_height, coords):
    if len(c) >= 4:
        geom = gj.Polygon([c])
        feature = gj.Feature(geometry=geom, properties={"height": h, "min_height": m})
        if feature.errors() == None:
            features.append(feature)
            i += 1

feature_collection = gj.FeatureCollection(features)

with open(f'data/options/contextv2.geojson', 'w') as f:
    gj.dump(feature_collection, f)