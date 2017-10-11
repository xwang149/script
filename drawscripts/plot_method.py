#!/usr/bin/python
from operator import truediv
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from load_app_data import APP
from load_wrkld_data import WorkLoad


line_width = 3
label_font = 25
# line_style = [ ['green', '--'],  ['blue', '--'], ['green', '-'], ['blue','-'] ]       #place and route
line_style = [ ['green', '-'], ['red', '-'], ['purple', '-'], ['blue', '-'] ]            #adp
# line_style = [ ['green', '--'], ['red', '--'], ['purple', '--'], ['blue','--'] ]      #min
# line_style = [ ['green', '--'], ['blue', '--'], ['red', '--'], ['green','-'], ['blue','-'], ['red','-']]

def comm_time_plot(app, subplot):
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
    ax2.set_xticklabels(app.xlabel,fontsize = label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    #plt.yticks(fontsize = label_size)
    plt.yticks(fontsize = label_font)
    plt.xticks(fontsize = label_font, rotation=30)
    ax2.set_yticklabels(ax2.get_yticks())
    #axes = plt.gca()
    # ax2.set_ylim([165,170])
    ax2.set_ylabel("Milliseconds", fontsize=label_font)
    title = app.name+'-CommunicationTime'
    plt.title(title, fontsize = label_font)
    plt.tight_layout()
    plt.savefig('./'+app.prefix+title+'.eps', format='eps', dpi=1000)
    # plt.savefig("./" +title+ ".pdf", format='pdf', dpi=1000)
    #  plt.show()


def msg_busytime_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_busytime), len(APP.xlabel)
    for item in range(len(APP.msg_busytime)):
        #  print "idx is", item
        busytime = APP.msg_busytime[item]
        busytime.sort()
        yvals = np.arange(len(busytime))/float(len(busytime))
        plt.plot(busytime, yvals*100, label=APP.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                 )

    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.locator_params(axis='x', nbins=5)
    plt.xlabel('Saturated Time(Milliseconds)', fontsize = label_font)
    plt.ylabel('Percentage of Ranks', fontsize = label_font)
    # axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    title = APP.name + '_TerminalLinkSaturatedTime'
    # plt.title(title, fontsize = label_font)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+APP.prefix + title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def msg_avghop_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_avg_hop), len(APP.xlabel)
    for item in range(len(APP.msg_avg_hop)):
        #  print "idx is", item
        avg_hop = APP.msg_avg_hop[item]
        avg_hop.sort()
        yvals = np.arange(len(avg_hop))/float(len(avg_hop))
        plt.plot(avg_hop, yvals*100, label=APP.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                 )

    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Msg Avg Hops', fontsize = label_font)
    plt.ylabel('Percentage of Ranks', fontsize = label_font)
    title = APP.name + '-RankAvgHop'
    plt.title(title, fontsize = label_font)
    plt.legend(loc = 'best', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+APP.prefix + title+'.eps', format='eps', dpi=1000)
    #  plt.show()


def tlink_traffic_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_latency), len(APP.xlabel)
    for item in range(len(APP.tlink_traffic)):
        tlink_traffic = APP.tlink_traffic[item]
        tlink_traffic.sort()
        yvals = np.arange(len(tlink_traffic))/float(len(tlink_traffic))
        plt.plot(tlink_traffic, yvals*100, label=APP.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                 )


    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.locator_params(axis='x', nbins=5)
    plt.xlabel('Terminal Traffic Amount (MB)', fontsize = label_font)
    plt.ylabel('Percentage of Terminal Links', fontsize = label_font)
    title = APP.name + '_TlinkTraffic'
    #  plt.title(APP.name + '\n MPI Rank transfer latency(total_time/num_packet)', fontsize = label_font)
    # plt.title(title, fontsize = label_font)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+ APP.prefix + title+'.eps', format='eps', dpi=1000)
    #  plt.show()



