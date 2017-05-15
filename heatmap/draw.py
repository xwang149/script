#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import itertools
import math

NUM_BINS=400
RADIX=48
LChannel=34
GChannel=10
Terminal=4
label_size = 25

def readMPI(file_name):

    mpi_op = {}
    mpi_op["src"]=[]
    mpi_op["dst"]=[]
    mpi_op["time"]=[]
    mpi_op["msg_sz"]=[]

    wlf = open("mpi-op-logs-"+file_name, "r")
    z = [ [ 0.0 for y in range( rank ) ] for x in range( rank ) ]
    count = 0
    count1 = 0
    count2 = 0
    count3 = 0
    for line in wlf:
        line = line.strip('\n')
        line = line.strip('\r')
        if len(line)==0:
            continue
        if ")" in line:
            temp = line.split()
            end_time = float(temp[0][1:-1])
        if "SEND" not in line:
            continue
        parts = line.split()
        if "ID" in line:
            src_rank = int(parts[7])
            dst_rank = int(parts[9])
            msg_size = float(parts[13])/1024.0/1024.0 
        else:
            src_rank = int(parts[6])
            dst_rank = int(parts[8])
            msg_size = float(parts[12])/1024.0/1024.0            
        time = float(parts[0][1:-1])
        mpi_op["src"].append(src_rank)
        mpi_op["dst"].append(dst_rank)
        mpi_op["msg_sz"].append(msg_size)
        mpi_op["time"].append(time)
        z[dst_rank][src_rank] += msg_size
        count += 1

        chas_id1 = src_rank / 64
        chas_id2 = dst_rank / 64
        cab1 = src_rank / 192
        cab2 = dst_rank / 192
        grop1 = src_rank / 384
        grop2 = dst_rank / 384
        if (chas_id1 != chas_id2):
            count1 += 1
        if (cab1 != cab2):
            count2 += 1
        if (grop1 != grop2):
            count3 += 1

    print "Total sends: %d, cross group: %d, cross chas: %d, cross cab: %d" %(count, count3, count1, count2)

    wlf.close()
    return mpi_op, z, end_time

def drawHeatmap(rank, prefix, z):
    #plot heat map
    x = range(rank)
    y = range(rank)
    x, y = np.meshgrid(x, y)

    z = np.array(z)
    # print z

    #plot heatmap
    fig = plt.figure(10)
    ax = fig.add_subplot(111)
    ax.set_xlabel('MPI_ranks',fontsize = label_size)
    ax.set_ylabel('MPI_ranks',fontsize = label_size)
    ax.set_xlim([0, rank])
    ax.set_ylim([0, rank])
    # plt.pcolormesh(x, y, z)
    plt.pcolormesh(x, y, z, cmap=plt.cm.Greys)
    plt.colorbar() #need a colorbar to show the intensity scale
    title = prefix +'_Communication_Topology'
    # plt.title(title, fontsize = label_size)
    plt.yticks(fontsize = label_size)
    plt.xticks(fontsize = label_size)
    # plt.locator_params(axis='x', nbins=7)
    plt.tight_layout()
    plt.savefig('./'+title+'.png', format='png', dpi=1000)
    plt.close(fig)

