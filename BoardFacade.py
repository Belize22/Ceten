from Board import Board
from SubmitButton import SubmitButton
from TileFacade import TileFacade
from CornerFacade import CornerFacade
from NotificationPanel import NotificationPanel
import pygame
import math


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

    def __init__(self, screen, num_players):
        self.board = Board(num_players)
        self.screen = screen
        self.tile_facades = []
        self.corner_facades = []
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
        self.current_feedback = ""
        self.generate_facades()
        
    def generate_facades(self, size=42.5):
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

    def produce_resources(self, roll):
        self.board.produce_resources(roll)

    def render_control_menu(self):
        pygame.draw.rect(
            self.screen, (178, 155, 130),
            ((self.screen.get_width()*0.8, self.screen.get_height()*0.5),
             (self.screen.get_width()*0.2, self.screen.get_height()*0.5)), 0)
        self.roll_dice_button.draw()
        self.end_turn_button.draw()

    def roll_dice(self):
        roll = self.board.die_roller.roll_dice()
        pygame.draw.circle(
            self.screen, (228, 205, 180), self.dice_value_position, 30, 0)
        font = pygame.font.Font(None, 36)
        text = font.render(str(roll), 1, (10, 10, 10))
        self.screen.blit(
            text, [self.dice_value_position[0] - 11,
                   self.dice_value_position[1] - 8])
        self.board.change_game_phase()
        if roll != 7:
            self.board.change_game_phase()
            self.produce_resources(roll)

    def place_robber(self, mouse_pos):
        tile_facade = self.find_tile_at(mouse_pos)
        if int(tile_facade.tile.relational_id) < 19:
            robber_tile_facade = self.find_robber()
            if tile_facade == robber_tile_facade:
                self.current_feedback = \
                    "Cannot place robber on his current spot!"
            else:
                robber_tile_facade.set_robber(False)
                tile_facade.set_robber(True)
                self.current_feedback = ""
                self.board.change_game_phase()

    def build_component(self, mouse_pos, player_facade):
        cf = self.find_corner_at(mouse_pos)
        if cf is not None:
            self.place_settlement(cf, player_facade)

    def end_turn(self, player_facade):
        if player_facade.player.retrieve_victory_points() >= 3:
            self.board.change_phase()
        current_phase_before = self.board.get_current_phase()
        if current_phase_before == 3:
            self.end_turn_button.update("New Game")
            self.current_feedback = player_facade.player. \
               retrieve_player_name() + "has won Ceten."
        else:
            player = self.board.retrieve_current_player()
            self.board.change_current_player(player)
            player = self.board.retrieve_current_player()
            current_phase_after = self.board.get_current_phase()
            player_facade.set_next_player(player)
            if current_phase_before != 1:
                self.board.change_game_phase()
                self.current_feedback = ""
            else:
                if current_phase_after == 1:
                    self.current_feedback = player_facade.player.\
                        retrieve_player_name() + ", place a settlement."
                else:
                    self.current_feedback = ""

    # will always return at least one robber
    def find_robber(self):
        tile = self.board.find_robber()
        for tf in self.tile_facades:
            if tf.tile == tile:
                return tf

    def place_settlement(self, corner_facade, player_facade):
        feedback = self.board.place_settlement(
            corner_facade.corner, player_facade.player)
        self.current_feedback = feedback
        if feedback == "":
            corner_facade.update(player_facade.player)
            current_phase = self.board.get_current_phase()
            if current_phase == 1:
                self.end_turn(player_facade)

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

    def retrieve_players(self):
        return self.board.retrieve_players()

    def get_current_phases(self):
        return self.board.get_current_phase(), \
               self.board.get_current_game_phase()

    def update_phase_panel(self):
        current_phase = self.board.get_current_phase()
        current_game_phase = self.board.get_current_game_phase()
        message = ""
        if current_phase == 1:
            message = "Setup Phase"
        elif current_phase == 3:
            message = "Game Over!"
        else:
            if current_game_phase == 1:
                message = "Roll Dice"
            elif current_game_phase == 2:
                message = "Move the Robber to a new resource tile"
            elif current_game_phase == 3:
                message = "Build something from your Inventory"
        self.phase_panel.update(message)

    def update_feedback_panel(self):
        self.feedback_panel.update(self.current_feedback)

    def set_initial_feedback_message(self, player_facade):
        self.current_feedback = player_facade.player.retrieve_player_name() \
            + ", place a settlement."
        self.feedback_panel.update(self.current_feedback)

    def draw(self):
        self.phase_panel.draw()
        self.feedback_panel.draw()
        for tf in self.tile_facades:
            tf.draw()
        for cf in self.corner_facades:
            cf.draw()
