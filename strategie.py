
from structs import *
from look import *
from actions import *
import ai
import path_finder


def strat(player, map):
    print("----- Strat -----")

    posRes = trouverPlusProche(player.Position, map, TileContent.Resource)
    print("-----ResPos-----")
    print (posRes)


    #if (DistanceEntre(player.HouseLocation, player.Position)+1) > DistanceEntre(trouverPlusProche(player.HouseLocation, map, 2), player.HouseLocation):
     #   return path_finder.move_to(map, player.Position, player.HouseLocation, player.Position)
    if DistanceEntre(player.Position, player.HouseLocation) == 1:
        if player.CarryingCapacity == 1000 and player.Score >= 15000:
            return create_upgrade_action(UpgradeType.CarryingCapacity)

    if player.CarriedRessources >= player.CarryingCapacity:
        return path_finder.move_to(map, player.Position, player.HouseLocation, player.Position)

    elif abs(DistanceEntre(player.Position, posRes)) == 1:
        return ai.create_collect_action(posRes)

    else:
        return path_finder.move_to(map, player.Position, posRes, player.Position)



def DistanceEntre(point1, point2):
    deltaX = abs(point1.X - point2.X)
    deltaY = abs(point1.Y - point2.Y)
    total = deltaX+deltaY
    print("---ToTal---")
    print(total)
    return total

