#!/usr/bin/python
from operator import truediv
import subprocess
import shlex
import numpy as np
import os
from string import digits

# sort_order1 = {'cont':0 ,'rand_cab':1, 'rand_chas':2, 'rand_rotr':3, 'rand_node':4}
sort_order1 = {'cont':0 ,'rand_cab':1, 'rand_chas':2, 'rand_rotr':3, 'rand':4}
sort_order2 = {'min':0, 'adp':1, 'padp':2}
num_global_channels=1
num_local_channels=34
num_terminal_channels=4

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
        self.msg_maxlatency = []
        self.msg_hopbytes = []
        self.tlink_traffic = []

        self.router_lch_stats =[]
        self.router_gch_stats =[]
        
        self.router_lch_sat = []
        self.router_gch_sat = []

        self.router_lch_load = []
        self.router_gch_load = []

        self.router_lch_traffic = []
        self.router_gch_traffic = []

        self.router_tlink_traffic = []
        self.router_tlink_stats = []

        self.router_traffic = []

    def load_commtime_data(self, path='.'):
        subprocess.call(shlex.split("./getappfromwkld.sh "+self.name+" "+str(self.hasSyn)))
        print 'comm time: '
        # int(x.split("-")[4][1:]), 
        for subdir in sorted(next(os.walk(path))[1], key=lambda x: (sort_order2[x.split("-")[1]] ,sort_order1[x.split("-")[0].translate(None, digits)])):
            print subdir
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.file_name)
            DATA = np.genfromtxt(load_file, delimiter=None, names=['lpid', 'tid', 'nsend', 'nrecv', 'bytesend', 'byterecv','sendtime', 'commtime', 'comptime', 'jobid'])
            self.comm_time_data.append(DATA['commtime']/self.time_scale)
            # print self.comm_time_data

    def load_msg_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_from_wkld.py "+self.name+" "+str(self.hasSyn)))
        # int(x.split("-")[4][1:]),  
        for subdir in sorted(next(os.walk(path))[1], key=lambda x: (sort_order2[x.split("-")[1]] ,sort_order1[x.split("-")[0].translate(None, digits)])):
            output_folder=os.path.join(path, subdir)
            load_file = os.path.join(output_folder, self.name+'-msg-stats.csv')
            DATA = np.genfromtxt(load_file, delimiter=None, names=['lpid', 'tid', 'datasize', 'avglatency', 'packets', 'avghop','busytime', 'maxlatency', 'minlatency'])
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
            
            latency = DATA['avglatency']
            latency[:] = [x/self.time_scale for x in latency]
            self.msg_latency.append(latency)

            # maxlatency = DATA['maxlatency']
            # maxlatency[:] = [x/self.time_scale for x in latency]
            # self.msg_maxlatency.append(latency)
        
        # print self.msg_hopbytes

    def load_router_stats_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_router_info.py "+self.name+" "+str(self.hasSyn)))
        print 'router stats:'
        # int(x.split("-")[4][1:]),  
        for subdir in sorted(next(os.walk(path))[1], key=lambda x: (sort_order2[x.split("-")[1]] ,sort_order1[x.split("-")[0].translate(None, digits)])):
            print subdir
            output_folder=os.path.join(path, subdir)
            if self.name in 'syn':
                load_file = os.path.join(output_folder, 'dragonfly-router-stats')
            else:
                load_file = os.path.join(output_folder, self.name+'_router_stats.csv')
            
            channel_names=['lpid', 'groupid', 'routerid']
            for i in range(0,num_local_channels):
                channel_names.append("lc"+str(i+1))
            for i in range(0,num_global_channels):
                channel_names.append("gc"+str(i+1)) 
            for i in range(0,num_terminal_channels):
                channel_names.append("tc"+str(i+1))   
            DATA = np.genfromtxt(load_file, delimiter=None, names=channel_names)
            data = DATA.view(np.float64).reshape(len(DATA), -1)

            print data[0]

            sum_lch = data[:, 3:3+num_local_channels].sum(axis=1)
            max_lch = data[:, 3:3+num_local_channels].max(axis=1)
            # sum_lch = filter(None, sum_lch)
            sum_lch = [x/self.time_scale for x in sum_lch]
            sorted_sum_lch = np.sort(sum_lch)

            #  yvals = np.arange(len(sorted_sum_lch))/float(len(sorted_sum_lch))
            #  filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            # self.router_lch_stats.append(sorted_sum_lch)

            sum_gch = data[:, 3+num_local_channels:3+num_local_channels+num_global_channels].sum(axis=1)
            max_gch = data[:, 3+num_local_channels:3+num_local_channels+num_global_channels].max(axis=1)
            sum_gch[:] = [x/self.time_scale for x in sum_gch]
            sorted_sum_gch = np.sort(sum_gch)

            # sum_tch = data[:, 47:51].sum(axis=1)
            # sum_tch[:] = [x/self.time_scale for x in sum_tch]
            # sorted_sum_tch = np.sort(sum_tch)
            # self.router_tlink_stats.append(sorted_sum_tch)

            print "max lch: %.5f max gch: %.5f" % (max(max_lch)/self.time_scale, max(max_gch)/self.time_scale)

            self.router_lch_stats.append(sorted_sum_lch)
            self.router_gch_stats.append(sorted_sum_gch)

            lch = list(data[:,3:3+num_local_channels].flat)
            lch = [x/self.time_scale for x in lch]
            gch = list(data[:, 3+num_local_channels:3+num_local_channels+num_global_channels].flat)
            gch = [x/self.time_scale for x in gch]

            # #padding with len(data)
            # if(len(lch) < len(data)):
            #     lch = [0.0]*(len(data)-len(lch)) + lch

            # if(len(gch) < len(data)):
            #     gch = [0.0]*(len(data)-len(gch)) + gch

            # sorted_lch = np.sort(lch)
            # sorted_gch = np.sort(gch)
            self.router_lch_sat.append(lch)
            self.router_gch_sat.append(gch)
            

        # print len(self.router_lch_stats), len(self.router_lch_stats[0])
        # print len(self.router_gch_stats), len(self.router_gch_stats[0])
        # print len(self.router_tlink_stats), len(self.router_tlink_stats[0])

    def make_label(self, path='.'):
        alloc_type=['rand', 'rand_grop', 'rand_rotr', 'rand_chas','rand_cab','cont', 'hyb']
        # alloc_type=['rand', 'cont', 'cons','hyb', 'perm']
        routing_type=['min', 'adp', 'padp', 'nonm']
        app_name=['2pt', '6pt', 'z14pt']
        # routing_type=[]
        # mapping_type=['cons', 'perm', 'rand3d']
        print 'labels: '
        # int(x.split("-")[4][1:]),  
        for subdir in sorted(next(os.walk(path))[1], key=lambda x: (sort_order2[x.split("-")[1]] ,sort_order1[x.split("-")[0].translate(None, digits)])):
            print subdir
            word_array=subdir.split('-')
            tag = ''
            name=''
            payload_size = '-bck'
            for word in word_array:
                if('l' in word):
                    payload_size += word[1:]
                for elem in alloc_type:
                    if elem in word:
                        # if elem == 'rand':
                            # tag += word
                        # else:
                            # tag += elem
                        final = word.translate(None, digits)
                        # final = final.replace("rand_node","rand")
                        final = final.replace("rand_cab","cab")
                        final = final.replace("rand_chas","chas")
                        final = final.replace("rand_rotr","rotr")
                        tag += final
                        tag += '-'
                # for elem in mapping_type:
                #     if elem in word:
                #         tag += word+"-"
                for elem in routing_type:
                    if elem == word:
                        final = word.replace("(","")
                        tag += final+"-"
                # for elem in app_name:
                #     if elem == word:
                #         name +="("+word.replace("z","")+")"
            # tag += payload_size
            # tag += 'adp '+name+'-'
            tag = tag[:-1]
            # tag = payload_size[1:]
            self.xlabel.append(tag)
        #  print self.xlabel

    def load_router_traffic_data(self, path='.'):
        subprocess.call(shlex.split("./sep_app_router_info.py "+self.name+" "+str(self.hasSyn)))
        index = 0
        print 'traffic: '
        # int(x.split("-")[4][1:]),  
        for subdir in sorted(next(os.walk(path))[1], key=lambda x: (sort_order2[x.split("-")[1]] ,sort_order1[x.split("-")[0].translate(None, digits)])):
            print subdir
            output_folder=os.path.join(path, subdir)
            if self.name in 'syn':
                load_file = os.path.join(output_folder, 'dragonfly-router-traffic')
            else:
                load_file = os.path.join(output_folder, self.name+'_router_traffic.csv')
            
            channel_names=['lpid', 'groupid', 'routerid']
            for i in range(0,num_local_channels):
                channel_names.append("lc"+str(i+1))
            for i in range(0,num_global_channels):
                channel_names.append("gc"+str(i+1)) 
            for i in range(0,num_terminal_channels):
                channel_names.append("tc"+str(i+1))

            DATA = np.genfromtxt(load_file, delimiter=None, names=channel_names)
            data = DATA.view(np.float64).reshape(len(DATA), -1)

            # data[:] = [0.0 for y in data for x in y if x > 9999999999]
            # for x in range(0,len(data)):
            #     for y in range(0, len(data[x])):
            #         if (self.name=='amg' and data[x,y] > 999999):
            #             # print data[x,y]
            #             data[x,y] = 0.0

            sum_lch = data[:, 3:3+num_local_channels].sum(axis=1)
            #  sum_lch = filter(None, sum_lch)
            sum_lch = [x/self.data_scale for x in sum_lch]
            sorted_sum_lch = np.sort(sum_lch)
            #  yvals = np.arange(len(sorted_sum_lch))/float(len(sorted_sum_lch))
            filtered_sorted_sum_lch=filter(None, sorted_sum_lch)
            self.router_lch_traffic.append(filtered_sorted_sum_lch)
            # np.savetxt("router_lch_traffic.csv", filtered_sorted_sum_lch, delimiter=",")
            sum_gch = data[:, 3+num_local_channels:3+num_local_channels+num_global_channels].sum(axis=1)
            sum_gch[:] = [x/self.data_scale for x in sum_gch]
            sorted_sum_gch = np.sort( sum_gch )
            self.router_gch_traffic.append(sorted_sum_gch)

            lch = list(data[:,3:3+num_local_channels].flat)
            lch = [x/self.time_scale for x in lch]
            gch = list(data[:, 3+num_local_channels:3+num_local_channels+num_global_channels].flat)
            gch = [x/self.time_scale for x in gch]
            # sorted_lch = np.sort(lch)
            # sorted_gch = np.sort(gch)
            self.router_lch_load.append(lch)
            self.router_gch_load.append(gch)

            # sum_tch = data[:, 47:51].sum(axis=1)
            # sum_tch[:] = [x/self.data_scale for x in sum_tch]
            # sorted_sum_tch = np.sort( sum_tch )
            # self.router_tlink_traffic.append(sorted_sum_tch)
            # np.savetxt("router_gch_traffic.csv", sorted_sum_gch, delimiter=",")
            # avg_comm_time = sum(self.comm_time_data[index])/len(self.comm_time_data[index])
            # avg_lch_traffic = 8*sum(filtered_sorted_sum_lch)/len(filtered_sorted_sum_lch)/avg_comm_time/1000
            # avg_gch_traffic = 8*sum(sorted_sum_gch)/len(sorted_sum_gch)/avg_comm_time/1000
            # print subdir+":"
            # print str(avg_lch_traffic) + "\t" + str(avg_gch_traffic)
            index += 1;

        # print len(self.router_lch_load), len(self.router_lch_load[0])
        # print len(self.router_gch_traffic), len(self.router_gch_traffic[0])

