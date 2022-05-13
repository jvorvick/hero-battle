f = open('map.txt', 'r')
lines = f.readlines()
rows = []
for line in lines:
    row = []
    for i in range(0, len(line), 2):
        c = line[i]
        row.append(c)
    rows.append(row)
print(rows)

for r in rows:
    for c in r:
        print(c, end='-')
    print('')

entities = []
for ir, r in enumerate(rows):
    for ic, c in enumerate(r):
        entities.append({
            'x': ic,
            'y': ir,
            'v': c
        })
print(entities)