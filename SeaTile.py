from Tile import Tile


class SeaTile(Tile):
    def __init__(self, coordinates, tile_aggregate, port_type, port_direction):
        super().__init__(coordinates, tile_aggregate)
        self.set_port_of_edge(port_type, port_direction)

    def set_port_of_edge(self, port_type, port_direction):
        if port_direction is not None:
            self.edges[port_direction].port = port_type
