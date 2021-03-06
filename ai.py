from flask import Flask, request
from structs import *
import json
import numpy

from actions import *
import visualize_round
import strategie

app = Flask(__name__)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(20)] for y in range(20)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)

    return deserialized_map

def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]), p["Score"],
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map = deserialize_map(serialized_map)

    otherPlayers = []

    for players in map_json["OtherPlayers"]:
        player_info = players["Value"]
        p_pos = player_info["Position"]
        player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

        otherPlayers.append(player_info)

    #visualize_round.show(otherPlayers, serialized_map, deserialized_map)


    # return decision
    print("=== Map ===")
    print " ",
    for i in range(20):
        print ((i+player.Position.X) % 10),
    print
    for j in range(20):
        print ((j+player.Position.Y) % 10),
        for i in range(20):
            if deserialized_map[i][j].Content == TileContent.Empty:
                print " ",
            elif deserialized_map[i][j].Content == TileContent.Wall:
                print "#",
            elif deserialized_map[i][j].Content == TileContent.House:
                print "^",
            elif deserialized_map[i][j].Content == TileContent.Lava:
                print "o",
            elif deserialized_map[i][j].Content == TileContent.Resource:
                print "~",
            elif deserialized_map[i][j].Content == TileContent.Shop:
                print "$",
            elif deserialized_map[i][j].Content == TileContent.Player:
                print "x",
            else:
                print "?",
        print
    print("=== Player ===")
    print("Score: "+str(player.Score))
    print("Position: " + str(player.Position))
    print("Health: " + str(player.Health) + "/" + str(player.MaxHealth))
    print("Ressources: " + str(player.CarriedRessources) + "/" + str(player.CarryingCapacity))
    a = strategie.strat(player, deserialized_map)
    return a

@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    res_value = bot()
    return res_value

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
