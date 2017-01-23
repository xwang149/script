#!/usr/bin/python
from operator import truediv
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from load_app_data import APP
from load_wrkld_data import WorkLoad


line_width = 3
line_style = [ ['blue', '--'], ['red', '--'], ['green', '--'],\
             ['blue', '-'], ['red', '-'], ['green', '-'] ]


def comm_time_plot(app, subplot):
    label_size = 12
    fig = plt.figure(subplot)
    # fig.set_canvas(plt.gcf().canvas)
    ax2 = fig.add_subplot(111)
    bp2 = ax2.boxplot(app.comm_time_data, patch_artist=True)
    for box in bp2['boxes']:
        box.set( color='#7570b3', linewidth=2)
        box.set( facecolor = app.color)
    for whisker in bp2['whiskers']:
            whisker.set(color=app.color, linewidth=2)
    for cap in bp2['caps']:
            cap.set(color=app.color, linewidth=2)
    for median in bp2['medians']:
            median.set(color=app.med_color, linewidth=4)
    for flier in bp2['fliers']:
            flier.set(marker='o', color= app.color, alpha=0.8)
    ax2.set_xticklabels(app.xlabel,fontsize = label_size)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    #plt.yticks(fontsize = label_size)
    plt.yticks(fontsize = label_size)
    plt.xticks(fontsize = label_size, rotation=30)
    #axes = plt.gca()
    #axes.set_ylim([800,4000])
    ax2.set_ylabel("millisecond", fontsize=label_size)
    title = app.name+'_CommunicationTime'
    plt.title(title, fontsize = label_size)
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    # plt.savefig("./" +title+ ".pdf", format='pdf', dpi=1000)
    #  plt.show()


