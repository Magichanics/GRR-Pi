'''
Author: Matteo Tempo
Date: April 16th, 2019
'''

from mapping import Mapping
from PIL import Image
from PIL import ImageDraw

map_obj = Mapping()
map_obj.create_map(3)

x = len(map_obj.grid[0])
y = len(map_obj.grid)

img = Image.new('RGB', (x*50, y*50), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

for row in range(x):
    for col in range(y):
        draw.rectangle([(row * 50, row * 50 + 49), (col * 50, col * 50 + 49)}, )

for i in range(len(map_obj.grid)):
    print(map_obj.grid[i])

