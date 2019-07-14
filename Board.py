from Tile import Tile
from LandTile import LandTile
from SeaTile import SeaTile
from Player import Player
from DieRoller import DieRoller
from ResourceBank import ResourceBank
from ResourceType import ResourceType
from GamePieceType import GamePieceType
from CurrentPhase import CurrentPhase
from CurrentGamePhase import CurrentGamePhase
from EdgeCardinality import EdgeCardinality

import random


class Board:
    NUM_DICE = 2
    LAND_TILE_QUANTITY = 19
    SEA_TILE_QUANTITY = 18
    SETTLEMENT_COST = [1, 1, 1, 1, 0]
    CITY_COST = [0, 0, 2, 0, 3]
    EXTRA_RESOURCE_QUANTITIES = [3, 3, 3, 3, 3]

    resources = {
        ResourceType.LUMBER.value: 4,
        ResourceType.WOOL.value: 4,
        ResourceType.GRAIN.value: 4,
        ResourceType.BRICK.value: 3,
        ResourceType.ORE.value: 3,
        ResourceType.DESERT.value: 1,
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

    def __init__(self, num_players):
        self.land_tiles = []
        self.sea_tiles = []
        self.players = []
        self.current_player = None
        self.resource_bank = ResourceBank(19)
        self.die_roller = DieRoller(self.NUM_DICE)
        self.current_phase = CurrentPhase.SETUP_PHASE.value
        self.current_game_phase = CurrentGamePhase.ROLL_DICE.value
        self.reverse_turn_order = False
        current_resources = Board.resources.copy()
        for i in range(1, num_players + 1):
            self.players.append(
                    Player(i, "Player" + str(i)))
        self.randomize_turn_order()
        current_coordinate = [0, 0]
        directions = self.retrieve_map_builder_directions()

        for i in range(0, self.LAND_TILE_QUANTITY):
            (resource, resource_count) = random.choice(
                list(current_resources.items()))
            current_resources[resource] -= 1
            if resource_count - 1 < 1:
                current_resources.pop(resource)
            self.land_tiles.append(LandTile(current_coordinate, resource))
            current_coordinate = Tile.change_coordinate(
                current_coordinate, directions.pop(0))

        for i in range(0, self.SEA_TILE_QUANTITY):
            self.sea_tiles.append(SeaTile(current_coordinate))
            if i < self.SEA_TILE_QUANTITY - 1:
                current_coordinate = Tile.change_coordinate(
                    current_coordinate, directions.pop(0))
        self.place_tokens()

    """place_tokens:
    Places tokens on land tiles. These tokens have an activation value
    that represents the total dice value required for the tile to give
    the adjacent settlements and cities resources. This algorithm was 
    designed so that tokens with values 6 and 8 are not adjacent to 
    each other.
    """
    def place_tokens(self):
        active_activation_values = self.activation_values.copy()
        tiles_to_place_tokens_on = self.land_tiles
        rejected_tiles_for_reds = []      # 6's and 8's referred to as reds.
        tiles_with_a_token_placed = []

        # Desert tile gets no token
        for t in tiles_to_place_tokens_on:
            if t.resource == ResourceType.DESERT.value:
                tiles_with_a_token_placed.append(t)
                tiles_to_place_tokens_on.remove(t)
        # Place 6's first, then 8's after.
        while (active_activation_values.get("6") > 0
                or active_activation_values.get("8")) > 0:
            token_value = "6"
            if active_activation_values.get("6") == 0:
                token_value = "8"
            tile_to_place_token_on = tiles_to_place_tokens_on.pop(
                random.randint(0, (len(tiles_to_place_tokens_on) - 1)))
            tile_to_place_token_on.activation_value = int(token_value)
            tiles_with_a_token_placed.append(tile_to_place_token_on)
            # Reject surrounding tiles as future candidates for reds.
            for t in tile_to_place_token_on.get_adjacent_land_tiles(
                    self.land_tiles):
                tiles_to_place_tokens_on.remove(t)
                rejected_tiles_for_reds.append(t)
            active_activation_values[token_value] -= 1
        # Rejected tiles are now considered for the rest of the tokens.
        while len(rejected_tiles_for_reds) > 0:
            tiles_to_place_tokens_on.append(rejected_tiles_for_reds.pop(0))
        # Place the rest of the tokens on the land tiles.
        for activation_value, amount in active_activation_values.items():
            while amount > 0:
                tile_to_place_token_on = tiles_to_place_tokens_on.pop(
                    random.randint(0, (len(tiles_to_place_tokens_on) - 1)))
                tile_to_place_token_on.activation_value = int(activation_value)
                tiles_with_a_token_placed.append(tile_to_place_token_on)
                amount -= 1
        self.land_tiles = tiles_with_a_token_placed

    def get_current_phase(self):
        return self.current_phase

    def get_current_game_phase(self):
        return self.current_game_phase

    def change_phase(self):
        self.current_phase += 1

    def change_game_phase(self):
        self.current_game_phase += 1
        if self.current_game_phase > len(CurrentGamePhase):
            self.current_game_phase = CurrentGamePhase.ROLL_DICE.value

    """produce_resources:
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
                    if (player.game_piece_bank.game_pieces[
                         GamePieceType.SETTLEMENT.value] > 0):
                        if self.current_phase == CurrentPhase.GAME_PHASE.value:
                            player.resource_bank.spend_resources(
                                self.SETTLEMENT_COST)
                            self.resource_bank.collect_resources(
                                self.SETTLEMENT_COST)
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
                    if (player.game_piece_bank.game_pieces[
                         GamePieceType.CITY.value] > 0):
                        if self.reverse_turn_order is True:
                            return "Can't build cities during setup phase!"
                        player.resource_bank.spend_resources(self.CITY_COST)
                        self.resource_bank.collect_resources(self.CITY_COST)
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
            p.resource_bank.collect_resources(self.EXTRA_RESOURCE_QUANTITIES)
            p.resource_bank.validate_transaction()
            self.resource_bank.spend_resources(self.EXTRA_RESOURCE_QUANTITIES)
            self.resource_bank.validate_transaction()

    def change_current_player(self, player):
        if self.current_player is None:
            self.current_player = self.players[0]
        else:
            for i in range(0, len(self.players)):  # Go to next player's turn
                if self.players[i] is player:
                    if (i == len(self.players) - 1
                       and self.reverse_turn_order is not True):
                        if (self.current_phase ==
                                CurrentPhase.SETUP_PHASE.value):
                            self.reverse_turn_order = True
                        else:
                            self.current_player = self.players[0]
                    elif (self.current_phase == CurrentPhase.SETUP_PHASE.value
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

    '''
    retrieve_map_builder_directions:
    This logic dictates the sequence of directions the map builder will
    traverse. i dictates the number of circular loops made, j
    represents a clockwise traversal of all edge directions. 
    For each loop, first pass of Top-left is always appended once while
    Top-right is appended one time less than the other directions.
    This builds the base map for a 3-4 player Ceten game.
    '''
    def retrieve_map_builder_directions(self):
        directions = []
        for i in range(1, 4):
            for j in range(EdgeCardinality.TOP_LEFT.value,
                           EdgeCardinality.LEFT.value + 2):
                if j == EdgeCardinality.TOP_RIGHT.value:
                    i -= 1
                for k in range(0, i):
                    directions.append(j % len(EdgeCardinality))
                    if j == EdgeCardinality.TOP_LEFT.value:
                        break
                if j == EdgeCardinality.TOP_RIGHT.value:
                    i += 1
        return directions
