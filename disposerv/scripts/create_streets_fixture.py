import json

with open("all_districts.json", "r") as inFile:
    streetData = json.load(inFile)

# print(json.dumps(streetData[0]["features"][0], indent=2))
plzs = set()
streetFixture = []
index = 1
for featureCollection in streetData:
    for feature in featureCollection["features"]:
        prop, geometry = (feature["properties"], feature["geometry"])
        scrubbed =\
            {
                "model": "disposerv.Street",
                "pk": index,
                "fields": {
                    'name': prop['NAME'],
                    'name_street': prop['NAME_STR'],
                    'nr_von' : prop['ONR_VON'],
                    'nr_bis': prop['ONR_BIS'],
                    'postal_code': prop['PLZ'],
                    'lon': geometry['coordinates'][0],
                    'lat': geometry['coordinates'][1]
                }
            }
        streetFixture.append(scrubbed)
        index += 1

with open("streetsFixture.json", "w") as streetFixtureFile: 
    json.dump(streetFixture, streetFixtureFile)
