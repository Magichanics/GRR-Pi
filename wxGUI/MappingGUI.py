'''
Author: Jan Garong
Thursday May 28th, 2019
'''
from mappingtools.Mapping import Mapping
from mappingtools import PathFinding as pf

# p1 and p2 are tuple coordinates (x, y)
def plot_graph(p1, p2):

    # convert coordinates to indices.
    mp = Mapping()
    mp.read_mppy('temp/map.txt')
    pi, pj = mp.get_index(p1)
    li, lj = mp.get_index(p2)

    # convert coordinates to indices (reversed coords)
    pf.main((pi, pj), (li, lj), save_path='temp/map_path.png')
