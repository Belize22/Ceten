from ResourceBank import ResourceBank
from GamePieceBank import GamePieceBank


class Player:
    def __init__(self, id, name):
        self.id = id
        self.turn_priority = id
        self.name = name
        self.resource_bank = ResourceBank()
        self.game_piece_bank = GamePieceBank()
        self.dev_cards = []

    def retrieve_victory_points(self):
        victory_points = 0
        victory_points += (5-self.game_piece_bank.game_pieces[1])
        victory_points += (4-self.game_piece_bank.game_pieces[2])*2
        return victory_points
            
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
        resource_info = ["Roads: ", "Settlements: ", "Cities: "]
        for i in range(len(self.game_piece_bank.game_pieces)):
            resource_info[i] += str(self.game_piece_bank.game_pieces[i])
        return resource_info



