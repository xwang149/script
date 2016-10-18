#!/usr/bin/python
from operator import truediv
import subprocess
import numpy as np
import os

class WorkLoad(object):
    def __init__(self, time_scale=1000000,\
                data_scale=1000*1000):
        self.time_scale = time_scale # convert time in non-sec to milli-sec
        self.data_scale = data_scale # convert data in Byte to MB
        self.xlabel=[]
        self.make_label('.')

        self.Tlink_busytime= []
        self.msg_avg_hop = []
        self.msg_latency = []
        self.Tlink_traffic = []

        self.router_lch_stats =[]
        self.router_gch_stats =[]

        self.router_lch_traffic = []
        self.router_gch_traffic = []

    def make_label(self, path='.'):
        alloc_type=['cont', 'rand', 'hyb']
        routing_type=['min', 'adp', 'padp','dfly_adp', 'dfly_min']
        for subdir in sorted(next(os.walk(path))[1]):
            word_array=subdir.split('-')
            tag = ''
            for word in word_array:
                if word in alloc_type:
                    tag += word
                    tag += '-'
                elif word in routing_type:
                    tag += word
            self.xlabel.append(tag)
        #  print self.xlabel


    def load_msg_data(self, path='.'):
        for subdir in sorted(next(os.walk(path))[1]):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, 'dragonfly-msg-stats')
            DATA = np.genfromtxt(load_file, delimiter=None, names=['lpid', 'tid', 'datasize', 'time','packets', 'avghop', 'busytime'])
            busytime = filter(None, DATA['busytime'])
            #  busytime.sort()
            busytime[:] = [x/self.time_scale for x in busytime]
            self.Tlink_busytime.append(busytime)
            avghop = DATA['avghop']
            #  avghop.sort()
            self.msg_avg_hop.append( avghop)

            #  traffic = filter(None, DATA['datasize'])
            traffic = DATA['datasize']
            traffic[:] = [x/self.data_scale for x in traffic]
            self.Tlink_traffic.append(traffic)

            num_packet = filter(None, DATA['packets'])
            total_time = filter(None, DATA['time'])
            total_time[:] = [x/self.time_scale for x in total_time]
            latency = map(truediv, total_time, num_packet)
            self.msg_latency.append(latency)

    def load_router_stats_data(self, path='.'):
        for subdir in sorted(next(os.walk(path))[1]):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, 'dragonfly-router-stats')
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
            filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            self.router_lch_stats.append(filtered_sorted_sum_lch)

            sum_gch = data[:, 11:].sum(axis=1)
            sum_gch[:] = [x/self.time_scale for x in sum_gch]
            sorted_sum_gch = np.sort( sum_gch )
            self.router_gch_stats.append(sorted_sum_gch)

        print len(self.router_lch_stats), len(self.router_lch_stats[0])
        print len(self.router_gch_stats), len(self.router_gch_stats[0])



    def load_router_traffic_data(self, path='.'):
        for subdir in sorted(next(os.walk(path))[1]):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, 'dragonfly-router-traffic')
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

        print len(self.router_lch_traffic), len(self.router_lch_traffic[0])
        print len(self.router_gch_traffic), len(self.router_gch_traffic[0])

