from torus import Torus 
from dragonfly import Dragonfly

'''
jobrank_list specifies the number of ranks of each job
'''
jobrank_list = [27, 10]

'''
The way to generate allocation list on Dragonfly:

    Dragonfly(num.router, num.group, alloc_function, jobrank_list, num.random_seed)

'''
#  Dragonfly(8, 33, 'cont', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_router', jobrank_list, 1)
#  Dragonfly(8, 33, 'rand_group', jobrank_list, 1)
Dragonfly(4, 9, 'rand_node', jobrank_list, 10)
#  Dragonfly(8, 33, 'hyb', jobrank_list, 3)
 
'''
The way to generate allocation list on Dragonfly:

    Torus(torus_dimesion_vector, alloc_function, jobrank_list, num.random_seed)

'''  
jobrank_list = [10, 5, 10]
torus_dim = [8, 16, 16]
#  Torus(torus_dim, 'cont', jobrank_list, 3)
#  Torus(torus_dim, 'rand', jobrank_list, 3)
#  Torus(torus_dim, 'hyb', jobrank_list, 3)

