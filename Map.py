class Map():
    def __init__(self, dimensions, entities):
        self.dimensions = dimensions
        self.entities = entities
        self.map_data = []
        for y in range(self.dimensions.height):
            row = []
            for x in range(self.dimensions.width):
                if (x == self.dimensions.width - 1) or (x == 0) or (y == 0) or (y == self.dimensions.height - 1):
                    row.append('#')
                else:
                    row.append('.')
            self.map_data.append(row)

    # def place_entity(self, entity, coord='random'):
    #     if coord == 'random':
    #         coord_list = []
    #         for r in range(len(self.data)):
    #             for c in range(len(self.data[r])):
    #                 if self.data[r][c] == '.':
    #                     coord_list.append((c, r))
    #         coord = choice(coord_list)
    #     x, y = coord
    #     self.data[y][x] = entity
    #     return coord 
    
    def __str__(self):
        for e in self.entities:
            self.map_data[e.position.y][e.position.x] = e.graphic
        text = '\n'
        for r in self.map_data:
            for c in r:
                text += c + ' '
            text += '\n'
        return text

    # def __repr__(self):
    #     for x in self.layout:
    #         str(x)

    # def __str__(self):