#!/usr/bin/python
from operator import truediv
import subprocess
import shlex
import numpy as np
import os

class APP(object):
    def __init__(self, name, prefix, color, syn,\
                time_scale=1000000,\
                data_scale=1024*1024):
        self.name = name
        self.prefix = prefix
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
        self.msg_hopbytes = []
        self.tlink_traffic = []

        self.router_lch_stats =[]
        self.router_gch_stats =[]

        self.router_lch_traffic = []
        self.router_gch_traffic = []

        self.router_traffic = []

    def load_commtime_data(self, path='.'):
        subprocess.call(shlex.split("./getappfromwkld.sh "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: ( int(x[x.find("-l")+2:x.find("-i")]), x[0:x.find("-"+self.name)] )):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.file_name)
            DATA = np.genfromtxt(load_file, delimiter=None, names=['App', 'appid', 'RANK', 'rankid','lpid', 'nwid', 'nsend', 'nrecv', 'bytesend', 'byterecv','sendtime', 'commtime', 'comptime'])
            self.comm_time_data.append(DATA['commtime']/self.time_scale)
            #  print DATA['commtime'][0:10]

    def load_msg_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_from_wkld.py "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: ( int(x[x.find("-l")+2:x.find("-i")]), x[0:x.find("-"+self.name)] )):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.name+'-msg-stats.csv')
            DATA = np.genfromtxt(load_file, delimiter=None, names=['lpid', 'tid', 'datasize', 'avgpacketlatency','packets', 'avghop', 'busytime'])
            #  busytime = filter(None, DATA['busytime'])
            busytime = DATA['busytime']
            #  busytime.sort()
            busytime[:] = [x/self.time_scale for x in busytime]
            #busytime[:] = [x for x in busytime]
            self.msg_busytime.append(busytime)
            avghop = DATA['avghop']
            #  avghop.sort()
            self.msg_avg_hop.append( avghop)

            tlink_traffic = DATA['datasize']
            tlink_traffic[:] = [x/self.data_scale for x in tlink_traffic]
            self.tlink_traffic.append(tlink_traffic)
            
            # estimate hopbytes (MB)
            tlink_hopbytes = [avghop[i] * tlink_traffic[i] for i in range(len(avghop))]
            sum_hopbytes = sum(tlink_hopbytes)
            self.msg_hopbytes.append(sum_hopbytes)
            
            latency = DATA['avgpacketlatency']
            latency[:] = [x/self.time_scale for x in latency]
            self.msg_latency.append(latency)
        
        print self.msg_hopbytes


    def load_router_stats_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_router_info.py "+self.name+" "+str(self.hasSyn)))
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: ( int(x[x.find("-l")+2:x.find("-i")]), x[0:x.find("-"+self.name)] )):
            output_folder=os.path.join(path, subdir)
            if self.name in 'syn':
                load_file = os.path.join(output_folder, 'dragonfly-router-stats')
            else:
                load_file = os.path.join(output_folder, self.name+'_router_stats.csv')
            
            channel_names=['lpid', 'groupid', 'routerid']
            for i in range(0,34):
                channel_names.append("lc"+str(i+1))
            for i in range(0,10):
                channel_names.append("gc"+str(i+1)) 
            for i in range(0,4):
                channel_names.append("tc"+str(i+1))   

            DATA = np.genfromtxt(load_file, delimiter=None, names=channel_names)
            data = DATA.view(np.float64).reshape(len(DATA), -1)
            sum_lch = data[:, 3:37].sum(axis=1)
            #  sum_lch = filter(None, sum_lch)
            sum_lch = [x/self.time_scale for x in sum_lch]
            sorted_sum_lch = np.sort(sum_lch)
            #  yvals = np.arange(len(sorted_sum_lch))/float(len(sorted_sum_lch))
            #  filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            self.router_lch_stats.append(sorted_sum_lch)
            # print data[0, 99:]
            sum_gch = data[:, 37:47].sum(axis=1)
            sum_gch[:] = [x/self.time_scale for x in sum_gch]
            sorted_sum_gch = np.sort( sum_gch )
            self.router_gch_stats.append(sorted_sum_gch)

        # print len(self.router_lch_stats), len(self.router_lch_stats[0])
        # print len(self.router_gch_stats), len(self.router_gch_stats[0])


    def make_label(self, path='.'):
        alloc_type=['rand_node', 'rand_grop', 'rand_rotr', 'rand_chassis','rand_cabinet','cont', 'hyb', 'randCab']
        # alloc_type=['rand', 'cont', 'cons','hyb', 'perm']
        routing_type=['(min', 'adp', 'padp']
        # routing_type=[]
        # mapping_type=['cons', 'perm', 'rand3d']
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: ( int(x[x.find("-l")+2:x.find("-i")]), x[0:x.find("-"+self.name)] )):
            print subdir
            word_array=subdir.split('-')
            tag = ''
            payload_size = '-msg'
            for word in word_array:
                if('l' in word):
                    payload_size += word[1:]
                for elem in alloc_type:
                    if elem in word:
                        # if elem == 'rand':
                            # tag += word
                        # else:
                            # tag += elem
                        tag += word
                        tag += '-'
                # for elem in mapping_type:
                #     if elem in word:
                #         tag += word+"-"
                for elem in routing_type:
                    if elem == word:
                        tag += word.replace("(","")+"-"
            # tag += payload_size
            tag = tag[:-1]
            # tag = payload_size[1:]
            self.xlabel.append(tag)
        #  print self.xlabel


    def load_router_traffic_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_router_info.py "+self.name+" "+str(self.hasSyn)))
        index = 0
        for subdir in sorted(next(os.walk(path))[1], key = lambda x: ( int(x[x.find("-l")+2:x.find("-i")]), x[0:x.find("-"+self.name)] )):
            output_folder=os.path.join(path, subdir)
            if self.name in 'syn':
                load_file = os.path.join(output_folder, 'dragonfly-router-traffic')
            else:
                load_file = os.path.join(output_folder, self.name+'_router_traffic.csv')
            
            channel_names=['lpid', 'groupid', 'routerid']
            for i in range(0,34):
                channel_names.append("lc"+str(i+1))
            for i in range(0,10):
                channel_names.append("gc"+str(i+1)) 
            for i in range(0,4):
                channel_names.append("tc"+str(i+1))

            DATA = np.genfromtxt(load_file, delimiter=None, names=channel_names)
            data = DATA.view(np.float64).reshape(len(DATA), -1)
            sum_lch = data[:, 3:37].sum(axis=1)
            #  sum_lch = filter(None, sum_lch)
            sum_lch = [x/self.data_scale for x in sum_lch]
            sorted_sum_lch = np.sort(sum_lch)
            #  yvals = np.arange(len(sorted_sum_lch))/float(len(sorted_sum_lch))
            filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            self.router_lch_traffic.append(filtered_sorted_sum_lch)
            # np.savetxt("router_lch_traffic.csv", filtered_sorted_sum_lch, delimiter=",")
            sum_gch = data[:, 37:47].sum(axis=1)
            sum_gch[:] = [x/self.data_scale for x in sum_gch]
            sorted_sum_gch = np.sort( sum_gch )
            self.router_gch_traffic.append(sorted_sum_gch)
            # np.savetxt("router_gch_traffic.csv", sorted_sum_gch, delimiter=",")
            # avg_comm_time = sum(self.comm_time_data[index])/len(self.comm_time_data[index])
            # avg_lch_traffic = 8*sum(filtered_sorted_sum_lch)/len(filtered_sorted_sum_lch)/avg_comm_time/1000
            # avg_gch_traffic = 8*sum(sorted_sum_gch)/len(sorted_sum_gch)/avg_comm_time/1000
            # print subdir+":"
            # print str(avg_lch_traffic) + "\t" + str(avg_gch_traffic)
            index += 1;

        # print len(self.router_lch_traffic), len(self.router_lch_traffic[0])
        # print len(self.router_gch_traffic), len(self.router_gch_traffic[0])

