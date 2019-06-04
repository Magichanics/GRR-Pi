'''
Author: Jan Garong
'''

import pandas as pd
import matplotlib


class VisualizationFunctions:

    def displacement_graph(self, df, path='temp/displacement_graph.png'):

        from matplotlib import pyplot as plt

        # plot x and y
        plt.plot(df['seconds'], df['displacement'])

        # label axis
        plt.xlabel('Time (seconds)', fontsize=14)
        plt.ylabel('Displacement (decimeters)', fontsize=14)

        # save
        plt.savefig(path)
        plt.close()

    def angle_graph(self, df, path='temp/angle_graph.png'):

        from matplotlib import pyplot as plt

        # plot x and y
        plt.plot(df['seconds'], df['angle'])

        # label axis
        plt.xlabel('Time (seconds)', fontsize=14)
        plt.ylabel('Degrees relative to North', fontsize=14)

        # save
        plt.savefig(path)
        plt.close()

    def graph_items(self, debug_path='temp/debug_log.csv'):
        df = pd.read_csv(debug_path)
        self.displacement_graph(df)
        self.angle_graph(df)

    def __init__(self):
        matplotlib.use("TkAgg")  # prevents errors


VisualizationFunctions()
