from Tile import Tile
from LandTile import LandTile
from SeaTile import SeaTile
from Player import Player
from DieRoller import DieRoller
from ResourceBank import ResourceBank
from ResourceType import ResourceType
from PortType import PortType
from GamePieceType import GamePieceType
from CurrentPhase import CurrentPhase
from CurrentGamePhase import CurrentGamePhase
from EdgeCardinality import EdgeCardinality
from SettlementLevel import SettlementLevel

import random


class Board:
    NUM_DICE = 2
    LAND_TILE_QUANTITY = 19
    SEA_TILE_QUANTITY = 18
    ROAD_COST = [1, 0, 0, 1, 0]
    SETTLEMENT_COST = [1, 1, 1, 1, 0]
    CITY_COST = [0, 0, 2, 0, 3]
    EXTRA_RESOURCE_QUANTITIES = [3, 3, 3, 3, 3]
    NAMES = ["Feng", "Suggs", "Lotus", "Regina"]

    resources = {
        ResourceType.LUMBER.value: 4,
        ResourceType.WOOL.value: 4,
        ResourceType.GRAIN.value: 4,
        ResourceType.BRICK.value: 3,
        ResourceType.ORE.value: 3,
        ResourceType.DESERT.value: 1,
    }
    activation_values = {
        2: 1,
        3: 2,
        4: 2,
        5: 2,
        6: 2,
        8: 2,
        9: 2,
        10: 2,
        11: 2,
        12: 1,
    }

    def __init__(self, num_players):
        self.land_tiles = []
        self.sea_tiles = []
        self.players = []
        self.current_player = None
        self.resource_bank = ResourceBank(30)
        self.die_roller = DieRoller(self.NUM_DICE)
        self.current_phase = CurrentPhase.SETUP_PHASE.value
        self.current_game_phase = CurrentGamePhase.ROLL_DICE.value
        self.reverse_turn_order = False
        self.settlement_placement_during_setup = True
        for i in range(1, num_players + 1):
            self.players.append(Player(i, self.NAMES[i - 1], self))
        self.randomize_turn_order()
        current_coordinate = [0, 0]
        current_resources = Board.resources.copy()
        directions = self.retrieve_map_builder_directions()
        port_directions = self.retrieve_port_edge_directions()
        port_types = self.retrieve_randomized_port_list()
        current_coordinate = self.generate_land_tiles(
            current_coordinate, current_resources, directions)
        self.generate_sea_tiles(
            current_coordinate, directions, port_directions, port_types)

    """generate_land_tiles:
    Generates all land tiles for Ceten. This process takes a
    random resource and assigns it to a tile. Meanwhile, an
    implicit map builder changes the coordinate that the next
    tile will use by resorting to a list of set directions.
    """
    def generate_land_tiles(
            self, current_coordinate, current_resources, directions):
        for i in range(0, self.LAND_TILE_QUANTITY):
            (resource, resource_count) = random.choice(
                list(current_resources.items()))
            current_resources[resource] -= 1
            if resource_count - 1 < 1:
                current_resources.pop(resource)
            self.land_tiles.append(
                LandTile(current_coordinate, self.land_tiles, resource))
            current_coordinate = Tile.change_coordinate(
                current_coordinate, directions.pop(0))
        # Sea tile generations needs this to  continue from last land tile.
        return current_coordinate

    """generate_sea_tiles:
    Generates all sea tiles for Ceten. The implicit map builder will
    changes the coordinate that the next tile will use by using the
    remaining directions in the list. Meanwhile, every odd sea tile
    placed has a port. The direction the port faces and the type of
    port is dictated by a list of set port directions and a list of
    randomized port types.
    """
    def generate_sea_tiles(
            self, current_coordinate, directions, port_directions, port_types):
        for i in range(0, self.SEA_TILE_QUANTITY):
            port_type = None
            port_direction = None
            if i % 2 == 0:
                port_type = port_types.pop(0)
                port_direction = port_directions.pop(0)
            self.sea_tiles.append(
                SeaTile(
                    current_coordinate, self.sea_tiles + self.land_tiles,
                    port_type, port_direction))
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
        while (active_activation_values.get(6) > 0
                or active_activation_values.get(8)) > 0:
            token_value = 6
            if active_activation_values.get(6) == 0:
                token_value = 8
            tile_to_place_token_on = tiles_to_place_tokens_on.pop(
                random.randint(0, (len(tiles_to_place_tokens_on) - 1)))
            tile_to_place_token_on.activation_value = token_value
            tiles_with_a_token_placed.append(tile_to_place_token_on)
            # Reject surrounding tiles as future candidates for reds.
            for t in tile_to_place_token_on.get_adjacent_tiles(
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

    """produce_resources:
    Gives resources to the settlements adjacent to tiles with 
    activation value "roll". Settlements receive 1 of the tile's
    resource while cities receive 2.
    """
    def produce_resources(self, roll):
        productive_tiles = []
        for lt in self.land_tiles:
            if str(lt.activation_value) == str(roll) and not lt.robber:
                productive_tiles.append(lt)
        for pt in productive_tiles:
            for c in pt.corners:
                self.gather_resource_with_settlement(pt, c, self.players)
                valid_transaction = self.resource_bank.validate_transaction()
                if not valid_transaction:
                    break
            if valid_transaction:
                for p in self.players:
                    p.resource_bank.validate_transaction()
            else:
                for p in self.players:
                    p.resource_bank.cancel_transaction()

    """produce_initial_resources:
    Handles the scenario for resource collection upon placement of the
    second settlement during the setup phase. Gathers 1 resource for
    each tile adjacent to the placed settlement.
    """
    def produce_initial_resources(self, corner, player):
        adjacent_tiles = []
        for t in corner.tiles:
            if t not in adjacent_tiles:
                adjacent_tiles.append(t)
        for at in adjacent_tiles:
            if at.resource is not ResourceType.DESERT.value:
                player.resource_bank.deposit_resource(at.resource, 1)
                player.resource_bank.validate_transaction()
                self.resource_bank.withdraw_resource(at.resource, 1)
                self.resource_bank.validate_transaction()

    """place_road:
    The logic for a player placing a road. Costs 1 lumber and 1 brick.
    - Road must be adjacent to another road owned by the player.
    - Above rule must also have the settlement in between the roads
      not be owned by a different player.
    - Edge must not already be occupied by a road.
    During setup phase:
    - Road must be next to the settlement that the player just placed.
    """
    def place_road(self, edge, player):
        if edge.road_is_not_occupied():
            if (player.game_piece_bank.game_pieces[
                 GamePieceType.ROAD.value] > 0):
                if self.current_phase == CurrentPhase.GAME_PHASE.value:
                    if edge.road_can_be_placed(player.id):
                        player.resource_bank.spend_resources(
                            self.ROAD_COST)
                        self.resource_bank.collect_resources(
                            self.ROAD_COST)
                        transaction_valid = (
                            player.resource_bank.validate_transaction())
                        if transaction_valid:
                            self.resource_bank.validate_transaction()
                            player.game_piece_bank.place_road()
                            return ""
                        else:
                            return "Insufficient resources to build a road!"
                    else:
                        return "Cannot place road here!"
                elif not self.settlement_placement_during_setup:
                    if edge.road_can_be_placed_during_setup(player.id):
                        player.game_piece_bank.place_road()
                        self.settlement_placement_during_setup = True
                        return ""
                    else:
                        return "Road must be next to current settlement!"
                else:
                    return "Must place a settlement!"
            else:
                return "No more roads in your inventory!"
        else:
            return "Road has already been built here."

    """place_settlement:
    The logic for a player placing a settlement or city. Settlements
    require 1 of every resource except ore, Cities require 2 grain and
    3 ore.
    - Settlement must be adjacent to a player's road (except during
      setup phase)
    - Settlement cannot be placed next to another settlement.
    - Cities must be built on an already existing settlement.
    """
    def place_settlement(self, corner, player):
        if corner.is_settlement_not_settled_by_current_player(player.id):
            if not corner.are_neighboring_corners_settled():
                if corner.settlement == SettlementLevel.NONE.value:
                    if (player.game_piece_bank.game_pieces[
                         GamePieceType.SETTLEMENT.value] > 0):
                        if self.current_phase == CurrentPhase.GAME_PHASE.value:
                            if corner.corner_adjacent_to_players_road(
                                    player.id):
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
                                    return (
                                        "Insufficient resources to "
                                        + "build a settlement!")
                            else:
                                return "Settlement must be next to your road!"
                        elif self.settlement_placement_during_setup:
                            player.game_piece_bank.place_settlement()
                            if self.reverse_turn_order:
                                self.produce_initial_resources(corner, player)
                            self.settlement_placement_during_setup = False
                            return ""
                        else:
                            return "Must place a road!"
                    else:
                        return "No more settlements in your inventory!"
                elif corner.settlement == SettlementLevel.SETTLEMENT.value:
                    if (player.game_piece_bank.game_pieces[
                         GamePieceType.CITY.value] > 0):
                        if self.reverse_turn_order is True:
                            return "Can't build cities during setup phase!"
                        player.resource_bank.spend_resources(self.CITY_COST)
                        self.resource_bank.collect_resources(self.CITY_COST)
                        transaction_valid = (
                            player.resource_bank.validate_transaction())
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
            return "Can't upgrade another player's settlement!"

    """gather_resource_with_settlement:
    Directly gives the generated resource to the settlements next to
    tiles responsible for giving resources during the current turn.
    Cities give 2 resources, Settlements give 1 resource, unoccupied
    corners give no resources.
    """
    def gather_resource_with_settlement(self, tile, corner, players):
        resource = tile.resource
        if corner.settlement == SettlementLevel.CITY.value:
            quantity = 2
        elif corner.settlement == SettlementLevel.SETTLEMENT.value:
            quantity = 1
        else:  # Settlement level is at none.
            quantity = 0
        if corner.ownership != 0:
            for p in players:
                if p.id == corner.ownership:
                    owner = p
            owner.resource_bank.deposit_resource(resource, quantity)
            self.resource_bank.withdraw_resource(resource, quantity)

    """change_current_player:
    Changes the player after the current player ends their turn.
    The next player that gets his/her turn depends on the randomized
    turn order. Reverse turn order applies for the second half of
    the setup phase.
    """
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

    def find_robber_tile(self):
        for t in self.land_tiles:
            if t.robber:
                return t

    def get_current_phase(self):
        return self.current_phase

    def get_current_game_phase(self):
        return self.current_game_phase

    def change_phase(self):
        self.current_phase += 1

    def advance_game_phase(self):
        self.current_game_phase += 1
        if self.current_game_phase > len(CurrentGamePhase):
            self.current_game_phase = CurrentGamePhase.ROLL_DICE.value

    def recede_game_phase(self):
        if self.current_game_phase > 1:
            self.current_game_phase -= 1

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

    """retrieve_map_builder_directions:
    This logic dictates the sequence of directions the map builder will
    traverse. i dictates the number of circular loops made, j
    represents a clockwise traversal of all edge directions. 
    For each loop, first pass of Top-left is always appended once while
    Top-right is appended one time less than the other directions.
    This builds the base map for a 3-4 player Ceten game.
    """
    @staticmethod
    def retrieve_map_builder_directions():
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

    """retrieve_port_edge_directions:
    This logic dictates the sequence of directions the map builder will
    place edges for sea tiles. This is intended to be used with the
    map builder that builds the base board, where ports are placed every
    odd sea tile (in comparison to when the first sea tile is placed.
    """
    @staticmethod
    def retrieve_port_edge_directions():
        directions = []
        for i in range(EdgeCardinality.TOP_LEFT.value,
                       EdgeCardinality.LEFT.value + 2):
            # First port faces rightwards.
            true_direction = i + 2 % len(EdgeCardinality)
            directions.append(true_direction % len(EdgeCardinality))
            # Direction that you start and end off with are only applied once.
            if (i % 2 != 0 and true_direction != EdgeCardinality.RIGHT.value
                    and true_direction != EdgeCardinality.RIGHT.value):
                directions.append(true_direction % len(EdgeCardinality))
        return directions

    """
    retrieve_randomized_port_list:
    This function gives the list of port types that will be used for the
    base version of Ceten. 4 standard ports and 5 specialized ports for
    each resource type are used.
    """
    @staticmethod
    def retrieve_randomized_port_list():
        num_standard_ports = 5
        port_types = []
        for i in range(0, num_standard_ports):
            port_types.append(PortType.STANDARD.value)
        port_types.append(PortType.LUMBER.value)
        port_types.append(PortType.WOOL.value)
        port_types.append(PortType.GRAIN.value)
        port_types.append(PortType.BRICK.value)
        port_types.append(PortType.ORE.value)
        for i in range(0, len(port_types)):
            random_index = random.randint(0, len(port_types)-1)
            port_types[i], port_types[random_index] = \
                port_types[random_index], port_types[i]
        return port_types

    # For debugging purposes only!
    def start_off_with_extra_resources(self, players):
        for p in players:
            p.resource_bank.collect_resources(self.EXTRA_RESOURCE_QUANTITIES)
            p.resource_bank.validate_transaction()
            self.resource_bank.spend_resources(self.EXTRA_RESOURCE_QUANTITIES)
            self.resource_bank.validate_transaction()



