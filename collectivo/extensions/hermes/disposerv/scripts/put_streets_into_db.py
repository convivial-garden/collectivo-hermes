"""
class Street(models.Model):
    name = models.CharField(max_length=400, default='')
    name_street = models.CharField(max_length=400, default='')
    nr_von = models.CharField(max_length=10, null=True)
    nr_bis = models.CharField(max_length=10, null=True)
    postal_code = models.CharField(max_length=4)
    lat = models.FloatField(default=16)
    lon = models.FloatField(default=48
"""
from disposerv.models import Street
import json

with open("all_districts.json", "r") as inFile:
    streetData = json.load(inFile)

Street.objects.all().delete()
# print(json.dumps(streetData[0]["features"][0], indent=2))
plzs = set()
streetInstances = []
for featureCollection in streetData:
    for feature in featureCollection["features"]:
        prop, geometry = (feature["properties"], feature["geometry"])
        scrubbed = {
                'name': prop['NAME'],
                'name_street': prop['NAME_STR'],
                'nr_von' : prop['ONR_VON'],
                'nr_bis': prop['ONR_BIS'],
                'postal_code': prop['PLZ'],
                'lon': geometry['coordinates'][0],
                'lat': geometry['coordinates'][1]
        }
        plzs.add(prop["PLZ"])
        streetInstances.append(Street(**scrubbed))

Street.objects.bulk_create(streetInstances)