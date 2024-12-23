import psutil
import functools
import pyqtgraph

from .. import sys_utils
from ..qt_components import CWTM_TabManager
from .core_properties import (
    CWTM_NetworkingTabTableColumns,
    CWTM_TableWidgetItemProperties
)
from ..qt_widgets import CWTM_ResourceGraphWidget
from ..thread_workers import CWTM_NetworkingInterfaceRetrievalWorker

from PyQt5.QtCore import (
    Qt, QTimer,
    pyqtSignal,
    QThread, QObject
)
from PyQt5.QtWidgets import QTableWidgetItem, QGroupBox


class CWTM_NetworkingTab(CWTM_TabManager):
    def __init__(self, parent):
        self.parent = parent
        
        self.NETWORK_INTERFACE_GRAPHS = {}
        self.NET_T_NETWORKING_LIST_TABLE_UPDATE_FREQUENCY = 1000

    def setup_system_networking_interfaces(self):
        system_networking_interfaces = psutil.net_if_addrs().items()

        for interface_name, interface_info in system_networking_interfaces:
            self.register_network_interface(interface_name)

    def register_network_interface(self, interface_name):
        interface_full_name = sys_utils.get_interface_type_full_name(
                interface_name
            ) + f" ({interface_name})" # Local Area Connection (lo)

        (i_net_graph, i_net_groupbox,
         i_net_sent_data_x, i_net_sent_data_y,
         i_net_recv_data_x, i_net_recv_data_y,
         i_net_sent_plot_item, i_net_recv_plot_item) = \
             self._network_create_interface_resource_graph(
                    interface_full_name)
        
        self.NETWORK_INTERFACE_GRAPHS[interface_name] = (
            i_net_graph, i_net_groupbox, i_net_sent_data_x, 
            i_net_sent_data_y, i_net_recv_data_x, i_net_recv_data_y,
            i_net_sent_plot_item, i_net_recv_plot_item,
            interface_full_name)

        self.parent.net_t_vbox_layout.addWidget(i_net_groupbox)
        self.update_networking_page_net_list_table(interface_full_name)

    def unregister_disconnected_network_interface(self, interface_name):
        (_, i_net_groupbox, *_) = self.NETWORK_INTERFACE_GRAPHS[interface_name]
        self.parent.net_t_vbox_layout.removeWidget(i_net_groupbox)
        self.refresh_networking_page_net_list_table()

        del self.NETWORK_INTERFACE_GRAPHS[interface_name]

    def refresh_networking_page_net_list_table(self):
        self.parent.net_t_network_list_table.setRowCount(0)
        system_networking_interfaces = psutil.net_if_addrs().items()

        for interface_name, interface_info in system_networking_interfaces:
            interface_full_name = sys_utils.get_interface_type_full_name(
                interface_name
            ) + f" ({interface_name})" # Local Area Connection (lo)

            self.update_networking_page_net_list_table(interface_full_name)

    def update_networking_page(self, n_interface, n_b_sent, n_b_recv):
        if n_interface not in self.NETWORK_INTERFACE_GRAPHS:
            self.register_network_interface(n_interface)

        (i_net_graph, i_net_groupbox, i_net_sent_data_x, 
        i_net_sent_data_y, i_net_recv_data_x, i_net_recv_data_y,
        i_net_sent_plot_item, i_net_recv_plot_item,
        i_net_full_name) = self.NETWORK_INTERFACE_GRAPHS[n_interface]
        
        i_net_graph.update_plot(
            i_net_sent_plot_item, n_b_sent,
            i_net_sent_data_x, i_net_sent_data_y
        )
        i_net_graph.update_plot(
            i_net_recv_plot_item, n_b_recv,
            i_net_recv_data_x, i_net_recv_data_y
        )

        *graph_equal_ticks, = i_net_graph.get_equal_tick_spacing(4)
        self.set_networking_speed_unit_ticks(i_net_graph, graph_equal_ticks)
        self.set_network_interface_table_information(
            i_net_graph, n_b_sent, n_b_recv, n_interface, i_net_full_name
        )

    def set_network_interface_table_information(
        self, network_graph, sent_bytes, recv_bytes, interface_name, interface_full_name):
        _, max_y = network_graph.viewRange()[1]
        if recv_bytes > max_y or sent_bytes > max_y:
            total_net_utilization = 100
        else:
            network_sending_percentage = sent_bytes / max_y * 100
            network_receiving_percentage = recv_bytes / max_y * 100

            total_net_utilization = (
                network_sending_percentage + network_receiving_percentage
            ) / 2

        total_net_utilization_label = f"{round(total_net_utilization, 1)}%"

        network_interface_is_connected = sys_utils.check_if_network_interface_is_connected(
            interface_name
        )
        network_interface_is_connected_label = "Connected" if network_interface_is_connected \
                                                    else "Disconnected"

        self.update_networking_page_net_list_table(
            interface_full_name, 
            total_net_utilization_label, 
            "-", network_interface_is_connected_label
        )

    def set_networking_speed_unit_ticks(self, network_graph, tick_values):
        ticks = [(0, "0 B/s")]

        for tick_value in tick_values:
            tick_value_speed, tick_value_speed_label = sys_utils.get_memory_size_info(
                int(tick_value)
            )
            tick_value_speed_full = f"{tick_value_speed} {tick_value_speed_label}/s"
            ticks.append((int(tick_value), tick_value_speed_full))

        network_graph.plot_left_axis.setTicks([ticks])


    def update_networking_page_net_list_table(
        self, interface_full_name, net_utilization="-", link_speed="-", network_state="-"):
        self.append_row_to_table(
            self.parent.net_t_network_list_table, CWTM_NetworkingTabTableColumns,
            CWTM_TableWidgetItemProperties(item_label=interface_full_name, 
                item_tool_tip=interface_full_name),
            CWTM_TableWidgetItemProperties(item_label=net_utilization), 
            CWTM_TableWidgetItemProperties(item_label=link_speed), #todo
            CWTM_TableWidgetItemProperties(item_label=network_state)
        )


    def _network_create_interface_resource_graph(self, interface_full_name):
        interface_net_graph = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=False, show_left_values=True,
            dotted_grid_lines=self.parent.old_style
        )
        net_grid_usage_sent_data_x, net_grid_usage_sent_data_y = \
                                    interface_net_graph.get_all_data_axes()
        net_grid_usage_recv_data_x, net_grid_usage_recv_data_y = \
                                    interface_net_graph.get_all_data_axes()
        net_grid_usage_sent_plot_item = interface_net_graph.plot(
            net_grid_usage_sent_data_x, net_grid_usage_sent_data_y,
            pen=pyqtgraph.mkPen(color="g", width=1)
        )
        net_grid_usage_recv_plot_item = interface_net_graph.plot(
            net_grid_usage_recv_data_x, net_grid_usage_recv_data_y,
            pen=pyqtgraph.mkPen(color="r", width=1)
        )
        interface_net_groupbox = self.add_full_size_widget_to_groupbox(
            interface_full_name, interface_net_graph
        )

        return (interface_net_graph, interface_net_groupbox,
                net_grid_usage_sent_data_x, net_grid_usage_sent_data_y,
                net_grid_usage_recv_data_x, net_grid_usage_recv_data_y,
                net_grid_usage_sent_plot_item, net_grid_usage_recv_plot_item)

    def start_networking_page_updater_thread(self):
        self.networking_interface_retrieval_thread = QThread()
        self.networking_interface_retrieval_worker = \
            CWTM_NetworkingInterfaceRetrievalWorker(
                self.NET_T_NETWORKING_LIST_TABLE_UPDATE_FREQUENCY, self.parent)      

        self.networking_interface_retrieval_worker.moveToThread(
            self.networking_interface_retrieval_thread
        )

        self.networking_interface_retrieval_thread.started.connect(
            self.networking_interface_retrieval_worker.run
        )
        self.networking_interface_retrieval_worker.ni_sig_usage_frame.connect(
            self.update_networking_page
        )
        self.networking_interface_retrieval_worker.ni_sig_disconnect_nic.connect(
            self.unregister_disconnected_network_interface
        )
        
        #self.networking_interface_retrieval_worker.networking_interface_retrieval_timer.timeout.connect(
        #    functools.partial(self.parent.net_t_network_list_table.setRowCount, 0)
        #)
        self.networking_interface_retrieval_thread.start()
