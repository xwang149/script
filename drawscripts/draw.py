#!/usr/bin/python
from load_app_data import APP
import plot_method as pmd
import sys

if __name__ == "__main__":

    app = sys.argv[1]
    hasSyn = int(sys.argv[2])
    if not sys.argv[3]:
        prefix = ""
    else:
        prefix = sys.argv[3]
    print prefix
    if (app.lower()=='amg'):
        amg = APP('AMG', prefix, ['pink', 'purple'], hasSyn)

        amg.load_commtime_data('.')
        pmd.comm_time_plot(amg, 10)

        amg.load_msg_data()
        pmd.msg_busytime_plot(amg,11)
        pmd.msg_avghop_plot(amg, 12)
        pmd.msg_latency_plot(amg,13)
        # pmd.tlink_traffic_plot(amg, 18)

        amg.load_router_stats_data()
        pmd.router_lch_stats_plot(amg, 14)
        pmd.router_gch_stats_plot(amg, 15)

        amg.load_router_traffic_data()
        pmd.router_gch_traffic_plot(amg, 16)
        pmd.router_lch_traffic_plot(amg, 17)
        pmd.router_lch_load_plot(amg,18)
        pmd.router_gch_load_plot(amg,19)

        pmd.plt.close()

    elif (app.lower()=='mg'):
        mg = APP('MG',prefix, ['steelblue', 'black'], hasSyn)

        mg.load_commtime_data('.')
        pmd.comm_time_plot(mg, 20)

        mg.load_msg_data()
        pmd.msg_busytime_plot(mg,21)
        pmd.msg_avghop_plot(mg, 22)
        pmd.msg_latency_plot(mg,23)
        # pmd.tlink_traffic_plot(mg, 28)

        mg.load_router_stats_data()
        pmd.router_lch_stats_plot(mg, 24)
        pmd.router_gch_stats_plot(mg, 25)

        mg.load_router_traffic_data()
        pmd.router_gch_traffic_plot(mg, 26)
        pmd.router_lch_traffic_plot(mg, 27)
        pmd.router_lch_load_plot(mg,28)
        pmd.router_gch_load_plot(mg,29)

        pmd.plt.close()

    elif (app.lower()=='fb'):
        mg = APP('FB',prefix, ['steelblue', 'black'], hasSyn)

        mg.load_commtime_data('.')
        pmd.comm_time_plot(mg, 20)

        mg.load_msg_data()
        pmd.msg_busytime_plot(mg,21)
        pmd.msg_avghop_plot(mg, 22)
        pmd.msg_latency_plot(mg,23)
        # pmd.tlink_traffic_plot(mg, 28)

        mg.load_router_stats_data()
        pmd.router_lch_stats_plot(mg, 24)
        pmd.router_gch_stats_plot(mg, 25)

        mg.load_router_traffic_data()
        pmd.router_gch_traffic_plot(mg, 26)
        pmd.router_lch_traffic_plot(mg, 27)
        pmd.router_lch_load_plot(mg,28)
        pmd.router_gch_load_plot(mg,29)

        pmd.plt.close()

    elif (app.lower()=='cr'):
        cr = APP('CR',prefix, ['blue', 'black'], hasSyn)

        cr.load_commtime_data('.')
        pmd.comm_time_plot(cr, 30)

        cr.load_msg_data()
        pmd.msg_busytime_plot(cr, 31)
        pmd.msg_avghop_plot(cr, 32)
        pmd.msg_latency_plot(cr, 33)
        # pmd.tlink_traffic_plot(cr, 38)

        cr.load_router_stats_data()
        pmd.router_lch_stats_plot(cr, 34)
        pmd.router_gch_stats_plot(cr, 35)

        cr.load_router_traffic_data()
        pmd.router_gch_traffic_plot(cr, 36)
        pmd.router_lch_traffic_plot(cr, 37)
        pmd.router_lch_load_plot(cr,38)
        pmd.router_gch_load_plot(cr,39)

        pmd.plt.close()

    elif (app.lower()=='syn'):
        syn = APP('syn',prefix, ['yellow', 'magenta'], hasSyn)

        syn.load_commtime_data('.')
        pmd.comm_time_plot(syn, 50)

        syn.load_msg_data()
        pmd.msg_busytime_plot(syn,51)
        pmd.msg_avghop_plot(syn, 52)
        pmd.msg_latency_plot(syn,53)
        # pmd.tlink_traffic_plot(syn, 58)

        syn.load_router_stats_data()
        pmd.router_lch_stats_plot(syn, 54)
        pmd.router_gch_stats_plot(syn, 55)

        syn.load_router_traffic_data()
        pmd.router_gch_traffic_plot(syn, 56)
        pmd.router_lch_traffic_plot(syn, 57)
        pmd.router_lch_load_plot(syn,58)
        pmd.router_gch_load_plot(syn,59)

        pmd.plt.close()

    else:
        oth = APP(app, prefix, ['cyan', 'teal'], hasSyn)

        oth.load_commtime_data('.')
        pmd.comm_time_plot(oth, 40)

        oth.load_msg_data()
        pmd.msg_busytime_plot(oth,41)
        pmd.msg_avghop_plot(oth, 42)
        pmd.msg_latency_plot(oth,43)
        # pmd.tlink_traffic_plot(oth, 48)

        oth.load_router_stats_data()
        pmd.router_lch_stats_plot(oth, 44)
        pmd.router_gch_stats_plot(oth, 45)

        oth.load_router_traffic_data()
        pmd.router_gch_traffic_plot(oth, 46)
        pmd.router_lch_traffic_plot(oth, 47)
        pmd.router_lch_load_plot(oth,48)
        pmd.router_gch_load_plot(oth,49)

        pmd.plt.close()
    # pmd.plt.show()