def drawMsgmap(prefix, mpi_op, time_interval, end_time):
    #plot msg load
    # bin_sz = (mpi_op["time"][-1] - mpi_op["time"][0]+1)/NUM_BINS
    bin_sz = time_interval
    num_bins = int(math.ceil(end_time/time_interval))
    # print num_bins
    bins = [x*time_interval/1000.0/1000.0 for x in range(0,num_bins)] #millisec
    msg_load = [0.0 for x in range(0,num_bins)]
    avg_load = [0.0 for x in range(0,num_bins)]
    max_load = [0.0 for x in range(0,num_bins)]
    # print bins
    index = 0
    # start = mpi_op["time"][0]
    start = 0
    for i in xrange(0, num_bins):
        count = 0
        end = start + bin_sz*(i+1)

        while (index <len(mpi_op["time"]) and mpi_op["time"][index] <= end ):
            msg_load[i] += mpi_op["msg_sz"][index]*1024.0
            if (mpi_op["msg_sz"][index]*1024.0 > max_load[i]):
                max_load[i] = mpi_op["msg_sz"][index]*1024.0
            index += 1
            count += 1
        # print i, count
        if count > 0:  
            avg_load[i] = (msg_load[i]/count)
        else:
            avg_load[i] = (msg_load[i])

    total_msg = sum(msg_load)
    peak_load = np.max(avg_load)*1000.0*1000.0*1000.0/bin_sz/1024.0/1024.0    # GB/s
    peakmax_load = np.max(avg_load)    # KB
    bot_load = np.min(avg_load)
    top_load = np.max(avg_load)
    print 'Peak avg load: %.5f GB/s' % (peak_load)
    print 'Total '+ format(total_msg, '.5f') +'KB ( '+ format(np.max(avg_load), '.5f')+' KB/'+ str(bin_sz) +'ns)'
    # print 'min avg: %d  max avg: %d' %(bot_load, top_load)
    print 'peak avg load: %.5f KB / %d ns' % (peakmax_load, bin_sz)
    temp = sorted(avg_load)
    print temp[0:20]

    width = bin_sz/1000.0/1000.0
    # fig = plt.figure(11)
    # ax = fig.add_subplot(111)
    # ax.set_xlabel('Time (milliseconds)', fontsize = label_size)
    # ax.set_ylabel('Total message load (KB)', fontsize = label_size)
    # ax.set_xlim([0, bin_sz*num_bins/1000.0/1000.0])
    # plt.bar(bins, msg_load, width, color="blue", linewidth=0.5)
    # plt.locator_params(axis='x', nbins=5)
    # plt.xticks(fontsize=label_size)
    # plt.yticks(fontsize=label_size)
    # title = prefix +'_Message_Load'
    # # plt.title(title, fontsize = label_size)
    # plt.tight_layout()
    # plt.savefig('./'+title+'.eps', format='eps', dpi=1000)

    fig = plt.figure(12)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time (milliseconds)', fontsize = label_size)
    ax.set_ylabel('Msg load/rank (KB)', fontsize = label_size)
    ax.set_ylim([0, 20])
    ax.set_xlim([0, 0.2])
    # ax.set_ylim([0, 35])
    # ax.set_xlim([0, bin_sz*num_bins/1000.0/1000.0])
    plt.plot(bins, avg_load, color="slategrey", linewidth=2)
    ax.fill_between(bins, avg_load, color="slategrey")
    plt.xticks(fontsize=label_size)
    plt.yticks(fontsize=label_size)
    plt.locator_params(axis='x', nbins=5)
    title = 'Total '+ format(total_msg, '.5f') +'( '+ format(np.max(avg_load), '.5f')+' KB/'+ str(bin_sz) +'ns)'
    # plt.title(title, fontsize = label_size)
    plt.tight_layout()
    plt.savefig('./'+prefix +'_Avg_Msg_Load.eps', format='eps', dpi=1000)
    
    
    # fig = plt.figure(13)
    # ax = fig.add_subplot(111)
    # ax.set_xlabel('Time (milliseconds)', fontsize = label_size)
    # ax.set_ylabel('Peak message load per rank (KB)', fontsize = label_size)
    # # ax.set_ylim([0, 20])
    # ax.set_xlim([0, bin_sz*num_bins/1000.0/1000.0])
    # plt.plot(bins, max_load, color="slategrey", linewidth=2)
    # ax.fill_between(bins, max_load, color="slategrey")
    # plt.xticks(fontsize=label_size)
    # plt.yticks(fontsize=label_size)
    # title = 'Total '+ format(total_msg, '.5f') +'( '+ format(np.max(max_load), '.5f')+' KB/'+ str(bin_sz) +'ns)'
    # # plt.title(title, fontsize = label_size)
    # plt.tight_layout()
    # plt.savefig('./'+prefix +'_Max_Msg_Load.eps', format='eps', dpi=1000)
    


    plt.close(fig)

    return sorted(range(len(msg_load)), key=lambda i: msg_load[i])[-10:]

