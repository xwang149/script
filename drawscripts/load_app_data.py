#!/usr/bin/python
from operator import truediv
import subprocess
import shlex
import numpy as np
import os

class APP(object):
    def __init__(self, name, color, syn,\
                time_scale=1000000,\
                data_scale=1024*1024):
        self.name = name
        self.color = color[0]
        self.med_color = color[1]
        self.hasSyn = syn
        self.time_scale = time_scale # convert time in non-sec to milli-sec
        self.data_scale = data_scale # convert data in Byte to MB
        self.file_name=name+'.csv'
        self.xlabel=[]
        self.make_label('.')

        self.comm_time_data = []

        self.msg_busytime = []
        self.msg_avg_hop = []
        self.msg_latency = []
        self.tlink_traffic = []

        self.router_lch_stats =[]
        self.router_gch_stats =[]

        self.router_lch_traffic = []
        self.router_gch_traffic = []

    def load_commtime_data(self, path='.'):
        subprocess.call(shlex.split("./getappfromwkld.sh "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: int(x[x.find("-l")+2:x.find("-i")])):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.file_name)
            DATA = np.genfromtxt(load_file, delimiter=None, names=['App', 'appid', 'RANK', 'rankid','lpid', 'nwid', 'nsend', 'nrecv', 'bytesend', 'byterecv','sendtime', 'commtime', 'comptime'])
            self.comm_time_data.append(DATA['commtime']/self.time_scale)
            #  print DATA['commtime'][0:10]

    def load_msg_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_from_wkld.py "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: int(x[x.find("-l")+2:x.find("-i")])):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.name+'-msg-stats.csv')
            DATA = np.genfromtxt(load_file, delimiter=None, names=['lpid', 'tid', 'datasize', 'avgpacketlatency','packets', 'avghop', 'busytime'])
            #  busytime = filter(None, DATA['busytime'])
            busytime = DATA['busytime']
            #  busytime.sort()
            busytime[:] = [x/self.time_scale for x in busytime]
            self.msg_busytime.append(busytime)
            avghop = DATA['avghop']
            #  avghop.sort()
            self.msg_avg_hop.append( avghop)

            tlink_traffic = DATA['datasize']
            tlink_traffic[:] = [x/self.data_scale for x in tlink_traffic]
            self.tlink_traffic.append(tlink_traffic)

            latency = DATA['avgpacketlatency']
            latency[:] = [x/self.time_scale for x in latency]
            self.msg_latency.append(latency)


    def load_router_stats_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_router_info.py "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: int(x[x.find("-l")+2:x.find("-i")])):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.name+'_router_stats.csv')
            DATA = np.genfromtxt(load_file, delimiter=None,\
                    names=['lpid', 'groupid', 'routerid', 'lc1',\
                    'lc2', 'lc3', 'lc4', 'lc5', 'lc6'\
                    'lc7', 'lc8', 'gc1', 'gc2', 'gc3', 'gc4'])
            data = DATA.view(np.float64).reshape(len(DATA), -1)
            sum_lch = data[:, 3:11].sum(axis=1)
            #  sum_lch = filter(None, sum_lch)
            sum_lch = [x/self.time_scale for x in sum_lch]
            sorted_sum_lch = np.sort(sum_lch)
            #  yvals = np.arange(len(sorted_sum_lch))/float(len(sorted_sum_lch))
            #  filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            self.router_lch_stats.append(sorted_sum_lch)

            sum_gch = data[:, 11:].sum(axis=1)
            sum_gch[:] = [x/self.time_scale for x in sum_gch]
            sorted_sum_gch = np.sort( sum_gch )
            self.router_gch_stats.append(sorted_sum_gch)

        print len(self.router_lch_stats), len(self.router_lch_stats[0])
        print len(self.router_gch_stats), len(self.router_gch_stats[0])


    def make_label(self, path='.'):
        alloc_type=['rand_node', 'rand_grop', 'rand_rotr', 'cont', 'hyb']
        # alloc_type=['rand', 'cont', 'cons','hyb', 'perm']
        #  routing_type=['min', 'adp', 'padp']
        # routing_type=[]
        mapping_type=['cons', 'perm']
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: int(x[x.find("-l")+2:x.find("-i")])):
            print subdir
            word_array=subdir.split('-')
            tag = ''
            payload_size = '-msg'
            for word in word_array:
                if('l' in word):
                    payload_size += word[1:]
                for elem in alloc_type:
                    if elem in word:
                        if elem == 'rand':
                            tag += word
                        else:
                            tag += elem 
                        tag += '-'
                if word in mapping_type:
                    tag += word
            tag += payload_size
            tag = tag[:-1]
            self.xlabel.append(tag)
        #  print self.xlabel


    def load_router_traffic_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_router_info.py "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: int(x[x.find("-l")+2:x.find("-i")])):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.name+'_router_traffic.csv')
            DATA = np.genfromtxt(load_file, delimiter=None,\
                    names=['lpid', 'groupid', 'routerid', 'lc1',\
                    'lc2', 'lc3', 'lc4', 'lc5', 'lc6'\
                    'lc7', 'lc8', 'gc1', 'gc2', 'gc3', 'gc4'])
            data = DATA.view(np.float64).reshape(len(DATA), -1)
            sum_lch = data[:, 3:11].sum(axis=1)
            #  sum_lch = filter(None, sum_lch)
            sum_lch = [x/self.data_scale for x in sum_lch]
            sorted_sum_lch = np.sort(sum_lch)
            #  yvals = np.arange(len(sorted_sum_lch))/float(len(sorted_sum_lch))
            filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            self.router_lch_traffic.append(filtered_sorted_sum_lch)

            sum_gch = data[:, 11:].sum(axis=1)
            sum_gch[:] = [x/self.data_scale for x in sum_gch]
            sorted_sum_gch = np.sort( sum_gch )
            self.router_gch_traffic.append(sorted_sum_gch)

        #  print len(self.router_lch_traffic), len(self.router_lch_traffic[0])
        #  print len(self.router_gch_traffic), len(self.router_gch_traffic[0])