def msg_busytime_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_busytime), len(APP.xlabel)
    for item in range(len(APP.msg_busytime)):
        #  print "idx is", item
        APP.msg_busytime[item].sort()
        plt.plot(APP.msg_busytime[item], label=APP.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #axes.set_ylim([0,10])
    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Ranks sorted by Saturated Time', fontsize = label_font)
    plt.ylabel('Saturated Time(Nanosecond) ', fontsize = label_font)
    title = APP.name + '_TerminalLinkSaturatedTime'
    plt.title(title, fontsize = label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def msg_avghop_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_avg_hop), len(APP.xlabel)
    for item in range(len(APP.msg_avg_hop)):
        #  print "idx is", item
        APP.msg_avg_hop[item].sort()
        plt.plot(APP.msg_avg_hop[item], label=APP.xlabel[item] 
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1]
                )

    label_font = 24
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #axes.set_ylim([0,10])
    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Ranks sorted by Msg Avg Hop', fontsize = label_font)
    plt.ylabel('Avg Hops ', fontsize = label_font)
    title = APP.name + '_RankAvgHop'
    plt.title(title, fontsize = label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()



def tlink_traffic_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_latency), len(APP.xlabel)
    for item in range(len(APP.tlink_traffic)):
        #  print "idx is", item
        APP.tlink_traffic[item].sort()
        plt.plot(APP.tlink_traffic[item], label=APP.xlabel[item], linewidth=line_width )

    label_font = 24
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #axes.set_ylim([0,10])
    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Ranks sorted by Terminal Traffic', fontsize = label_font)
    plt.ylabel('Data Amount (MB) ', fontsize = label_font)
    title = APP.name + '_TlinkTraffic'
    #  plt.title(APP.name + '\n MPI Rank transfer latency(total_time/num_packet)', fontsize = label_font)
    plt.title(title, fontsize = label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()



def msg_latency_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_latency), len(APP.xlabel)
    for item in range(len(APP.msg_latency)):
        #  print "idx is", item
        APP.msg_latency[item].sort()
        plt.plot(APP.msg_latency[item], label=APP.xlabel[item], linewidth=line_width )

    label_font = 24
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #axes.set_ylim([0,10])
    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Ranks sorted by Msg Latency', fontsize = label_font)
    plt.ylabel('Latency (Millisecond) ', fontsize = label_font)
    title = APP.name + '_MsgLatency'
    #  plt.title(APP.name + '\n MPI Rank transfer latency(total_time/num_packet)', fontsize = label_font)
    plt.title(title, fontsize = label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def router_lch_stats_plot(app, subplot):
    plt.figure(subplot)
    for item in range(len(app.router_lch_stats)):
        plt.plot(app.router_lch_stats[item], label=app.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )


    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #axes.set_ylim([0,160])
    plt.xlabel('Router ID sorted by local channel Saturated time', fontsize=label_font)
    plt.ylabel('Saturated time (Millisecond)', fontsize=label_font)
    if app.name in 'syn':
        title = 'total_LchannelSaturatedTime'
    else:
        title = app.name + '_LchannelSaturatedTime'
    plt.title(title,  fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def router_lch_traffic_plot(app, subplot):
    plt.figure(subplot)
    maxlen = 0
    for elem in app.router_lch_traffic:
        if maxlen < len(elem):
            maxlen = len(elem)

    for item in range(len(app.router_lch_traffic)):
        router_lch_traffic = [None]*(maxlen-len(app.router_lch_traffic[item]))+ \
                            app.router_lch_traffic[item]
        plt.plot(router_lch_traffic, label=app.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Router ID sorted by local channel traffic', fontsize=label_font)
    plt.ylabel('Traffic Amount(MB)', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-LchannelTraffic'
    else:
        title = app.name+'-LchannelTraffic'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()



def router_gch_stats_plot(app, subplot):
    plt.figure(subplot)
    for item in range(len(app.router_gch_stats)):
        plt.plot(app.router_gch_stats[item], label=app.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #axes.set_ylim([0,160])
    plt.xlabel('Router ID sorted by global channel Saturated time', fontsize=label_font)
    plt.ylabel('Saturated time (Millisecond)', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-GchannelSaturatedTime'
    else:
        title = app.name + '-GchannelSaturatedTime'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def router_gch_traffic_plot(app, subplot):
    plt.figure(subplot)
    maxlen = 0
    for elem in app.router_gch_traffic:
        if maxlen < len(elem):
            maxlen = len(elem)

    for item in range(len(app.router_gch_traffic)):
        router_gch_traffic = [None]*(maxlen-len(app.router_gch_traffic[item]))+ \
                            app.router_gch_traffic[item].tolist()
        plt.plot(router_gch_traffic, label=app.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Router ID sorted by global channel traffic', fontsize=label_font)
    plt.ylabel('Traffic Amount(MB)', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-GchannelTraffic'
    else:
        title = app.name + '-GchannelTraffic'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def wrkld_tlink_saturation_time_plot(wrkld, subplot):
    plt.figure(subplot)
    for item in range(len(wrkld.Tlink_busytime)):
        busytime = wrkld.Tlink_busytime[item]
        busytime.sort()
        yvals = np.arange(len(busytime))/float(len(busytime))
        plt.plot(busytime, yvals*100, label=wrkld.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Saturation Time (Millisecond)', fontsize=label_font)
    plt.ylabel('Percentage of Terminal Link',fontsize=label_font)
    title = 'TerminalLinkSaturationTime_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def wrkld_tlink_traffic_plot(wrkld, subplot):
    plt.figure(subplot)
    for item in range(len(wrkld.Tlink_traffic)):
        traffic = wrkld.Tlink_traffic[item]
        traffic.sort()
        yvals = np.arange(len(traffic))/float(len(traffic))
        plt.plot(traffic, yvals*100, label=wrkld.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )


    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Data Amount (MB)', fontsize=label_font)
    plt.ylabel('Percentage of Terminal Link',fontsize=label_font)
    title = 'TerminalLinkDataTransferAmount_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def wrkld_router_saturation_time_plot(wrkld, subplot):
    plt.figure(subplot)
    for item in range(len(wrkld.router_lch_stats)):
        lch_busytime = wrkld.router_lch_stats[item]
        lch_busytime.sort()
        yvals = np.arange(len(lch_busytime))/float(len(lch_busytime))
        plt.plot(lch_busytime, yvals*100, label=wrkld.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Saturation Time (Millisecond)', fontsize=label_font)
    plt.ylabel('Percentage of Router',fontsize=label_font)
    title = 'LocalChannelSaturationTime_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()


    # =====plot Global Channel saturation time====
    plt.figure(subplot+1)
    for item in range(len(wrkld.router_gch_stats)):
        gch_busytime = wrkld.router_gch_stats[item]
        gch_busytime.sort()
        yvals = np.arange(len(gch_busytime))/float(len(gch_busytime))
        plt.plot(gch_busytime, yvals*100, label=wrkld.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Saturation Time (Millisecond)', fontsize=label_font)
    plt.ylabel('Percentage of Router',fontsize=label_font)
    title = 'GlobalChannelSaturationTime_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def wrkld_router_traffic_plot(wrkld, subplot):
    plt.figure(subplot)
    for item in range(len(wrkld.router_lch_traffic)):
        lc_traffic = wrkld.router_lch_traffic[item]
        lc_traffic.sort()
        yvals = np.arange(len(lc_traffic))/float(len(lc_traffic))
        plt.plot(lc_traffic, yvals*100, label=wrkld.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Traffic Amount (MB)', fontsize=label_font)
    plt.ylabel('Percentage of Router',fontsize=label_font)
    title = 'LocalChannelTrafficAmount_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()



    # =====plot Global Channel saturation time====
    plt.figure(subplot+1)
    for item in range(len(wrkld.router_gch_traffic)):
        gc_traffic = wrkld.router_gch_traffic[item]
        gc_traffic.sort()
        yvals = np.arange(len(gc_traffic))/float(len(gc_traffic))
        plt.plot(gc_traffic, yvals*100, label=wrkld.xlabel[item]
                #  linewidth=line_width, color=line_style[item][0],\
                #  linestyle=line_style[item][1])
                )

    label_font = 24
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Traffic Amount (MB)', fontsize=label_font)
    plt.ylabel('Percentage of Router',fontsize=label_font)
    title = 'GlobalChannelTrafficAmount_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('./'+title+'.eps', format='eps', dpi=1000)
    #  plt.show()


