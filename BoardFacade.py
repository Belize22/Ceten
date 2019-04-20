from Board import Board
from Tile import Tile
from TileFacade import TileFacade
from CornerFacade import CornerFacade
import pygame
import math
import random


class BoardFacade:
    grid_coordinates = [
        (0, -3),
        (-1, -2),
        (-2, -1),
        (-3, 0),
        (1, -3),
        (0, -2),
        (-1, -1),
        (-2, 0),
        (-3, 1),
        (2, -3),
        (1, -2),
        (0, -1),
        (-1, 0),
        (-2, 1),
        (-3, 2),
        (3, -3),
        (2, -2),
        (1, -1),
        (0, 0),
        (-1, 1),
        (-2, 2),
        (-3, 3),
        (3, -2),
        (2, -1),
        (1, 0),
        (0, 1),
        (-1, 2),
        (-2, 3),
        (3, -1),
        (2, 0),
        (1, 1),
        (0, 2),
        (-1, 3),
        (3, 0),
        (2, 1),
        (1, 2),
        (0, 3)
    ]

    def __init__(self, board, screen):
        self.board = board
        self.screen = screen
        self.tile_facades = []
        self.corner_facades = []
        self.generate_facades()
        
    def generate_facades(self, start=[400.0, 290.0], size=40.0):
        tile_count = 0
        offset_y = 0
        offset_x = 0
        tiles = self.board.get_tiles_ordered_by_physical_id()
        for q, r in BoardFacade.grid_coordinates:
            current_tile = tiles.pop(0)
            if (int(current_tile.relational_id) > 18
               and int(current_tile.relational_id) % 2 == 0):
                if int(current_tile.relational_id) > 18:
                    current_direction = 0
                if int(current_tile.relational_id) > 22:
                    current_direction = 1
                if int(current_tile.relational_id) > 24:
                    current_direction = 2
                if int(current_tile.relational_id) > 28:
                    current_direction = 3
                if int(current_tile.relational_id) > 30:
                    current_direction = 4
                if int(current_tile.relational_id) > 34:
                    current_direction = 5
            else:
                tile_direction = -1
            s = -q - r
            tile_facade = TileFacade(current_tile, 
                                     self.screen, 
                                     [self.screen.get_width()*0.5+s * size
                                      * math.sqrt(3.0)+offset_x, 
                                      self.screen.get_height()*0.5+1.5 * q * size+offset_y],
                                     size,
                                     current_direction)
            print (tile_facade.str())
            index = 0
            for tf in self.tile_facades:
                if (int(tf.tile.relational_id) < 
                   int(tile_facade.tile.relational_id)):
                    index += 1
                else:
                    break
            self.tile_facades.insert(index, tile_facade)
            tile_count += 1
            # be careful tinkering with this code, it is tempermental
            if tile_count == 4:
                offset_x = size * 0.87
            elif tile_count == 9:
                offset_x = size * 1.72
            elif tile_count == 15:
                offset_x = size * 2.6
            elif tile_count == 22:
                offset_x = size * 2.6
            elif tile_count == 28:
                offset_x = size * 2.6
            elif tile_count == 33:
                offset_x = size * 2.6
            else:
                offset_x -= size * math.sqrt(3.0)/2.0
        corners_of_tile = []
        for tf in self.tile_facades:
            for e in tf.tile.edges:
                for c in e.corners:
                    if c not in corners_of_tile:
                        corners_of_tile.append(c)
            for c in corners_of_tile:
                tiles_of_corner = []
                for e in c.edges:
                    for t in e.tiles:
                        if t not in tiles_of_corner:
                            tiles_of_corner.append(t)
                tile_facade_reference_points = []
                for t in tiles_of_corner:
                    for tf in self.tile_facades:
                        if tf.tile == t:
                            tile_facade_reference_points.append(tf)
                center_x = 0
                center_y = 0
                for tfrp in tile_facade_reference_points:
                    center_x += tfrp.centre[0]/3
                    center_y += tfrp.centre[1]/3
                corner_facade = CornerFacade([round(center_x),
                                              round(center_y)],
                                             c, self.screen)			
                insert_facade = True
                for cf in self.corner_facades:
                    if cf.center == corner_facade.center:
                        insert_facade = False
                        break
                if insert_facade:
                    self.corner_facades.append(corner_facade)

    def produce_resources(self, roll):
        return self.board.produce_resources(roll)

    # will always return at least one robber
    def find_robber(self):
        tile = self.board.find_robber()
        print("Robber Found! " + tile.str())
        for tf in self.tile_facades:
            if tf.tile == tile:
                print("Robber Facade Found! " + str(tf))
                return tf

    def place_settlement(self, corner_facade, player_facade):
        if corner_facade.corner.can_settlement_be_placed(player_facade.player.id):
            if corner_facade.corner.settlement == "none":
                if player_facade.player.game_piece_bank.game_pieces[1] > 0:
                    player_facade.player.resource_bank.spend_resources([1, 1, 1, 1, 0])
                    self.board.resource_bank.collect_resources([1, 1, 1, 1, 0])
                    transaction_valid = player_facade.player.resource_bank.validate_transaction()
                    if transaction_valid:
                        self.board.resource_bank.validate_transaction()
                        corner_facade.update(player_facade.player)
                        player_facade.player.game_piece_bank.place_settlement()
                    else:
                        print("Insufficient resources to build a settlement!")
                else:
                    print("You have no more settlements in your inventory!")
            elif corner_facade.corner.settlement == "settlement":
                if player_facade.player.game_piece_bank.game_pieces[2] > 0:
                    player_facade.player.resource_bank.spend_resources([0, 0, 2, 0, 3])
                    self.board.resource_bank.collect_resources([0, 0, 2, 0, 3])
                    transaction_valid = player_facade.player.resource_bank.validate_transaction()
                    if transaction_valid:
                        self.board.resource_bank.validate_transaction()
                        corner_facade.update(player_facade.player)
                        player_facade.player.game_piece_bank.place_city()
                    else:
                        print("Insufficient resources to build a city!")
                else:
                    print("You have no more cities in your inventory!")
            else:
                print("Cities cannot be upgraded further!")

    def find_tile_at(self, pos):
        for tf in self.tile_facades:
            if tf.rect.collidepoint(pos):
                return tf

    def find_corner_at(self, pos):
        for cf in self.corner_facades:
            if cf.circle.collidepoint(pos):
                return cf

    def in_boundaries(self, pos):
        if self.find_tile_at(pos) is not None:
            return True
        return False	

    def draw(self):
        for tf in self.tile_facades:
            tf.draw()
        for cf in self.corner_facades:
            cf.draw()
