#!/usr/bin/python

from operator import truediv
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from operator import add
import os
import sys
import shlex

groupsize = 96*4
routersize = 4

def identify_router_of_app(nwid_list, wkld_router_info):
    #get each the group id and router id that belongs to each application

    app_nwid = [int(x) for x in nwid_list]
    app_groupid = [int (x) / groupsize for x in app_nwid] 
    app_ingrouprouterid = [int ((x%groupsize)/ routersize) for x in app_nwid]

    # print "app_nwid:\n"
    # print app_nwid
     # print app1_groupid
    #  print app1_ingrouprouterid
    #  print len(app1_groupid)
    #  print len(app1_ingrouprouterid)

    app_group_router_id = []
    for groupid,routerid in zip(app_groupid, app_ingrouprouterid):
        item = [groupid, routerid]
        if item not in app_group_router_id:#remove dumplicated
            app_group_router_id.append(item)
    #select rows in workload that belongs to each Application
    app_matrix = []
    for row in wkld_router_info:
        for item in app_group_router_id:
            if(row[1] == item[0] and row[2] == item[1]):
                app_matrix.append(row)

    return app_matrix


def sep_app_router_from_wkld(app_name, path, output_info='stats'):
    for subdir in next(os.walk(path))[1]:
        lp_output_folder = os.path.join(path, subdir)
        wkld_router_file = os.path.join(lp_output_folder, 'dragonfly-router-'+output_info)
        #  print wkld_router_file
        # header = open(wkld_router_file, 'r').readline()
        channel_names=['lpid', 'groupid', 'routerid']
        for i in range(0,34):
            channel_names.append("lc"+str(i+1))
        for i in range(0,4):
            channel_names.append("gc"+str(i+1)) 
        # for i in range(0,4):
        #     channel_names.append("tc"+str(i+1))        
        if(output_info=='stats'):
            all_router_data = np.genfromtxt(wkld_router_file, delimiter=None, skip_header=1, names=channel_names)
        else:
            all_router_data = np.genfromtxt(wkld_router_file, delimiter=None, skip_header=0, names=channel_names)
        app_mpi_replay_stats_file = os.path.join(lp_output_folder, app_name+'.csv')
        #  print app_mpi_replay_stats_file
        app_mpi_replay_stats = np.genfromtxt(app_mpi_replay_stats_file, delimiter=None, names=['lpid', 'tid', 'nsend', 'nrecv', 'bytesend', 'byterecv','sendtime', 'commtime', 'comptime', 'jobid'])

        allrouter = all_router_data.view(np.float64).reshape(len(all_router_data), -1)
        app = app_mpi_replay_stats.view(np.float64).reshape(len(app_mpi_replay_stats), -1)
        app_nwid = app[:,1]
        app_router_info = identify_router_of_app(app_nwid, allrouter)

        app_router_info_file = os.path.join(lp_output_folder, app_name+"_router_"+output_info+".csv")
        with open(app_router_info_file, 'w') as outputfile:
            #outputfile.write(header)
            np.savetxt(outputfile, app_router_info, delimiter=" ")


if __name__ == "__main__":
    app = sys.argv[1]
    hasSyn = sys.argv[2]
    subprocess.call(shlex.split("./getappfromwkld.sh "+app+" "+hasSyn))
    # sep_app_router_from_wkld(app, '.', 'traffic')
    sep_app_router_from_wkld(app, '.', 'stats')
    # sep_app_router_from_wkld('MG', '.', 'traffic')
    # sep_app_router_from_wkld('MG', '.', 'stats')
    # sep_app_router_from_wkld('CR', '.', 'traffic')
    # sep_app_router_from_wkld('CR', '.', 'stats')
    if(hasSyn==1):
        # sep_app_router_from_wkld('syn', '.', 'traffic')
        sep_app_router_from_wkld('syn', '.', 'stats')
