
from structs import *


def show(player_dict, serialized_map, deserialized_map):
    print("--- Current Player ---")
    #print(player_dict)

    lst_round = []
    for lst in deserialized_map:
        for item in lst:
            if(item.X != 0 and item.Y !=0 and item.Content!=None):
                #print(item.X, item.Y, item.Content)
                if(item.Content ==2):
                    lst_round.append([item.X, item.Y, item.Content])

    #if(len(item)==0):
    #    print("No Player found around")
    for item in lst_round:
        print item


    #print("--- Other Player ---")



