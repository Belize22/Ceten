from ResourceBank import ResourceBank
from GamePieceBank import GamePieceBank


class Player:
    def __init__(self, id, name):
        self.id = id
        self.turn_priority = id
        self.name = name
        self.resource_bank = ResourceBank()
        self.game_piece_bank = GamePieceBank()

    def retrieve_victory_points(self):
        victory_points = 0
        victory_points += (
                self.game_piece_bank.STARTING_QUANTITIES[1]
                - self.game_piece_bank.game_pieces[1])
        victory_points += (
                self.game_piece_bank.STARTING_QUANTITIES[2]
                - self.game_piece_bank.game_pieces[2])*2
        return victory_points
    
    def retrieve_player_name(self):
        return str(self.name)



