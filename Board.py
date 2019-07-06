from Tile import Tile
from Edge import Edge
from Corner import Corner
from Player import Player
from DieRoller import DieRoller
from ResourceBank import ResourceBank

import random
import re


class Board:
    NUM_DICE = 2

    resources = {
        "ore": 3,
        "desert": 1,
        "brick": 3,
        "wool": 4,
        "grain": 4,
        "lumber": 4,
    }
    activation_values = {
        "2": 1,
        "3": 2,
        "4": 2,
        "5": 2,
        "6": 2,
        "8": 2,
        "9": 2,
        "10": 2,
        "11": 2,
        "12": 1,
    }
    relational_to_physical_id_mapping = [
        "30", "29", "28", "27",
        "31", "14", "13", "12", "26",
        "32", "15", "4", "3", "11", "25",
        "33", "16", "5", "0", "2", "10", "24",
        "34", "17", "6", "1", "9", "23",
        "35", "18", "7", "8", "22",
        "36", "19", "20", "21"
    ]

    def __init__(self, num_players):
        self.tiles = []
        self.players = []
        self.current_player = None
        self.resource_bank = ResourceBank(19)
        self.die_roller = DieRoller(self.NUM_DICE)
        self.current_phase = 1
        self.current_game_phase = 1
        self.reverse_turn_order = False
        current_resources = Board.resources.copy()
        for i in range(1, num_players + 1):
            self.players.append(
                    Player(i, "Player" + str(i)))
        self.randomize_turn_order()
        while len(current_resources) > 0:
            (resource, resource_count) = random.choice(
                list(current_resources.items()))
            if resource_count < 1:
                current_resources.pop(resource)
                continue
            if resource == "desert":
                tile = Tile(resource, 0)
                tile.robber = True
                self.tiles.append(tile)
                current_resources[resource] -= 1
                continue
            self.tiles.append(Tile(resource, 0))
            current_resources[resource] -= 1
        port_types = ["grain", "ore", "standard", "wool", "standard",
                      "standard", "brick", "lumber", "standard"]
        for i in range(19, 37):
            if i % 2 == 0:
                t = Tile(port_types.pop(
                          random.randint(0, len(port_types)-1))
                         + "_port", 0)
            else:
                t = Tile("water", 0)
            self.tiles.append(t)
        self.connect_board()
        self.place_tokens()
        self.start_off_with_extra_resources(self.players)
                
    def connect_board(self):
        num_circles = 2
        total_tile_quantity = get_product_sum(num_circles)
        val = 1
        level = 1
        self.tiles[0].relational_id = str(0)
        while level <= num_circles + 1:
            level_tile_quantity = get_product_sum(level)
            nth_tile_being_iterated = 1
            if level == 1:           # Middle Level
                while nth_tile_being_iterated < 6*level + 1:
                    self.tiles[val].relational_id = str(val)
                    second_corner = Corner()
                    third_corner = Corner()
                    if nth_tile_being_iterated == 1:
                        first_corner = Corner()
                        final_corner = first_corner
                    set_edges(
                        [self.tiles[val], self.tiles[val-1]],
                        [first_corner, second_corner])
                    if nth_tile_being_iterated == 6*level:
                        third_corner = final_corner
                    if nth_tile_being_iterated > 1:
                        set_edges(
                            [self.tiles[val], self.tiles[0]],
                            [first_corner, third_corner])
                    if nth_tile_being_iterated == 6*level:
                        bridge_corner = Corner()
                        set_edges(
                            [self.tiles[val], self.tiles[1]],
                            [third_corner, bridge_corner])
                    if nth_tile_being_iterated == 1:
                        first_corner = second_corner
                    else:
                        first_corner = third_corner
                    nth_tile_being_iterated += 1
                    val += 1
                level += 1
            elif level == 2:                       # Outer Level
                first_corner = bridge_corner
                adjacent_tile_of_previous_level = val - 6*(level-1)
                tiles_on_current_level_iterated = 0
                while nth_tile_being_iterated < 6*level+1:
                    self.tiles[val].relational_id = str(val)
                    second_corner = Corner()
                    third_corner = Corner()
                    set_edges(
                        [self.tiles[val], self.tiles[val-1]],
                        [first_corner, second_corner])
                    if val == 18:
                        third_corner = final_corner
                    if val > 7 and nth_tile_being_iterated % 2 == 1:
                        corners_of_edges = []
                        for e in self.tiles[
                                 adjacent_tile_of_previous_level].edges:
                            for c in e.corners:
                                if (self.tiles[
                                    adjacent_tile_of_previous_level]
                                    .num_edges_connected_to_corner(c) == 1
                                        and c != first_corner):
                                    third_corner = c
                    set_edges(
                        [self.tiles[val],
                         self.tiles[adjacent_tile_of_previous_level]],
                        [first_corner, third_corner])
                    if val == 7:
                        final_corner = second_corner
                    if val == 12:
                        second_corner = final_corner
                    if val > 7 and nth_tile_being_iterated % 2 == 1:
                        fourth_corner = Corner()
                        adjacent_tile_of_previous_level += 1
                        set_edges(
                            [self.tiles[val], self.tiles[
                             adjacent_tile_of_previous_level]],
                            [third_corner, fourth_corner])
                        first_corner = fourth_corner
                    else:
                        first_corner = third_corner
                    if nth_tile_being_iterated == 6*level:
                        fourth_corner = Corner()
                        set_edges(
                            [self.tiles[val], self.tiles[val - 6*level + 1]],
                            [third_corner, fourth_corner])
                        if val == 18:
                            bridge_corner = fourth_corner                  
                    lone_edges_to_generate = 3 - (nth_tile_being_iterated % 2)
                    nth_tile_being_iterated += 1
                    val += 1
                level += 1
            else:
                nth_tile_being_iterated = 7
                first_corner = bridge_corner
                while nth_tile_being_iterated < total_tile_quantity:
                    second_corner = Corner()
                    self.tiles[val].relational_id = str(val)
                    set_edges(
                        [self.tiles[nth_tile_being_iterated],
                         self.tiles[val]],
                        [first_corner, second_corner])
                    val += 1
                    if nth_tile_being_iterated % 2 == 1:
                        second_to_last_corner = second_corner
                    else:
                        third_corner = Corner()
                        self.tiles[val].relational_id = str(val)
                        set_edges(
                            [self.tiles[nth_tile_being_iterated],
                             self.tiles[val]],
                            [second_corner, third_corner])
                        second_to_last_corner = third_corner
                        val += 1
                    if nth_tile_being_iterated == 18:
                        next_index = 7
                        val = 19
                        last_corner = bridge_corner
                    else:
                        next_index = nth_tile_being_iterated+1                        
                        for e in self.tiles[next_index].edges:
                            for c in e.corners:
                                has_current_tile = re.search(
                                    "([0-9]+-" + str(nth_tile_being_iterated)
                                    + ")|(" + str(nth_tile_being_iterated)
                                    + "[0-9]+)", e.relational_id)
                                if has_current_tile:
                                    two_corners_only = re.search(
                                        "(^[0-9]+-"
                                        + str(nth_tile_being_iterated)
                                        + "$)|(^"
                                        + str(nth_tile_being_iterated)
                                        + "[0-9]+)$", c.relational_id)
                                    if two_corners_only:
                                        last_corner = c 
                    self.tiles[val].relational_id = str(val)           
                    set_edges([self.tiles[nth_tile_being_iterated],
                               self.tiles[val]],
                                  [second_to_last_corner, last_corner])
                    first_corner = last_corner
                    nth_tile_being_iterated += 1
                level += 1
        for t in self.tiles:
            if t.relational_id != '' and int(t.relational_id) < 19:
                t.physical_id = self.relational_to_physical_id_mapping[
                                int(t.relational_id)]


    """place_tokens:
    Places tokens on land tiles. These tokens have an activation value
    that represents the total dice value required for the tile to give
    the adjacent settlements and cities resources. This algorithm was 
    designed so that tokens with values 6 and 8 are not adjacent to 
    each other.
    """
    def place_tokens(self):
        active_activation_values = self.activation_values.copy()
        tiles_to_place_tokens_on = []
        rejected_tiles_for_reds = []      # 6's and 8's referred to as reds.
        # Only land tiles get tokens on them.
        for t in self.tiles:
            if ("water" not in t.resource and "port" not in t.resource
                    and "desert" not in t.resource):
                tiles_to_place_tokens_on.append(t.relational_id)
        # Place 6's first, then 8's after.
        while (active_activation_values.get("6") > 0
                or active_activation_values.get("8")) > 0:
            token_value = "6"
            if active_activation_values.get("6") == 0:
                token_value = "8"
            tile_to_place_token_on = self.tiles[
                                      int(tiles_to_place_tokens_on
                                          [random.randint
                                           (0, (len(tiles_to_place_tokens_on)
                                            - 1))])]
            self.tiles[int(
                tile_to_place_token_on.relational_id)
                ].activation_value = int(token_value)
            tiles_to_place_tokens_on.remove(
                tile_to_place_token_on.relational_id)
            # Reject surrounding tiles as future candidates for reds.
            for e in tile_to_place_token_on.edges:
                for t in e.tiles:
                    if tile_to_place_token_on != t:
                        if t.relational_id in tiles_to_place_tokens_on:
                            rejected_tiles_for_reds.append(t.relational_id)
                            tiles_to_place_tokens_on.remove(t.relational_id)
            active_activation_values[token_value] -= 1
        # Rejected tiles are now considered for the rest of the tokens.
        while len(rejected_tiles_for_reds) > 0:
            tiles_to_place_tokens_on.append(rejected_tiles_for_reds.pop(0))
        # Place the rest of the tokens on the land tiles.
        for activation_value, amount in active_activation_values.items():
            while amount > 0:
                self.tiles[int(tiles_to_place_tokens_on.pop(
                    random.randint(0, (len(
                        tiles_to_place_tokens_on)
                        - 1))))].activation_value = activation_value
                amount -= 1

    def get_current_phase(self):
        return self.current_phase

    def get_current_game_phase(self):
        return self.current_game_phase

    def change_phase(self):
        self.current_phase += 1

    def change_game_phase(self):
        self.current_game_phase += 1
        if self.current_game_phase > 3:
            self.current_game_phase = 1

    """produce_resources:
    roll - Tiles with an activation value of this dice roll are the
           tiles involved with this procedure.
    Gives resources to the settlements adjacent to tiles with 
    activation value "roll". Settlements receive 1 of the tile's
    resource while cities receive 2.
    """
    def produce_resources(self, roll):
        productive_tiles = []
        for t in self.tiles:
            if str(t.activation_value) == str(roll) and not t.robber:
                productive_tiles.append(t)
        for pt in productive_tiles:
            starting_edge = pt.edges[0]
            starting_corner = pt.edges[0].corners[0]
            current_edge = starting_edge
            current_corner = starting_corner
            self.gather_resource_with_settlement(
                pt, current_corner, self.players)
            for c in current_edge.corners:
                if c != current_corner:
                    current_corner = c
                    break
            while c != starting_corner:
                for e in current_corner.edges:
                    if pt in e.tiles and e != current_edge:
                        current_edge = e
                        break
                self.gather_resource_with_settlement(
                    pt, current_corner, self.players)
                for c in current_edge.corners:
                    if c != current_corner:
                        current_corner = c
                        break
            valid_transaction = self.resource_bank.validate_transaction()
            if valid_transaction:
                for p in self.players:
                    p.resource_bank.validate_transaction()
            else:
                for p in self.players:
                    p.resource_bank.cancel_transaction()

    """produce_initial_resources:
    corner - the settlement that the player has placed.
    player - the player that receives the resources.
    Handles the scenario for resource collection upon placement of the
    second settlement during the setup phase. Gathers 1 resource for
    each tile adjacent to the placed settlement.
    """
    def produce_initial_resources(self, corner, player):
        adjacent_tiles = []
        for e in corner.edges:
            for t in e.tiles:
                if t not in adjacent_tiles:
                    adjacent_tiles.append(t)
        for at in adjacent_tiles:
            if ("desert" not in at.resource and "water" not in at.resource and
                    "port" not in at.resource):
                player.resource_bank.deposit_resource(at.resource, 1)
                player.resource_bank.validate_transaction()

    def __random_tile(self):
        return self.tiles[random.randint(0, len(self.tiles) - 1)]

    def get_tiles_ordered_by_physical_id(self):
        sorted_tiles = []
        for i in range(len(self.tiles)):
            for t in self.tiles:
                if (t.relational_id == 
                        self.relational_to_physical_id_mapping[i]):
                    sorted_tiles.append(t)
        return sorted_tiles

    def find_robber(self):
        for t in self.tiles:
            if t.robber:
                return t
    
    def gather_resource_with_settlement(self, tile, corner, players):
        resource = tile.resource
        if corner.settlement == "city": 
            quantity = 2
        elif corner.settlement == "settlement": 
            quantity = 1
        else:
            quantity = 0
        if corner.ownership != 0:
            for p in players:
                if p.id == corner.ownership:
                    owner = p
            owner.resource_bank.deposit_resource(resource, quantity)
            self.resource_bank.withdraw_resource(resource, quantity)

    def place_settlement(self, corner, player):
        if corner.does_corner_belong_to_a_player(
                player.id):
            if not corner.are_neighboring_corners_settled():
                if corner.settlement == "none":
                    if player.game_piece_bank.game_pieces[1] > 0:
                        if self.current_phase == 2:
                            player.resource_bank.spend_resources(
                                [1, 1, 1, 1, 0])
                            self.resource_bank.collect_resources(
                                [1, 1, 1, 1, 0])
                            transaction_valid = player\
                                .resource_bank.validate_transaction()
                            if transaction_valid:
                                self.resource_bank.validate_transaction()
                                player.game_piece_bank.place_settlement()
                                return ""
                            else:
                                return "Insufficient resources to" \
                                       " build a settlement!"
                        else:
                            player.game_piece_bank.place_settlement()
                            if self.reverse_turn_order is True:
                                self.produce_initial_resources(
                                    corner, player)
                            return ""
                    else:
                        return "No more settlements in your inventory!"
                elif corner.settlement == "settlement":
                    if player.game_piece_bank.game_pieces[2] > 0:
                        if self.reverse_turn_order is True:
                            return "Can't build cities during setup phase"
                        player.resource_bank.spend_resources(
                            [0, 0, 2, 0, 3])
                        self.resource_bank.collect_resources(
                            [0, 0, 2, 0, 3])
                        transaction_valid = player.\
                            resource_bank.validate_transaction()
                        if transaction_valid:
                            self.resource_bank.validate_transaction()
                            player.game_piece_bank.place_city()
                            return ""
                        else:
                            return "Insufficient resources to build a city!"
                    else:
                        return "No more cities in your inventory!"
                else:
                    return "Cities cannot be upgraded further!"
            else:
                return "Neighboring corners have settlements!"
        else:
            return "You don't own this " + corner.settlement + "!"

    def start_off_with_extra_resources(self, players):
        for p in players:
            p.resource_bank.collect_resources([3, 3, 3, 3, 3])
            p.resource_bank.validate_transaction()
            self.resource_bank.spend_resources([3, 3, 3, 3, 3])
            self.resource_bank.validate_transaction()

    def change_current_player(self, player):
        if self.current_player is None:
            self.current_player = self.players[0]
        else:
            for i in range(0, len(self.players)):  # Go to next player's turn
                if self.players[i] is player:
                    if (i == len(self.players) - 1
                       and self.reverse_turn_order is not True):
                        if self.current_phase == 1:
                            self.reverse_turn_order = True
                        else:
                            self.current_player = self.players[0]
                    elif (self.current_phase == 1
                          and self.reverse_turn_order is True):
                        if i == 0:
                            self.reverse_turn_order = False
                            self.change_phase()
                        else:
                            self.current_player = self.players[i - 1]
                    else:
                        self.current_player = self.players[i + 1]

    def retrieve_current_player(self):
        return self.current_player

    def retrieve_players(self):
        return self.players

    def randomize_turn_order(self):
        for i in range(0, len(self.players)-1):
            random_index = random.randint(0, len(self.players)-1)
            self.players[i].turn_priority, \
                self.players[random_index].turn_priority = \
                self.players[random_index].turn_priority, \
                self.players[i].turn_priority
            self.players[i], self.players[random_index] = \
                self.players[random_index], self.players[i]
        return self.players


def get_product_sum(num):
    sum = 0
    num += 1
    for i in range(num):
        if i > 0:
            sum += 6 * i
        else:
            sum += 1
    return sum


def set_edges(tiles, corners):
    edge = Edge()
    for i in range(len(tiles)):
        edge.add_corners(corners, tiles[i].relational_id)
        edge.add_tile(tiles[i])
        tiles[i].add_edge(edge)
        if edge.relational_id == "":
            edge.relational_id += tiles[i].relational_id
        else:
            edge.relational_id += ("-" + tiles[i].relational_id)
