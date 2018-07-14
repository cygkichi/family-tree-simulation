"""
This module includes the Family Tree class simulation.
"""
import numpy as np
import geneticlaw as gl

class Simulation(object):
    """Main simulation class.
    """
    def __init__(self, random_seed=None, genes=2):
        """Initialize the simulation.

        :param random_seed: random seed to be able to run the same simulation
        :param ngene: number of the gene
        """
        # environment
        self.genes = genes
        self.state_list = np.array([[i,j] for i in range(genes) for j in range(i,genes)])

        # nodes, state
        self.num_nodes = None
        self.nodes     = None
        self.relations = None
        self.genes_cnt = None


        # setup
        if random_seed is not None:
            np.random.seed(random_seed)

    def initialize_nodestate(self, num_nodes=5):
        """Initialize the node state
        """
        self.num_nodes = num_nodes
        common_gene = [0,1]
        self.nodes  = np.tile(common_gene,(num_nodes,1))

    def initialize_randomrelations(self, rate=0.5):
        """Initialize the relations [c,f,m]
        :param rante: pass
        """
        relations = [[2,0,1]]
        i = 3
        while i < self.num_nodes:
            p = np.random.rand()
            if p < rate and self.num_nodes - i != 1:
                #new node is parents
                if i%2 == 0:
                    wife_index    = np.random.choice(np.arange(1,i,2)[np.arange(1,i,2)>i-10])
                    relations.append([i+1, i, wife_index])
                else:
                    husband_index = np.random.choice(np.arange(0,i,2)[np.arange(0,i,2)>i-10])
                    relations.append([i+1, husband_index, i])
                i += 2
            else:
                #new node is child
                father_index = np.random.choice(np.arange(0,i,2)[np.arange(0,i,2)>i-10])
                mother_index = np.random.choice(np.arange(1,i,2)[np.arange(1,i,2)>i-10])
                relations.append([i, father_index, mother_index])
                i += 1
        self.relations = np.array(relations)

    def calculate_statics(self):
        self.gene_cnt = np.array([np.sum(np.all(self.nodes == gene, axis=1)) for gene in self.state_list])

    def child_indexs(self):
        """Return list of child index
        """
        return self.relations[:,0]

    def step_GibbsSampler(self):
        """Step forward the dynamic simulation via Gibbs Sampler
        """
        target_index = np.random.randint(0, self.num_nodes)
        use_relations = self.relations[ [target_index in rel for rel in self.relations] ]

        ps = []
        for replace_gene in self.state_list:
            replaced_relations = np.where( target_index == use_relations, -1, use_relations)
            tmp_nodes = np.append(self.nodes, [replace_gene], axis=0)
            xs  = tmp_nodes[replaced_relations]
            tmp = np.prod([gl.prob_mendel(x[0],x[1],x[2])for x in xs])
            ps   = np.append(ps, tmp)

        ps = ps / ps.sum()
        replacing_node = self.state_list[np.random.choice(len(self.state_list), 1, p=ps)]
        self.nodes[target_index] = replacing_node


if __name__ == '__main__':
    sim = Simulation()
    sim.initialize_nodestate(num_nodes=20)
    sim.initialize_randomrelations()
    sim.calculate_statics()
    print(sim.relations.tolist())
    print(sim.nodes.tolist())
    print(sim.gene_cnt.tolist())
    print(" .......... .......... ")
    for i in range(100):
        sim.step_GibbsSampler()
    sim.calculate_statics()
    print(sim.nodes.tolist())
    print(sim.gene_cnt.tolist())
    print(" .......... .......... ")
    for i in range(100):
        sim.step_GibbsSampler()
    sim.calculate_statics()
    print(sim.nodes.tolist())
    print(sim.gene_cnt.tolist())
    print(" .......... .......... ")
    for i in range(100):
        sim.step_GibbsSampler()
    sim.calculate_statics()
    print(sim.nodes.tolist())
    print(sim.gene_cnt.tolist())
    print(" .......... .......... ")
