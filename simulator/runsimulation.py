"""
This module is an example script to show
 how to use the simulation module to run Family Tree Simulation.
"""

import simulation


def parse_arguments():
    pass

def initialize_sim(genes, num_nodes):
    fts = simulation.Simulation(genes = genes)
    fts.initialize_nodestate(num_nodes = num_nodes)
    fts.initialize_randomrelations()
    fts.calculate_statics()
    return fts

def run_simulation(fts, num_steps=100,batch = 100):
    states = []
    for i in range(num_steps):
        state = {
            'node'     : fts.nodes.tolist(),
            'gene_cnt' : fts.gene_cnt.tolist()
        }
        states.append(state)
        print('.', end=' ', flush=True)
        for j in range(batch):
            fts.step_GibbsSampler()
        fts.calculate_statics()
    return states

def save_simulation():
    pass

def main():
    fts    = initialize_sim(2,10)
    states = run_simulation(fts, num_steps = 20, batch=200)
    print(states)

if __name__ == '__main__':
    main()

