from Tile import Tile
from Edge import Edge
from Corner import Corner
from Player import Player
import random
import re
import pdb

class Board:
    resources = {
    "ore"    : 3,
    "desert" : 1,
    "brick"  : 3,
    "wool"   : 4,
    "grain"  : 4,
    "lumber" : 4,
    }
    activation_values = {
    "2"  : 1,
    "3"  : 2,
    "4"  : 2,
    "5"  : 2,
    "6"  : 2,
    "8"  : 2,
    "9"  : 2,
    "10" : 2,
    "11" : 2,
    "12" : 1,
    }
    relational_to_physical_id_mapping = [
        "30", "29", "28", "27",
        "31", "14", "13", "12", "26",
        "32", "15", "4", "3", "11","25", 
        "33", "16", "5", "0", "2", "10", "24",
        "34", "17", "6", "1", "9", "23",
        "35", "18", "7", "8", "22",
        "36", "19", "20", "21"
    ]

    def __init__(self, tile_count=37):
        self.tiles = []
        self.players = []
        self.num_lumber = 19
        self.num_wool = 19
        self.num_grain = 19
        self.num_brick = 19
        self.num_ore = 19
        self.num_lumber_buffer = 0
        self.num_wool_buffer = 0
        self.num_grain_buffer = 0
        self.num_brick_buffer = 0
        self.num_ore_buffer = 0
        while len(Board.resources) > 0 and len(Board.activation_values) > 0:
            (resource, resource_count) = random.choice(
                                         list(Board.resources.items()))
            if (resource_count < 1):
                Board.resources.pop(resource)
                continue
            if (resource == "desert"):
                tile = Tile(resource, 0)
                tile.robber = True
                self.tiles.append(tile)
                Board.resources[resource] -= 1
                continue
            (activation_value, 
            activation_value_count) = random.choice(list
                                      (Board.activation_values.items()))
            if (activation_value_count < 1):
                Board.activation_values.pop(activation_value)
                continue
            self.tiles.append(Tile(resource, activation_value))
            Board.resources[resource] -= 1
            Board.activation_values[activation_value] -= 1
        port_types = ["grain", "ore", "standard", "wool", "standard",
                      "standard", "brick", "lumber", "standard"]
        current_direction = 1
        for i in range(19, 37):
            if i % 2 == 0:
                t = Tile(port_types.pop(random.randint(0, len(port_types)-1))
                   + "_port", 0)
            else:
                t = Tile("water", 0)
            self.tiles.append(t)
                
    def connect_board(self):
        num_circles = 2;
        total_tile_quantity = get_product_sum(num_circles)
        val = 1
        level = 1
        self.tiles[0].relational_id = str(0)
        while level <= num_circles + 1:
            level_tile_quantity = get_product_sum(level)
            nth_tile_being_iterated = 1
            if (level == 1):           #Middle Level
                while nth_tile_being_iterated < 6*level + 1:
                    self.tiles[val].relational_id = str(val)
                    second_corner = Corner()
                    third_corner = Corner()
                    if (nth_tile_being_iterated == 1):
                        first_corner = Corner()
                        final_corner = first_corner
                    set_edges([self.tiles[val], self.tiles[val-1]],
                                  [first_corner, second_corner])
                    if (nth_tile_being_iterated == 6*level):
                        third_corner = final_corner
                    if (nth_tile_being_iterated > 1):
                        set_edges([self.tiles[val], self.tiles[0]],
                                      [first_corner, third_corner])
                    if (nth_tile_being_iterated == 6*level):
                        bridge_corner = Corner()
                        set_edges([self.tiles[val], self.tiles[1]],
                                      [third_corner, bridge_corner])
                    if (nth_tile_being_iterated == 1):
                        first_corner = second_corner
                    else:
                        first_corner = third_corner
                    nth_tile_being_iterated += 1
                    val += 1
                level += 1
            elif (level == 2):                       #Outer Level
                first_corner = bridge_corner
                adjacent_tile_of_previous_level = val - 6*(level-1)
                tiles_on_current_level_iterated = 0
                while nth_tile_being_iterated < 6*level+1:
                    self.tiles[val].relational_id = str(val)
                    second_corner = Corner()
                    third_corner = Corner()
                    set_edges([self.tiles[val], self.tiles[val-1]],
                                  [first_corner, second_corner])
                    if (val == 18):
                        third_corner = final_corner
                    if (val > 7 and nth_tile_being_iterated % 2 == 1):
                        corners_of_edges = []
                        for e in self.tiles[
                                 adjacent_tile_of_previous_level].edges:
                            for c in e.corners:
                                if (self.tiles[
                                    adjacent_tile_of_previous_level]
                                    .num_edges_connected_to_corner(c) == 1
                                    and c != first_corner):
                                    third_corner = c
                    set_edges([self.tiles[val],
                                   self.tiles[
                                   adjacent_tile_of_previous_level]],
                                  [first_corner, third_corner])
                    if (val == 7):
                        final_corner = second_corner
                    if (val == 12):
                        second_corner = final_corner
                    if (val > 7 and nth_tile_being_iterated % 2 == 1):
                        fourth_corner = Corner()
                        adjacent_tile_of_previous_level += 1
                        set_edges([self.tiles[val],
                                       self.tiles[
                                       adjacent_tile_of_previous_level]],
                                      [third_corner, fourth_corner])
                        first_corner = fourth_corner
                    else:
                        first_corner = third_corner
                    if (nth_tile_being_iterated == 6*level):
                        fourth_corner = Corner()
                        set_edges([self.tiles[val], 
                                       self.tiles[val - 6*level + 1]],
                                      [third_corner, fourth_corner])
                        if (val == 18):
                            bridge_corner = fourth_corner                  
                    lone_edges_to_generate = 3 - (nth_tile_being_iterated%2)
                    nth_tile_being_iterated += 1
                    val += 1
                level += 1
            else:
                nth_tile_being_iterated = 7;
                first_corner = bridge_corner
                while nth_tile_being_iterated < total_tile_quantity:
                    second_corner = Corner()
                    self.tiles[val].relational_id = str(val)
                    set_edges([self.tiles[nth_tile_being_iterated],
                                   self.tiles[val]], 
                                  [first_corner, second_corner])
                    val += 1
                    if (nth_tile_being_iterated % 2 == 1):
                        second_to_last_corner = second_corner
                    else:
                        third_corner = Corner()
                        self.tiles[val].relational_id = str(val)
                        set_edges([self.tiles[nth_tile_being_iterated],
                                       self.tiles[val]], 
                                      [second_corner, third_corner])
                        second_to_last_corner = third_corner
                        val += 1
                    if (nth_tile_being_iterated == 18):
                        next_index = 7
                        val = 19
                        last_corner = bridge_corner
                    else:
                        next_index = nth_tile_being_iterated+1                        
                        for e in self.tiles[next_index].edges:
                            for c in e.corners:
                                has_current_tile = re.search("([0-9]+-"
                                                             + str(nth_tile_being_iterated)
                                                             + ")|("
                                                             + str(nth_tile_being_iterated)
                                                             + "[0-9]+)",
                                                             e.relational_id)
                                if (has_current_tile):
                                    two_corners_only = re.search("(^[0-9]+-"
                                                                 + str(nth_tile_being_iterated)
                                                                 + "$)|(^"
                                                                 + str(nth_tile_being_iterated)
                                                                 + "[0-9]+)$", 
                                                                 c.relational_id)
                                    if (two_corners_only):
                                        last_corner = c 
                    self.tiles[val].relational_id = str(val)           
                    set_edges([self.tiles[nth_tile_being_iterated],
                                   self.tiles[val]],
                                  [second_to_last_corner, last_corner])
                    first_corner = last_corner
                    nth_tile_being_iterated += 1
                level += 1
        for t in self.tiles:
            if (t.relational_id != '' and int(t.relational_id) < 19):
                t.physical_id = self.relational_to_physical_id_mapping[
                                int(t.relational_id)]
        self.tile_info()

    def tile_info(self):
        for t in self.tiles:
            corners_of_edges = []
            edge_ids = ""
            corner_ids = []
            for e in t.edges:
                if (edge_ids == ""):
                    edge_ids += e.relational_id
                else:
                    edge_ids += (", " + e.relational_id)
                for c in e.corners:
                    corners_of_edges.append(c)
                    corner_ids.append(c.relational_id)
            corner_ids = set(corner_ids)
            corner_id_string = ""
            for c in corner_ids:
                if (corner_id_string == ""):
                    corner_id_string += str(c)
                else:
                    corner_id_string += (", " + str(c))
            corners_of_current_tile = set(corners_of_edges)
            info = "Tile #" + t.relational_id + ": " \
                  + "Edge Relationships - {" + edge_ids + "}, " + ": " \
                  + "Corner Relationships - {" + corner_id_string + "}, " \
                  + str(len(corners_of_current_tile)) \
                  + " corners, Resource: " + t.resource
            print(info)

    def board_str(self):
        ret = ""
        count = 1;
        for t in self.tiles:
            print("TILE #" + str(count))
            ret += ("TILE #" + str(count) + t.str())
            count += 1

    def produce_resources(self, roll):
        productive_tiles = []
        for t in self.tiles:
            if str(t.activation_value) == str(roll) and not t.robber:
                productive_tiles.append(t)
        for pt in productive_tiles:
            print("Traversing Tile #" + pt.relational_id)
            starting_edge = pt.edges[0]
            starting_corner = pt.edges[0].corners[0]
            current_edge = starting_edge
            current_corner = starting_corner
            self.gather_resource_with_settlement(pt, current_corner)
            for c in current_edge.corners:
                if c != current_corner:
                    current_corner = c
                    break
            while c != starting_corner:
                for e in current_corner.edges:
                    if pt in e.tiles and e != current_edge:
                        current_edge = e
                        break
                self.gather_resource_with_settlement(pt, current_corner)
                for c in current_edge.corners:
                    if c != current_corner:
                        current_corner = c
                        break
            if self.did_resource_deplete(pt.resource):
                for p in self.players:
                    p.clear_buffer_of_specific_resource(pt.resource)
        for p in self.players:
            p.confirm_resource_collection()

    def __random_tile(self):
        return self.tiles[random.randint(0,len(self.tiles) - 1)]

    def get_tiles_ordered_by_physical_ID(self):
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
    
    def gather_resource_with_settlement(self, tile, corner):
        resource = tile.resource
        if corner.settlement == "city": 
            quantity = 2;
        elif corner.settlement == "settlement": 
            quantity = 1;
        else:
            quantity = 0;
        if corner.ownership != 0:
            owner = self.players[corner.ownership-1]
            owner.add_resources_to_buffer(resource, quantity)
            self.add_resources_to_buffer(resource, quantity)

    def add_resources_to_buffer(self, resource, quantity):
        if resource == "lumber":
            self.num_lumber_buffer += quantity
        elif resource == "wool":
            self.num_wool_buffer += quantity
        elif resource == "grain":
            self.num_grain_buffer += quantity
        elif resource == "brick":
            self.num_brick_buffer += quantity
        elif resource == "ore":
            self.num_ore_buffer += quantity
    
    def did_resource_deplete(self, resource):
        if resource == "lumber":
            if (self.num_lumber-self.num_lumber_buffer) < 0:
                return True
            else:
                return False
        elif resource == "wool":
            if (self.num_wool-self.num_wool_buffer) < 0:
                return True
            else:
                return False
        elif resource == "grain":
            if (self.num_grain-self.num_grain_buffer) < 0:
                return True
            else:
                return False
        elif resource == "brick":
            if (self.num_brick-self.num_brick_buffer) < 0:
                return True
            else:
                return False
        elif resource == "ore":
            if (self.num_ore-self.num_ore_buffer) < 0:
                return True
            else:
                return False
    
    def can_resources_be_spent(self, player, lumber, wool, grain, brick, ore):
        if (player.num_lumber < lumber):
            return False
        if (player.num_wool < wool):
            return False
        if (player.num_grain < grain):
            return False
        if (player.num_brick < brick):
            return False
        if (player.num_ore < ore):
            return False
        return True
        
    def spend_resources(self, player, lumber, wool, grain, brick, ore):
        player.num_lumber -= lumber
        player.num_wool -= wool
        player.num_grain -= grain
        player.num_brick -= brick
        player.num_ore -= ore
        self.num_lumber += lumber
        self.num_wool += wool
        self.num_grain += grain
        self.num_brick += brick
        self.num_ore += ore

    def simulate_starting_phase(self):
        self.tiles[9].edges[2].corners[1].settlement = "settlement"
        self.tiles[9].edges[2].corners[1].ownership = 1
        self.tiles[7].edges[0].corners[1].settlement = "settlement"
        self.tiles[7].edges[0].corners[1].ownership = 2
        self.tiles[15].edges[2].corners[1].settlement = "settlement"
        self.tiles[15].edges[2].corners[1].ownership = 3
        self.tiles[12].edges[1].corners[1].settlement = "settlement"
        self.tiles[12].edges[1].corners[1].ownership = 4
        for p in self.players:
            p.num_lumber = 3
            p.num_wool = 3
            p.num_grain = 3
            p.num_brick = 3
            p.num_ore = 3
            p.num_settlements -= 1
            self.num_lumber -= 3
            self.num_wool -= 3
            self.num_grain -= 3
            self.num_brick -= 3
            self.num_ore -= 3
            
    def str(self):
        ret = "Board has the Following Tiles:\n"
        for t in self.tiles:
            ret += t.str() + "\n"
        return ret


def get_product_sum(num):
    sum = 0
    num += 1
    for i in range(num):
        if (i > 0):
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
        if (edge.relational_id == ""):
            edge.relational_id += tiles[i].relational_id
        else:
            edge.relational_id += ("-" + tiles[i].relational_id)

