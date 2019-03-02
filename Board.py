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
        "14", "13", "12", "15", "4", 
        "3", "11", "16", "5", "0", 
        "2", "10", "17", "6", "1",
        "9", "18", "7", "8"
    ]

    def __init__(self, tile_count = 19):
        self.tiles = []
        self.players = []
        while len(Board.resources) > 0 and len(Board.activation_values) > 0:
            (rs, rs_count)  = random.choice(list(Board.resources.items()))
            if (rs_count < 1):
                Board.resources.pop(rs)
                continue
            if (rs == "desert"):
                t = Tile(rs,0)
                t.robber = True
                self.tiles.append(t)
                Board.resources[rs]-= 1
                continue
            (av, av_count) = random.choice(list(Board.activation_values.items()))
            if (av_count < 1):
                Board.activation_values.pop(av)
                continue
            self.tiles.append(Tile(rs,av))
            Board.resources[rs]-= 1
            Board.activation_values[av]-=1
      
    def connectBoard(self):
        num_circles = 2;
        total_tile_quantity = get_product_sum(num_circles)
        val = 1
        level = 1
        self.tiles[0].relational_id = str(0)
        while level <= num_circles+1:
            level_tile_quantity = get_product_sum(level)
            nth_tile_being_iterated = 1
            if (level == 1):           #Middle Level
                while nth_tile_being_iterated < 6*level+1:
                    self.tiles[val].relational_id = str(val)
                    second_corner = Corner()
                    third_corner = Corner()
                    if (nth_tile_being_iterated == 1):
                        first_corner = Corner()
                        final_corner = first_corner
                    setInnerEdges([self.tiles[val], self.tiles[val-1]], [first_corner, second_corner])
                    if (nth_tile_being_iterated == 6*level):
                        third_corner = final_corner
                    if (nth_tile_being_iterated > 1):
                        setInnerEdges([self.tiles[val], self.tiles[0]], [first_corner, third_corner])
                    if (nth_tile_being_iterated == 6*level):
                        bridge_corner = Corner()
                        setInnerEdges([self.tiles[val], self.tiles[1]], [third_corner, bridge_corner])
                    if (nth_tile_being_iterated == 1):
                        first_corner = second_corner
                    else:
                        first_corner = third_corner
                    nth_tile_being_iterated = nth_tile_being_iterated + 1
                    val = val + 1
                level += 1
            elif (level == 2):                       #Outer Level
                first_corner = bridge_corner
                adjacent_tile_of_previous_level = val - 6*(level-1)
                tiles_on_current_level_iterated = 0
                while nth_tile_being_iterated < 6*level+1:
                    self.tiles[val].relational_id = str(val)
                    second_corner = Corner()
                    third_corner = Corner()
                    setInnerEdges([self.tiles[val], self.tiles[val-1]], [first_corner, second_corner])
                    if (val == 18):
                        third_corner = final_corner
                    if (val > 7 and nth_tile_being_iterated % 2 == 1):
                        corners_of_edges = []
                        for e in self.tiles[adjacent_tile_of_previous_level].edges:
                            for c in e.corners:
                                if (self.tiles[adjacent_tile_of_previous_level].numEdgesConnectedToCorner(c) == 1 and c != first_corner):
                                    third_corner = c
                    setInnerEdges([self.tiles[val], self.tiles[adjacent_tile_of_previous_level]], [first_corner, third_corner])
                    if (val == 7):
                        final_corner = second_corner
                    if (val == 12):
                        second_corner = final_corner
                    if (val > 7 and nth_tile_being_iterated % 2 == 1):
                        fourth_corner = Corner()
                        adjacent_tile_of_previous_level += 1
                        setInnerEdges([self.tiles[val], self.tiles[adjacent_tile_of_previous_level]], [third_corner, fourth_corner])
                        first_corner = fourth_corner
                    else:
                        first_corner = third_corner
                    if (nth_tile_being_iterated == 6*level):
                        fourth_corner = Corner()
                        setInnerEdges([self.tiles[val], self.tiles[val - 6*level+1]], [third_corner, fourth_corner])
                        if (val == 18):
                            bridge_corner = fourth_corner                  
                    lone_edges_to_generate = 3 - (nth_tile_being_iterated % 2)
                    nth_tile_being_iterated = nth_tile_being_iterated + 1
                    val = val + 1
                level += 1
            else:
                nth_tile_being_iterated = 7;
                first_corner = bridge_corner
                while nth_tile_being_iterated < total_tile_quantity:
                    second_corner = Corner()
                    setPerimeterEdges(self.tiles[nth_tile_being_iterated], str(val), [first_corner, second_corner])
                    val += 1
                    if (nth_tile_being_iterated % 2 == 1):
                        second_to_last_corner = second_corner
                    else:
                        third_corner = Corner()
                        setPerimeterEdges(self.tiles[nth_tile_being_iterated], str(val), [second_corner, third_corner])
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
                                has_current_tile = re.search("([0-9]+-" + str(nth_tile_being_iterated) + ")|(" + str(nth_tile_being_iterated) + "[0-9]+)", e.relational_id)
                                if (has_current_tile):
                                    two_corners_only = re.search("(^[0-9]+-" + str(nth_tile_being_iterated) + "$)|(^" + str(nth_tile_being_iterated) + "[0-9]+)$", c.relational_id)
                                    if (two_corners_only):
                                        last_corner = c            
                    setPerimeterEdges(self.tiles[nth_tile_being_iterated], str(val), [second_to_last_corner, last_corner])
                    first_corner = last_corner
                    nth_tile_being_iterated += 1
                level += 1
        for t in self.tiles:
            t.physical_id = self.relational_to_physical_id_mapping[int(t.relational_id)]    
        self.tile_info()
        self.settlementAndCitySimulation()

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
            info = "Tile #" + t.relational_id + ": " + "Edge Relationships - {" + edge_ids + "}, " \
                 + ": " + "Corner Relationships - {" + corner_id_string + "}, " + str(len(corners_of_current_tile)) + " corners, Resource: " + t.resource
            print(info)

    def board_str(self):
        ret = ""
        count = 1;
        for t in self.tiles:
            print("TILE #" + str(count))
            ret += ("TILE #" + str(count) + t.str())
            count += 1

    def connect_tiles(self):
        seed = self.__random_tile()
        #generate a random ring of tiles around the seed tile	
        for e in seed.edges:
            if(e.connected_tiles != 2):
                t = self.__random_tile()
                e.adjacent_tiles.append(t)
                t.edges.append(e)
                inner_ring.append(t)

    def produceResources(self, roll):
        productive_tiles = []
        for t in self.tiles:
            if str(t.activation_value) == str(roll) and t.robber == False:
                productive_tiles.append(t)
        for pt in productive_tiles:
            print("Traversing Tile #" + pt.relational_id)
            starting_edge = pt.edges[0]
            starting_corner = pt.edges[0].corners[0]
            current_edge = starting_edge
            current_corner = starting_corner
            self.gatherResourceWithSettlement(pt, current_corner)
            for c in current_edge.corners:
                if c != current_corner:
                    current_corner = c
                    break
            while c != starting_corner:
                for e in current_corner.edges:
                    if pt in e.tiles and e != current_edge:
                        current_edge = e
                        break
                self.gatherResourceWithSettlement(pt, current_corner)
                for c in current_edge.corners:
                    if c != current_corner:
                        current_corner = c
                        break

    def __random_tile(self):
        return self.tiles[random.randint(0,len(self.tiles) - 1)]

    def getTilesOrderedByPhysicalID(self):
        sorted_tiles = []
        for i in range(len(self.tiles)):
            for t in self.tiles:
                if (t.relational_id == self.relational_to_physical_id_mapping[i]):
                    sorted_tiles.append(t)
        return sorted_tiles

    def find_robber(self):
        for t in self.tiles:
            if t.robber == True:
                return t

    def settlementAndCitySimulation(self):
        self.tiles[11].edges[4].corners[1].settlement = "settlement"
        self.tiles[11].edges[4].corners[1].ownership = "Player1"
        self.tiles[4].edges[0].corners[1].settlement = "settlement"
        self.tiles[4].edges[0].corners[1].ownership = "Player1"
        self.tiles[6].edges[3].corners[1].settlement = "settlement"
        self.tiles[6].edges[3].corners[1].ownership = "Player2"
        self.tiles[5].edges[3].corners[1].settlement = "settlement"
        self.tiles[5].edges[3].corners[1].ownership = "Player2"
        self.tiles[9].edges[3].corners[1].settlement = "settlement"
        self.tiles[9].edges[3].corners[1].ownership = "Player3"
        self.tiles[0].edges[4].corners[1].settlement = "city"
        self.tiles[0].edges[4].corners[1].ownership = "Player3"
        self.tiles[0].edges[1].corners[1].settlement = "city"
        self.tiles[0].edges[1].corners[1].ownership = "Player4"
    
    def gatherResourceWithSettlement(self, tile, corner):
        resource = tile.resource
        if corner.settlement == "city": 
            quantity = 2;
        elif corner.settlement == "settlement": 
            quantity = 1;
        else:
            quantity = 0;
        if corner.ownership != "none":
            owner = self.getPlayerByName(corner.ownership)
            owner.addResources(resource, quantity)
                
    def getPlayerByName(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return p

    def str(self):
        ret = "Board has the Following Tiles:\n"
        for t in self.tiles:
            ret+=t.str() + "\n"
        return ret

def get_product_sum(num):
    sum = 0
    num += 1
    for i in range(num):
        if (i > 0):
            sum += 6*i
        else:
            sum += 1
    return sum

def setInnerEdges(tiles, corners):
    edge = Edge()
    for i in range(len(tiles)):
        edge.addCorners(corners, tiles[i].relational_id)
        edge.addTile(tiles[i])
        tiles[i].addEdge(edge)
        if (edge.relational_id == ""):
            edge.relational_id += tiles[i].relational_id
        else:
            edge.relational_id += ("-" + tiles[i].relational_id)

def setPerimeterEdges(tile, phantom_tile_id, corners):
    edge = Edge()
    edge.addCorners(corners, phantom_tile_id)
    edge.addCorners(corners, tile.relational_id)
    edge.addTile(tile)
    tile.addEdge(edge)
    edge.relational_id = tile.relational_id + "-" + phantom_tile_id
    if (int(tile.relational_id) % 4 != 0 and int(phantom_tile_id) % 2 == 0):
        edge.port = True

