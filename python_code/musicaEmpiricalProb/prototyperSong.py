# Crea i protitipi per le singole canzoni

import json
from Song import Song

with open('data.txt') as json_file:
    data = json.load(json_file)
    for s in data['songs']:
        song = Song(str(s["title"]).replace('"', "").replace('/', '_').replace('?', '').replace(':', ''),
                    str(s["performer"]).replace('"', "").replace('/', '_').replace('?', '').replace(':', ''),
                    s["genre"], s["attributes"])
        song.toPercent()
