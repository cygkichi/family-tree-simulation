"""
This module is...
"""
from graphviz import Graph
import json
import argparse
import numpy as np


class Visualizer(object):
    def __init__(self):
        """Initialize the visualization."""
        args = self.parse_arguments()
        self.input  = args.input_json
        with open(self.input,'r') as o:
            self.result = json.load(o)

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-j', '--input-json', type=str, default='./result.json')
        args = parser.parse_args()
        return args

    def vis_family_tree(self):
        G = Graph(format="png")
        num_nodes     = len(self.result['states'][0]['node'])
        num_relations = len(self.result['relations'])
        for i in range(num_nodes):
            if i%2 == 0:
                G.node(str(i), str(i),shape='square')
            else:
                G.node(str(i), str(i),shape='circle')

        for i in range(num_relations):
            G.node(str(i+num_nodes),'',shape='diamond',style='filled',height='0.1',width='0.1')

        for i, rel in enumerate(self.result['relations']):
            c,f,m = rel
            G.edge(str(i+num_nodes),str(c))
            G.edge(str(f),str(i+num_nodes))
            G.edge(str(m),str(i+num_nodes))

        G.render('family-tree')


if __name__ == '__main__':
    vis = Visualizer()
    vis.vis_family_tree()



