"""Programa para carregar todos os json do tiled para um arquivo do jogo"""

import os
import json

def fix_pos(pos):
    """Retorna a coordenada invertida (y, x) e com divisão inteira por 64"""
    return [pos["y"] // 64, (pos["x"] // 64)]

with open('empty.json') as f:
    game = json.load(f)

game["levels"] = []

level_count = 0
for name in os.listdir('./tiled'):
    if name.endswith('.json'):
        level_count += 1
        with open('./tiled/' + name) as f:
            data = json.load(f)
        level = {
            "music": "./sound/music.wav",
            "colors": {
                "floor": [0, 0, 80 // level_count],
                "ceil": [0, 100 // level_count, 0],
                "dark": level_count % 5 == 0
            },
            "map": [],
            "enemies": [],
            "items": [],
            "player": []
        }
        for i in range(data["height"]):
            level["map"].append([])
            for j in range(data["width"]):
                level["map"][i].append(data["layers"][0]["data"][i * data["width"] + j])
        for entity in data["layers"][1]["objects"]:
            if entity["name"] in ("enemy", "boss"):
                level["enemies"].append([entity["name"], fix_pos(entity)])
            elif entity["name"] in ("health", "ammo"):
                level["items"].append([entity["name"], fix_pos(entity)])
            elif entity["name"] == "player":
                level["player"] = fix_pos(entity)
        game["levels"].append(level)

with open('game.json', 'w') as outfile:
    json.dump(game, outfile, indent=4)
