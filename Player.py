class Player:
    def __init__(self, id, name):
        # resources
        self.id = id
        self.name = name
        self.num_lumber = 0
        self.num_wool = 0
        self.num_grain = 0
        self.num_brick = 0
        self.num_ore = 0
        self.num_lumber_buffer = 0
        self.num_wool_buffer = 0
        self.num_grain_buffer = 0
        self.num_brick_buffer = 0
        self.num_ore_buffer = 0

        # pieces
        self.num_settlements = 5
        self.num_cities = 4
        self.num_roads = 15

        # development cards
        self.dev_cards = []
    
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

    def clear_buffer_of_specific_resource(self, resource):
        if resource == "lumber":
            self.num_lumber_buffer = 0
        elif resource == "wool":
            self.num_wool_buffer = 0
        elif resource == "grain":
            self.num_grain_buffer = 0
        elif resource == "brick":
            self.num_brick_buffer = 0
        elif resource == "ore":
            self.num_ore_buffer = 0
    
    def confirm_resource_collection(self):
        self.num_lumber += self.num_lumber_buffer
        self.num_wool += self.num_wool_buffer
        self.num_grain += self.num_grain_buffer
        self.num_brick += self.num_brick_buffer
        self.num_ore += self.num_ore_buffer
        self.num_lumber_buffer = 0
        self.num_wool_buffer = 0
        self.num_grain_buffer = 0
        self.num_brick_buffer = 0
        self.num_ore_buffer = 0
            
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
        return ["Wool: " + str(self.num_wool),
                "Lumber: " + str(self.num_lumber),
                "Grain: " + str(self.num_grain),
                "Brick: " + str(self.num_brick),
                "Ore: " + str(self.num_ore)]

    def piece_str_list(self):
        return ["Settlements: " + str(self.num_settlements),
                "Cities: " + str(self.num_cities),
                "Roads: " + str(self.num_roads)]



