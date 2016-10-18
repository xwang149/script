#!/usr/bin/python
from load_wrkld_data import WorkLoad
import plot_method as pmd


if __name__ == "__main__":
    wrkld1 = WorkLoad()
    wrkld1.load_msg_data()
    pmd.wrkld_tlink_saturation_time_plot(wrkld1, 100)
    pmd.wrkld_tlink_traffic_plot(wrkld1, 101)

    wrkld1.load_router_stats_data()
    pmd.wrkld_router_saturation_time_plot(wrkld1, 200)
    wrkld1.load_router_traffic_data()
    pmd.wrkld_router_traffic_plot(wrkld1, 300)

    pmd.plt.show()