def plotRtrStat(prefix, rtr_stat, subplot, ylimit):
    lch_stat=[]
    gch_stat=[]
    ter_stat=[]
    for i in range(NUM_BINS):
        lch_temp = list(itertools.chain(*rtr_stat[rtr_stat.keys()[i]]["lch_stat"]))
        lch_temp = [ k for k in lch_temp if k>0 ]
        lch_stat.append(lch_temp)
        gch_temp = list(itertools.chain(*rtr_stat[rtr_stat.keys()[i]]["gch_stat"]))
        gch_temp = [ k for k in gch_temp if k>0 ]
        gch_stat.append(gch_temp)
        ter_temp = list(itertools.chain(*rtr_stat[rtr_stat.keys()[i]]["ter_stat"]))
        ter_temp = [ k for k in ter_temp if k>0 ]
        ter_stat.append(ter_temp)
    # lch_stat = list(itertools.izip_longest(*lch_stat, fillvalue=0.0))
    # gch_stat = list(itertools.izip_longest(*gch_stat, fillvalue=0.0))
    # ter_stat = list(itertools.izip_longest(*ter_stat, fillvalue=0.0))

    # for i in range(NUM_BINS):
    #     lch_temp = list(itertools.chain(*rtr_stat[rtr_stat.keys()[i]]["lch_stat"]))
    #     lch_stat.append(sum(lch_temp))
    #     gch_temp = list(itertools.chain(*rtr_stat[rtr_stat.keys()[i]]["gch_stat"]))
    #     gch_stat.append(sum(gch_temp))
    #     ter_temp = list(itertools.chain(*rtr_stat[rtr_stat.keys()[i]]["ter_stat"]))        
    #     ter_stat.append(sum(ter_temp))
    limit=[]
    if ylimit == None:
        limit.append(0)
        limit.append(0)
        limit.append(0)
    else:
        limit = ylimit

    #plot local channel stat
    lch_max = plot_bars(subplot, lch_stat, 'Total Local Channel Saturation Time (ms)', prefix+'_LChannelSaturationTime', 'tomato', limit[0])
    #plot global channel stat
    gch_max = plot_bars(subplot+1, gch_stat, 'Total Global Channel Saturation Time (ms)', prefix+'_GChannelSaturationTime', 'orange', limit[1])
    #plot terminal stat
    ter_max = plot_bars(subplot+2, ter_stat, 'Total Terminal Saturation Time (ms)', prefix+'_TerminalSaturationTime', 'skyblue', limit[2])

    return lch_max, gch_max, ter_max

def plot_bars(subplot, line_stat, y_label, fig_name, boxcolor, ylimit):
    label_font = 12
    bins = [x*100/NUM_BINS for x in range(0,NUM_BINS)]
    fig = plt.figure(subplot)
    # width = 1/1.5
    # margin_bottom = np.zeros(NUM_BINS)
    # for i in range(len(line_stat)):
    #     if i%2 == 0:
    #         color='dimgray'
    #     else:
    #         color='lightgray'
    #     values = np.asarray(line_stat[i])
    #     plt.bar(bins, values, width, color=color, bottom=margin_bottom)
    #     margin_bottom += values
    # plt.bar(bins, line_stat, width, color='dimgray')

    ax2 = fig.add_subplot(111)
    bp2 = ax2.boxplot(line_stat, patch_artist=True)
    for box in bp2['boxes']:
        box.set( color='#7570b3')
        box.set( facecolor = boxcolor)
    for whisker in bp2['whiskers']:
            whisker.set(color=boxcolor)
    for cap in bp2['caps']:
            cap.set(color=boxcolor)
    for flier in bp2['fliers']:
            flier.set(color= boxcolor)

    axes = plt.gca()
    plt.xticks(np.arange(0, NUM_BINS+1, 10))
    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Normalized Timestamp', fontsize = label_font)
    plt.ylabel(y_label, fontsize = label_font)

    ylim = ax2.get_ylim()
    plt.title(fig_name, fontsize = label_font)
    # # plt.legend(loc = 'lower right')
    # # plt.tight_layout()
    plt.savefig('./' + fig_name+'.eps', format='eps', dpi=1000)
    plt.close(fig)
    return ylim

