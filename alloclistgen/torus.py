import random
from enum import Enum

class Torus(object):
    def __init__(self, network_dim, alloc_type, job_rank, num_seed):
        self.dim = network_dim
        self.total_node = 1
        for item in self.dim:
            self.total_node *= item 
        self.job_rank = job_rank
        self.alloc_type = alloc_type
        self.num_seed = num_seed
        self.alloc_file_prefix()
        self.load_alloc()

    def alloc_file_prefix(self):
        self.alloc_file = "torus-"+self.alloc_type+'-alloc-'+str(self.total_node)+'-'
        for jobsize in self.job_rank:
            self.alloc_file += str(jobsize)+'_'
        self.alloc_file = self.alloc_file[:-1]

    def load_alloc(self):
        if self.alloc_type == 'cont':
            print "this is torus cont alloc"
            self.cont_alloc()
        elif self.alloc_type == 'rand':
            print "Torus "+ self.alloc_type + " Allocation!"
            self.random_alloc()
        elif self.alloc_type == 'hyb':
            print "Torus"+ self.alloc_type + " Allocation!"
            self.hybrid_alloc()
        else:
            print self.alloc_type +" Function Not Supported Yet!"
            exit()

    def random_alloc(self):
        chunk_size = 1
        #  chunk_size is the num of consecutive nodes 
        #  if self.alloc_type == 'rand_router':
            #  #  chunk_size equals to num of nodes attached to a router 
            #  chunk_size = self.num_router/2
        #  elif self.alloc_type == 'rand_group':
            #  #  chunk_size equals to num of nodes in each group 
            #  chunk_size = self.num_router * self.num_router/2
        #  elif self.alloc_type == 'rand_node':
            #  chunk_size = 1
        for seed in range(self.num_seed):
            self.alloc_file += '-'+str(seed)
            #print self.alloc_file
            f = open(self.alloc_file+'.conf', 'w')
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            for rank in self.job_rank:
                #each job needs 'num_chunk' of nodes
                num_chunk = rank/chunk_size if rank%chunk_size == 0 else (rank/chunk_size)+1
                alloc_list = []
                for i in range(num_chunk):
                    idx = random.randint(0, len(node_list)-chunk_size)
                    alloc_list += node_list[idx:idx+chunk_size]
                    node_list = [elem for elem in node_list if (elem not in alloc_list)]
                #  print alloc_list[0:rank]
                for idx in range(rank):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file=self.alloc_file[:-2]


    def cont_alloc(self):
        print self.total_node
        f = open(self.alloc_file+".conf", 'w')
        start = 0
        for num_rank in self.job_rank:
            for rankid in range(start, start+ num_rank):
                f.write("%s " % rankid)
            f.write("\n")
            start += num_rank
        f.closed


    def hybrid_alloc(self):
        #  the first 'cont_job_num' jobs get contiguous allocation 
        #  the other job get random allocation
        cont_job_num = 2
        for seed in range(self.num_seed):
            self.alloc_file += '-'+str(seed)
            f = open(self.alloc_file+'.conf', 'w')
            node_list = range(0, int(self.total_node))
            random.seed(seed)
            for rankid in range(len(self.job_rank)):
                if(rankid < cont_job_num ):
                    job_size = self.job_rank[rankid]
                    alloc_list = node_list[0: job_size]
                    node_list = node_list[job_size: ]
                else:
                    alloc_list = random.sample(node_list, self.job_rank[rankid])
                node_list = [i for i in node_list if (i not in alloc_list)]
                for idx in range(len(alloc_list)):
                    f.write("%s " % alloc_list[idx])
                f.write("\n")
            f.closed
            self.alloc_file=self.alloc_file[:-2]