def msg_latency_plot(APP, subplot):
    plt.figure(subplot)
    #  print len(APP.msg_latency), len(APP.xlabel)
    for item in range(len(APP.msg_latency)):
        msg_latency = APP.msg_latency[item]
        msg_latency.sort()
        yvals = np.arange(len(msg_latency))/float(len(msg_latency))
        plt.plot(msg_latency, yvals*100, label=APP.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                 )

    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.xticks(fontsize = label_font)
    plt.yticks(fontsize = label_font)
    plt.xlabel('Msg Latency (Milliseconds)', fontsize = label_font)
    plt.ylabel('Percentage of Ranks', fontsize = label_font)
    title = APP.name + '_MsgLatency'
    #  plt.title(APP.name + '\n MPI Rank transfer latency(total_time/num_packet)', fontsize = label_font)
    # plt.title(title, fontsize = label_font)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.locator_params(axis='x', nbins=5)
    plt.tight_layout()
    plt.savefig('./'+APP.prefix + title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def router_lch_stats_plot(app, subplot):
    plt.figure(subplot)
    for item in range(len(app.router_lch_stats)):
        lch_stats = app.router_lch_stats[item]
        lch_stats.sort()
        yvals = np.arange(len(lch_stats))/float(len(lch_stats))
        plt.plot(lch_stats, yvals*100, label=app.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                )
    
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    # axes.set_xlim(left=0)
    # plt.ylim(90, 100)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.locator_params(axis='x', nbins=5)
    plt.xlabel('Saturated time (Milliseconds)', fontsize=label_font)
    plt.ylabel('Percentage of Routers', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-LchannelSaturatedTime'
    else:
        title = app.name + '-LchannelSaturatedTime'
    plt.title(title,  fontsize=label_font)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+app.prefix + title+'.eps', format='eps', dpi=1000)
    #  plt.show()

def router_lch_traffic_plot(app, subplot):
    plt.figure(subplot)
    maxlen = 0
    for elem in app.router_lch_traffic:
       if maxlen < len(elem):
           maxlen = len(elem)

    for item in range(len(app.router_lch_traffic)):
       print len(app.router_lch_traffic[item]), app.router_lch_traffic[item][0], app.router_lch_traffic[item][len(app.router_lch_traffic[item])-1]
       router_lch_traffic = [None]*(maxlen-len(app.router_lch_traffic[item]))+ \
                           app.router_lch_traffic[item]
       # print len(router_lch_traffic), router_lch_traffic[0], router_lch_traffic[len(router_lch_traffic)-1]
       plt.plot(router_lch_traffic, label=app.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
    # for item in range(len(app.router_lch_traffic)):
    #     lch_traffic = app.router_lch_traffic[item]
    #     lch_traffic.sort()
    #     yvals = np.arange(len(lch_traffic))/float(len(lch_traffic))
    #     plt.plot(lch_traffic, yvals*100, label=app.xlabel[item]
                )

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    axes.set_xlim(left=0)
    # axes.set_ylim([10,100])
    # plt.xlabel('Traffic Amount(MB)', fontsize=label_font)
    # plt.ylabel('Percentage of Routers', fontsize=label_font)
    # if app.name in 'syn':
    #     title = 'total-LchannelTraffic'
    # else:
    #     title = app.name+'-LchannelTraffic'
    # plt.title(title , fontsize=label_font)
    # plt.legend(loc = 'lower right')
    # plt.tight_layout()
    # plt.savefig('./'+app.prefix + title+'.eps', format='eps', dpi=1000)
    plt.locator_params(axis='x', nbins=5)
    plt.xlabel('Router ID sorted by local channel traffic', fontsize=label_font)
    plt.ylabel('Traffic Amount(MB)', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-LchannelTraffic'
    else:
        title = app.name+'-LchannelTraffic'
    # plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+app.prefix +title+'.eps', format='eps', dpi=1000)
    #  plt.show()



def router_gch_stats_plot(app, subplot):
    plt.figure(subplot)
    for item in range(len(app.router_gch_stats)):
        gch_stats = app.router_gch_stats[item]
        gch_stats.sort()
        yvals = np.arange(len(gch_stats))/float(len(gch_stats))
        plt.plot(gch_stats, yvals*100, label=app.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                )
        
    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    plt.locator_params(axis='x', nbins=5)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.xlabel('Saturated time (Milliseconds)', fontsize=label_font)
    plt.ylabel('Percentage of Routers', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-GchannelSaturatedTime'
    else:
        title = app.name + '-GchannelSaturatedTime'
    plt.title(title , fontsize=label_font)
    plt.locator_params(axis='x', nbins=5)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+ app.prefix + title+'.eps', format='eps', dpi=1000)
    #  plt.show()


def router_gch_traffic_plot(app, subplot):
    plt.figure(subplot)
    maxlen = 0
    for elem in app.router_gch_traffic:
       if maxlen < len(elem):
           maxlen = len(elem)

    for item in range(len(app.router_gch_traffic)):
        # gch_traffic = app.router_gch_traffic[item]
        # gch_traffic.sort()
        # yvals = np.arange(len(gch_traffic))/float(len(gch_traffic))
        # plt.plot(gch_traffic, yvals*100, label=app.xlabel[item]
        router_gch_traffic = [None]*(maxlen-len(app.router_gch_traffic[item]))+ \
                            app.router_gch_traffic[item].tolist()
        # print router_gch_traffic
        plt.plot(router_gch_traffic, label=app.xlabel[item]
                ,linewidth=line_width, color=line_style[item][0],\
                linestyle=line_style[item][1]
                )

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    plt.locator_params(axis='x', nbins=5)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    axes.set_xlim(left=0)
    # axes.set_ylim([0,10])
    # plt.xlabel('Traffic Amount(MB)', fontsize=label_font)
    # plt.ylabel('Percentage of Routers', fontsize=label_font)
    # if app.name in 'syn':
    #     title = 'total-GchannelTraffic'
    # else:
    #     title = app.name + '-GchannelTraffic'
    # plt.title(title , fontsize=label_font)
    # plt.legend(loc = 'lower right')
    # plt.tight_layout()
    # plt.savefig('./'+app.prefix + title+'.eps', format='eps', dpi=1000)
    plt.xlabel('Router ID sorted by global channel traffic', fontsize=label_font)
    plt.ylabel('Traffic Amount(MB)', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-GchannelTraffic'
    else:
        title = app.name + '-GchannelTraffic'
    # plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+app.prefix+title+'.eps', format='eps', dpi=1000)
    #  plt.show()


def router_gch_load_plot(app, subplot):
    plt.figure(subplot)
    maxlen = 0
    for elem in app.router_gch_load:
       if maxlen < len(elem):
           maxlen = len(elem)

    for item in range(len(app.router_gch_load)):
        gch_traffic = app.router_gch_load[item]
        gch_traffic.sort()
        yvals = np.arange(len(gch_traffic))/float(len(gch_traffic))
        plt.plot(gch_traffic, yvals*100, label=app.xlabel[item]
        # router_gch_traffic = [None]*(maxlen-len(app.router_gch_load[item]))+ \
                            # app.router_gch_load[item]
        # print router_gch_traffic
        # plt.plot(router_gch_traffic,label=app.xlabel[item], "o"
                ,linewidth=line_width 
                ,linestyle=line_style[item][1]
                ,color=line_style[item][0]
                )

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    plt.locator_params(axis='x', nbins=5)
    axes = plt.gca()
    axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.xlabel('Traffic Amount (MB)', fontsize=label_font)
    plt.ylabel('Percentage of global channels', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-GchannelLoad'
    else:
        title = app.name + '-GchannelLoad'
    # plt.title(title , fontsize=label_font)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+app.prefix+title+'.eps', format='eps', dpi=1000)


def router_lch_load_plot(app, subplot):
    plt.figure(subplot)
    maxlen = 0
    for elem in app.router_lch_load:
       if maxlen < len(elem):
           maxlen = len(elem)

    for item in range(len(app.router_lch_load)):
        lch_traffic = app.router_lch_load[item]
        lch_traffic.sort()
        yvals = np.arange(len(lch_traffic))/float(len(lch_traffic))
        plt.plot(lch_traffic, yvals*100, label=app.xlabel[item]
        # router_lch_traffic = [None]*(maxlen-len(app.router_lch_load[item]))+ \
                            # app.router_lch_load[item]
        # print router_gch_traffic
        # plt.plot(router_lch_traffic,label=app.xlabel[item], "o"
                ,linewidth=line_width
                ,linestyle=line_style[item][1]
                ,color=line_style[item][0]
                )

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    plt.locator_params(axis='x', nbins=5)
    axes = plt.gca()
    axes.set_xlim(left=0)
    # Hide the right and top spines
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    plt.grid(color='grey')

    plt.xlabel('Traffic Amount (MB)', fontsize=label_font)
    plt.ylabel('Percentage of local channels', fontsize=label_font)
    if app.name in 'syn':
        title = 'total-LchannelLoad'
    else:
        title = app.name + '-LchannelLoad'
    # plt.title(title , fontsize=label_font)
    plt.legend(loc = 'lower right', fontsize=20)
    plt.tight_layout()
    plt.savefig('./'+app.prefix+title+'.eps', format='eps', dpi=1000)




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

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Saturation Time (Millisecond)', fontsize=label_font)
    plt.ylabel('Percentage of Terminal Link',fontsize=label_font)
    title = 'TerminalLinkSaturationTime_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best', fontsize=20)
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

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Data Amount (MB)', fontsize=label_font)
    plt.ylabel('Percentage of Terminal Link',fontsize=label_font)
    title = 'TerminalLinkDataTransferAmount_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best', fontsize=20)
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

    plt.xticks(fontsize=label_font)
    plt.yticks(fontsize=label_font)
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))#scientific notation
    axes = plt.gca()
    #  axes.set_ylim([0,120])
    plt.xlabel('Saturation Time (Millisecond)', fontsize=label_font)
    plt.ylabel('Percentage of Router',fontsize=label_font)
    title = 'LocalChannelSaturationTime_CDF'
    plt.title(title , fontsize=label_font)
    plt.legend(loc = 'best', fontsize=20)
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


