"""
 This modules is a collection of Genetic Law.

 For now there is only Mendelic inheritance.
"""
import numpy as np

def prob_mendel(child, father, mother):
    """Mendelic Inheritance.
    calc P(x1|x2,x3)
    """
    combinations = np.sort([ [f,m] for f in father for m in mother],axis=1)
    count_all   = len(combinations)
    count_child = np.sum( np.all( child == combinations , axis = 1) )

    return count_child / count_all


if __name__ == '__main__':
    father = np.array(['A','A'])
    mother = np.array(['B','O'])
    for g1 in ['A','B','O']:
        for g2 in ['A','B','O']:
            child=np.sort([g1,g2])
            print(child,prob_mendel(child, father, mother))
