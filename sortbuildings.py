#%%

from ast import literal_eval
import json

with open('data/log.log') as f:
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
        item_coords.append(x)
    else:
        if add == 'yes':
            height.append(x)
            add = 'no'
            coords.append(item_coords)
            item_coords = []
        else:
            min_height.append(x)
            add = 'yes'

features = []

for h, m, g, c in zip(height, min_height, geo_type, coords):
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": g,
            "coordinates": [c]
        },
        "properties": {
            "height": h,
            "min_height": m
        }
    }
    if feature not in features:
        features.append(feature)

feature_collection = {
    "type": "FeatureCollection",
    "features": features
}

with open(f'data/context.geojson', 'w') as f:
    json.dump(feature_collection, f)