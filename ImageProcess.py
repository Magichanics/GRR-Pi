'''
Author: Matteo Tempo
Date: April 16th, 2019
'''

from Mapping import Mapping
from PIL import Image
from PIL import ImageDraw


class ImageProcess:
    # makes grid image
    def make_grid_image(self, map_obj):
        x = len(map_obj.grid[0])
        y = len(map_obj.grid)

        img = Image.new('RGB', (x * 50, y * 50), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        fill_colour = ""
        for row in range(x):
            for col in range(y):
                if map_obj.grid[col][row] == "R":
                    fill_colour = "black"
                elif map_obj.grid[col][row] == "r":
                    fill_colour = "red"
                elif map_obj.grid[col][row] == "g":
                    fill_colour = "green"
                else:
                    fill_colour = "white"
                draw.rectangle([(row * 50, col * 50), (row * 50 + 49, col * 50 + 49)], fill=fill_colour, outline="black")

        img.save("rectangle.png")
