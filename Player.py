from ResourceBank import ResourceBank
from GamePieceBank import GamePieceBank


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.resource_bank = ResourceBank()
        self.game_piece_bank = GamePieceBank()
        self.dev_cards = []
            
    def str(self):
        ret = self.name_str() + "\n"
        for s in self.res_str_list():
            ret += s + "\n"
        for s in self.piece_str_list():
            ret += s + "\n"
        return ret
    
    def name_str(self):
        return str(self.name)
    
    def res_str_list(self):
        resource_info = ["Lumber: ", "Wool: ", "Grain: ", "Brick: ",
                         "Ore: "]
        for i in range(len(self.resource_bank.resources)):
            resource_info[i] += str(self.resource_bank.resources[i])
        return resource_info

    def piece_str_list(self):
        return ["Settlements: " + str(self.game_piece_bank.settlements),
                "Cities: " + str(self.game_piece_bank.cities),
                "Roads: " + str(self.game_piece_bank.roads)]



