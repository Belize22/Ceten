from Board import Board
from Tile import Tile
from DieRoller import DieRoller
from SubmitButton import SubmitButton
from TileFacade import TileFacade
from CornerFacade import CornerFacade
from NotificationPanel import NotificationPanel
import pygame
import math
import random


class BoardFacade:
    NUM_DICE = 2
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
        self.die_roller = DieRoller(self.NUM_DICE)
        self.roll_dice_button = SubmitButton(
            self.screen, (int(self.screen.get_width()*0.9), 275), "Roll Dice")
        self.end_turn_button = SubmitButton(
            self.screen, (int(self.screen.get_width()*0.9), 425), "End Turn")
        self.dice_value_position = (int(self.screen.get_width()*0.9), 275 + 60)
        self.phase_panel = NotificationPanel(
            (self.screen.get_width() * 0.5, 0), self.screen)
        self.feedback_panel = NotificationPanel(
            (self.screen.get_width() * 0.5, self.screen.get_height() * 0.95),
            self.screen)
        self.generate_facades()
        
    def generate_facades(self, start=[400.0, 290.0], size=42.5):
        self.generate_tile_facades(size)
        self.generate_corner_facades(size/5)

    def generate_tile_facades(self, size):
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
                current_direction = -1
            s = -q - r
            tile_facade = TileFacade(
                current_tile, self.screen,
                [self.screen.get_width()*0.5+s * size
                 * math.sqrt(3.0)+offset_x,
                 self.screen.get_height()*0.5+1.5 * q * size+offset_y], size,
                 current_direction)
            print(tile_facade.str())
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

    def generate_corner_facades(self, radius):
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
                corner_facade = CornerFacade(
                    [round(center_x), round(center_y)], c, self.screen, radius)
                insert_facade = True
                for cf in self.corner_facades:
                    if cf.center == corner_facade.center:
                        insert_facade = False
                        break
                if insert_facade:
                    self.corner_facades.append(corner_facade)

    def produce_initial_resources(self, corner, player):
        self.board.produce_initial_resources(corner, player)

    def produce_resources(self, roll, players):
        self.board.produce_resources(roll, players)

    def render_control_menu(self):
        pygame.draw.rect(
            self.screen, (178, 155, 130),
            ((self.screen.get_width()*0.8, self.screen.get_height()*0.5),
             (self.screen.get_width()*0.2, self.screen.get_height()*0.5)), 0)
        self.roll_dice_button.draw()
        self.end_turn_button.draw()

    def roll_dice(self):
        roll = self.die_roller.roll_dice()
        pygame.draw.circle(
            self.screen, (228, 205, 180), self.dice_value_position, 30, 0)
        font = pygame.font.Font(None, 36)
        text = font.render(str(roll), 1, (10, 10, 10))
        self.screen.blit(
            text, [self.dice_value_position[0] - 11,
                   self.dice_value_position[1] - 8])
        print("Current Roll " + str(roll))
        if roll == 7:
            self.board.active_robber = True
        return roll

    # will always return at least one robber
    def find_robber(self):
        tile = self.board.find_robber()
        print("Robber Found! " + tile.str())
        for tf in self.tile_facades:
            if tf.tile == tile:
                print("Robber Facade Found! " + str(tf))
                return tf

    def place_settlement(self, corner_facade, player_facade):
        if corner_facade.corner.does_corner_belong_to_a_player(
                player_facade.player.id):
            if not corner_facade.corner.are_neighboring_corners_settled():
                if corner_facade.corner.settlement == "none":
                    if player_facade.player.game_piece_bank.game_pieces[1] > 0:
                        player_facade.player.resource_bank.spend_resources(
                            [1, 1, 1, 1, 0])
                        self.board.resource_bank.collect_resources(
                            [1, 1, 1, 1, 0])
                        transaction_valid = player_facade.player\
                            .resource_bank.validate_transaction()
                        if transaction_valid:
                            self.board.resource_bank.validate_transaction()
                            corner_facade.update(player_facade.player)
                            player_facade.player.game_piece_bank\
                                .place_settlement()
                        else:
                            self.feedback_panel.update(
                                "Insufficient resources to build a settlement!"
                            )
                    else:
                        self.feedback_panel.update(
                            "No more settlements in your inventory!")
                elif corner_facade.corner.settlement == "settlement":
                    if player_facade.player.game_piece_bank.game_pieces[2] > 0:
                        player_facade.player.resource_bank.spend_resources(
                            [0, 0, 2, 0, 3])
                        self.board.resource_bank.collect_resources(
                            [0, 0, 2, 0, 3])
                        transaction_valid = player_facade.player.\
                            resource_bank.validate_transaction()
                        if transaction_valid:
                            self.board.resource_bank.validate_transaction()
                            corner_facade.update(player_facade.player)
                            player_facade.player.game_piece_bank.place_city()
                        else:
                            self.feedback_panel.update(
                                "Insufficient resources to build a city!")
                    else:
                        self.feedback_panel.update(
                            "No more cities in your inventory!")
                else:
                    self.feedback_panel.update(
                        "Cities cannot be upgraded further!")
            else:
                self.feedback_panel.update(
                    "Neighboring corners have settlements!")
        else:
            self.feedback_panel.update("You don't own this "
                                       + corner_facade.corner.settlement + "!")

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
        self.phase_panel.draw()
        self.feedback_panel.draw()
        for tf in self.tile_facades:
            tf.draw()
        for cf in self.corner_facades:
            cf.draw()