def readSample(file_name):
    rtr_stat = {}
    wlf = open("dragonfly-rtr-write-"+file_name+".dat", "r")

    for line in wlf:
        line = line.strip('\n')
        line = line.strip('\r')
        if len(line)==0:
            continue
        parts=line.split()
        rtr_id = parts[0]
        timestamp = parts[-3]
        if not rtr_stat.has_key(timestamp):
            rtr_stat[timestamp]={}
            rtr_stat[timestamp]["lch_stat"]=[]
            rtr_stat[timestamp]["lch_traffic"]=[]
            rtr_stat[timestamp]["gch_stat"]=[]
            rtr_stat[timestamp]["gch_traffic"]=[]
            rtr_stat[timestamp]["ter_stat"]=[]
            rtr_stat[timestamp]["ter_traffic"]=[]
        lch_stat=[]
        lch_traffic=[]
        for i in xrange(0,LChannel):
            lch_stat.append(float(parts[1+i])/1000)
            lch_traffic.append(float(parts[1+i])/1024)
        gch_stat=[]
        gch_traffic=[]
        for i in xrange(LChannel, LChannel+GChannel):
            gch_stat.append(float(parts[1+i])/1000)
            gch_traffic.append(float(parts[1+i])/1024)
        ter_stat=[]
        ter_traffic=[]
        for i in xrange(LChannel+GChannel, RADIX):
            ter_stat.append(float(parts[1+i])/1000)
            ter_traffic.append(float(parts[1+i])/1024)
        rtr_stat[timestamp]["lch_stat"].append(lch_stat)
        rtr_stat[timestamp]["lch_traffic"].append(lch_traffic)
        rtr_stat[timestamp]["gch_stat"].append(gch_stat)
        rtr_stat[timestamp]["gch_traffic"].append(gch_traffic)
        rtr_stat[timestamp]["ter_stat"].append(ter_stat)
        rtr_stat[timestamp]["ter_traffic"].append(ter_traffic)          
    wlf.close()

    print len(rtr_stat)
    return rtr_stat

if __name__ == "__main__":

    rank = int(sys.argv[1])
    prefix = sys.argv[2]
    file_name = sys.argv[3]
    time_interval = None
    if len(sys.argv) > 4:
        time_interval = long(sys.argv[4])
    print prefix, rank

    limit=[]
    # rtr_stat = readSample(file_name+'_cont')
    # lch_max, gch_max, ter_max = plotRtrStat(prefix+'_cont', rtr_stat, 20, None)
    # limit.append(lch_max)
    # limit.append(gch_max)
    # limit.append(ter_max)
    # print limit

    # time_interval = float(min(rtr_stat.keys(), key=lambda x: float(x)))
    # print time_interval

    # rtr_stat = readSample(file_name+'_rn')
    # plotRtrStat(prefix+'_rn', rtr_stat, 30, limit)

    # rtr_stat = readSample(file_name+'_rch')
    # plotRtrStat(prefix+'_rch', rtr_stat, 40, limit)

    # rtr_stat = readSample(file_name+'_rcb')
    # plotRtrStat(prefix+'_rcb', rtr_stat, 50, limit)

    mpi_op, z, end_time = readMPI(file_name)
    if not time_interval:
        time_interval = int(math.ceil(end_time/NUM_BINS))
    # print time_interval
    drawHeatmap(rank, prefix, z)
    max_indexes = drawMsgmap(prefix, mpi_op, time_interval, end_time)




