class MapLoader:
    def __init__(self, map_name = 'map.txt'):
        self.map_name = map_name
        self.rows = self.load()

    def load(self):
        f = open(self.map_name, 'r')
        lines = f.readlines()
        rows = []
        for line in lines:
            row = []
            for i in range(0, len(line), 2):
                c = line[i]
                row.append(c)
            rows.append(row)
        return rows

    def display(self):
        for r in self.rows:
            for c in r:
                print(c, end='-')
            print('')

    def get_entities(self):
        entities = []
        for ir, r in enumerate(self.rows):
            for ic, c in enumerate(r):
                entities.append({
                    'x': ic,
                    'y': ir,
                    'v': c
                })
        return entities

ml = MapLoader('map.txt')
ml.display()
print(ml.get_entities())