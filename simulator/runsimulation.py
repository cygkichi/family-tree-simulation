"""
This module is an example script to show
 how to use the simulation module to run Family Tree Simulation.
"""
import argparse
import json

import simulation

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="""Run a Family Tree Simulation""")
    parser.add_argument('-n', '--num-nodes',  type=int, default=6)
    parser.add_argument('-g', '--num-genes',  type=int, default=2, help='number of gene')
    parser.add_argument('-s', '--num-steps',  type=int, default=10)
    parser.add_argument('-b', '--batch-size', type=int, default=100)
    parser.add_argument('-o', '--output', type=str, default='result.json')
    args = parser.parse_args()
    return args

def initialize_sim(num_genes, num_nodes):
    """Initialize the simulation."""
    sim = simulation.Simulation(genes = num_genes)
    sim.initialize_nodestate(num_nodes = num_nodes)
    sim.initialize_randomrelations()
    sim.calculate_statics()
    return sim

def run_simulation(sim, num_steps=100,batch_size = 100):
    """Run the simulation for num_steps steps and save quantities."""
    states = [{ 'relations' : sim.relations.tolist() }]
    for i in range(num_steps):
        state = {
            'node'     : sim.nodes.tolist(),
            'gene_cnt' : sim.gene_cnt.tolist()
        }
        states.append(state)
        print('.', end=' ', flush=True)
        for j in range(batch_size):
            sim.step_GibbsSampler()
        sim.calculate_statics()
    return states

def save_simulation(states, filename):
    """Save the simulation result into a json file of given name."""
    with open(filename, 'wt') as f:
        serialized = json.dumps(states, sort_keys=True)
        f.write(serialized)

def main():
    """Run the script"""
    args  = parse_arguments()
    sim   = initialize_sim(args.num_genes, args.num_nodes)
    states = run_simulation(sim, args.num_steps, args.batch_size)
    save_simulation(states, args.output)

if __name__ == '__main__':
    main()

