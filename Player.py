class Player:
    def __init__(self, name):
        # resources
        self.name = name
        self.num_lumber = 0
        self.num_wool = 0
        self.num_grain = 0
        self.num_brick = 0
        self.num_ore = 0

        # pieces
        self.num_settlements = 5
        self.num_cities = 4
        self.num_roads = 15

        # development cards
        self.dev_cards = []
    
    def addResources(self, resource, quantity):
        if resource == "lumber":
            self.num_lumber += quantity
        elif resource == "wool":
            self.num_wool += quantity
        elif resource == "grain":
            self.num_grain += quantity
        elif resource == "brick":
            self.num_brick += quantity
        elif resource == "ore":
            self.num_ore += quantity
            
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
        return ["Wool: " + str(self.num_wool), "Lumber: " + str(self.num_lumber),"Grain: " + str(self.num_grain), "Brick: " + str(self.num_brick), "Ore: " + str(self.num_ore)]

    def piece_str_list(self):
        return ["Settlements: " + str(self.num_settlements), "Cities: " + str(self.num_cities), "Roads: " + str(self.num_roads)]



