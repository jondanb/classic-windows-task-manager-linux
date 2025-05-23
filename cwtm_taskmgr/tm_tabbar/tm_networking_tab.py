import psutil
import pyqtgraph

from PyQt5.QtCore import  (
    Qt, 
    pyqtSignal, 
    pyqtSlot,
    QThread, 
    QObject
)

from .. import sys_utils
from ..qt_components import (
    CWTM_TableWidgetController,
    CWTM_GlobalUpdateIntervalHandler,
    CWTM_TableWidgetUpdateInitializer
)
from ..core_properties import (
    CWTM_NetworkingTabTableColumns,
    CWTM_NetworkingBytesLabelsColours,
    CWTM_NetworkInterfaceGraphProperties,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_NetworkInterfaceUsagePacket
)
from ..qt_widgets import CWTM_ResourceGraphWidget
from ..thread_workers import CWTM_NetworkingInterfaceRetrievalWorker


class CWTM_NetworkingTab(QObject, CWTM_TableWidgetController):
    def __init__(self, *args: list, parent: QObject, **kwargs: dict) -> None:
        """
        Initializes the networking tab for the task manager. This function sets up all the properties for
        the networking tab including the:
            - The update interval speed based on the enum properties of CWTM_GlobalUpdateIntervals.
            - The graphical networking widgets sizes and properties.

        Arguments:
            - args and kwargs: any arbitrary extra argument/keywork arguments to be passed into the
                main superclass. (QObject)
            - parent (QObject): Initialize the class with the parent as a property the superclass. 
        """
        super().__init__(*args, parent=parent, **kwargs)

        self.parent: QObject = parent
        
        self.NETWORK_INTERFACE_GRAPHS: dict[str, CWTM_NetworkInterfaceGraphProperties] = {}
        self.NETWORK_INTERFACE_LINK_SPEEDS: dict[str, str] = {}

        self.NET_T_NETWORKING_LIST_TABLE_UPDATE_FREQUENCY: CWTM_GlobalUpdateIntervals = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL
        self.NET_T_NETWORK_USAGE_GRID_SIZE: int = 8 # 200:8 ratio
        self.NET_T_NETWORK_USAGE_X_RANGE: int = 200 # 200:8 ratio 

        self.parent.tm_view_menu_nas_bytes_sent.triggered.connect(
            self.clear_all_disabled_networking_byte_lines)
        self.parent.tm_view_menu_nas_bytes_received.triggered.connect(
            self.clear_all_disabled_networking_byte_lines)
        self.parent.tm_view_menu_nas_bytes_total.triggered.connect(
            self.clear_all_disabled_networking_byte_lines)
        self.parent.tm_options_menu_show_scale.triggered.connect(
            self.hide_all_network_graph_scales)

    def setup_system_networking_interfaces(self) -> None:
        """
        Sets up and registers each network interface on the machine.
        """
        system_networking_interfaces = psutil.net_if_addrs().items()

        for interface_name, interface_info in system_networking_interfaces:
            self.register_network_interface(interface_name)

    @pyqtSlot(bool)
    def hide_all_network_graph_scales(self, checked: bool) -> None:
        """
        Hides each network interface usage scale (KB/S, MB/S) (left axis)

        Arguments:
            - checked (bool): If the hide scale checkbox is checked
        """
        for n_inteface in self.NETWORK_INTERFACE_GRAPHS.values():
            graph_plot_item = n_inteface.i_net_graph.getPlotItem()
            if not checked:
                graph_plot_item.hideAxis("left")
            else:
                graph_plot_item.showAxis("left")

    def register_network_interface(self, interface_name: str) -> None:
        """
        Registers a network interface based on its interface name. This function is responsible for adding
        a resource graphical widget which represents the passed network interface usage to the list of global
        registered network interfaces (NETWORK_INTERFACE_GRAPHS, NETWORK_INTERFACE_LINK_SPEEDS).

        Arguments:
            - interface_name (str): The short interface name (e.g lo, eth0, wlo1, docker0)
        """
        interface_full_name: str = sys_utils.get_interface_type_full_name(
                interface_name
            ) + f" ({interface_name})" # e.g: Local Area Connection (lo)

        network_interface_graph: CWTM_NetworkInterfaceGraphProperties = \
            self._network_create_interface_resource_graph(interface_full_name)
        network_interface_graph.i_net_full_name: str = interface_full_name
        
        self.NETWORK_INTERFACE_GRAPHS[interface_name]: CWTM_NetworkInterfaceGraphProperties = network_interface_graph
        self.NETWORK_INTERFACE_LINK_SPEEDS[interface_name]: str = sys_utils.get_network_interface_link_speed(
            interface_name)

        self.parent.net_t_vbox_layout.addWidget(network_interface_graph.i_net_groupbox)
        self.update_networking_page_net_list_table(interface_full_name)

    @pyqtSlot(str)
    def unregister_disconnected_network_interface(self, interface_name: str) -> None:
        """
        Unregisters a network interface based on its interface name. This function is responsible for removing the
        registered network interface from the list of global registered network interfaces and then removing their
        corresponding resource graphical widget from the QVBoxLayout.

        Arguments:
            - interface_name (str): The short interface name (e.g lo, eth0, wlo1, docker0)
        """
        network_interface_graph: CWTM_NetworkInterfaceGraphProperties = self.NETWORK_INTERFACE_GRAPHS[interface_name]
        self.parent.net_t_vbox_layout.removeWidget(network_interface_graph.i_net_groupbox)
        self.refresh_networking_page_net_list_table()

        del self.NETWORK_INTERFACE_GRAPHS[interface_name]
        del self.NETWORK_INTERFACE_LINK_SPEEDS[interface_name]

    def refresh_networking_page_net_list_table(self) -> None:
        """
        Refreshes the registered network interface information table consisting of their:
            - Interface Name
            - Network Utilization
            - Link Speed
            - Network State (Connected or Disconnected)

        """
        with CWTM_TableWidgetUpdateInitializer(self.parent.net_t_network_list_table):
            system_networking_interfaces: tuple[str, list] = psutil.net_if_addrs().items()

            for interface_name, interface_info in system_networking_interfaces:
                interface_full_name: str = sys_utils.get_interface_type_full_name(
                    interface_name
                ) + f" ({interface_name})" # Local Area Connection (lo)

                self.update_networking_page_net_list_table(interface_full_name)

    @pyqtSlot()
    def clear_all_disabled_networking_byte_lines(self) -> None:
        """
        Clears the byte lines for each network interface graph based on their checked value
        """
        for n_interface in self.NETWORK_INTERFACE_GRAPHS.values():
            if not self.parent.tm_view_menu_nas_bytes_sent.isChecked():
                n_interface.i_net_sent_plot_item.clear()
            if not self.parent.tm_view_menu_nas_bytes_received.isChecked():
                n_interface.i_net_recv_plot_item.clear()
            if not self.parent.tm_view_menu_nas_bytes_total.isChecked():
                n_interface.i_net_total_plot_item.clear()

    @pyqtSlot(CWTM_NetworkInterfaceUsagePacket)
    def update_networking_page(self, network_usage_frame: CWTM_NetworkInterfaceUsagePacket):
        """

        Arguments:
            - network_usage_frame (CWTM_NetworkInterfaceUsagePacket): 
                Contains network usage data (bytes recv, bytes sent...) for a network interface.
        """
        if (n_interface := network_usage_frame.i_net_name) not in self.NETWORK_INTERFACE_GRAPHS:
            self.register_network_interface(n_interface)

        network_interface_graph: CWTM_NetworkInterfaceGraphProperties = self.NETWORK_INTERFACE_GRAPHS[n_interface]
        
        network_interface_graph.i_net_graph.update_plot(
            network_interface_graph.i_net_sent_plot_item, 
            network_usage_frame.i_net_bytes_sent if self.parent.tm_view_menu_nas_bytes_sent.isChecked() else 0,
            network_interface_graph.i_net_sent_data_x, network_interface_graph.i_net_sent_data_y
        )
        network_interface_graph.i_net_graph.update_plot(
            network_interface_graph.i_net_recv_plot_item, 
            network_usage_frame.i_net_bytes_received if self.parent.tm_view_menu_nas_bytes_received.isChecked() else 0,
            network_interface_graph.i_net_recv_data_x, network_interface_graph.i_net_recv_data_y
        )
        network_interface_graph.i_net_graph.update_plot(
            network_interface_graph.i_net_total_plot_item, 
            network_usage_frame.i_net_bytes_received + network_usage_frame.i_net_bytes_sent \
                if self.parent.tm_view_menu_nas_bytes_total.isChecked() else 0,
            network_interface_graph.i_net_total_data_x, network_interface_graph.i_net_total_data_y
        )

        *graph_equal_ticks, = network_interface_graph.i_net_graph.get_equal_tick_spacing(4)
        self.set_networking_speed_unit_ticks(
            network_interface_graph.i_net_graph, graph_equal_ticks)

        if n_interface == list(self.NETWORK_INTERFACE_GRAPHS.keys())[0]:
            self.parent.net_t_network_list_table.setRowCount(0)

        self.set_network_interface_table_information(
            network_interface_graph.i_net_graph, 
            network_usage_frame.i_net_bytes_sent, 
            network_usage_frame.i_net_bytes_received, 
            n_interface, 
            network_interface_graph.i_net_full_name
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
            interface_full_name, total_net_utilization_label, 
            self.NETWORK_INTERFACE_LINK_SPEEDS[interface_name], 
            network_interface_is_connected_label
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

    def _network_create_interface_resource_graph(self, interface_full_name: str) -> CWTM_NetworkInterfaceGraphProperties:
        interface_net_graph = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=False, show_left_values=True,
            dotted_grid_lines=self.parent.old_style,
            grid_size_x=self.NET_T_NETWORK_USAGE_GRID_SIZE
        )
        net_grid_usage_sent_data_x, net_grid_usage_sent_data_y = \
            interface_net_graph.get_all_data_axes(self.NET_T_NETWORK_USAGE_X_RANGE)
        net_grid_usage_recv_data_x, net_grid_usage_recv_data_y = \
            interface_net_graph.get_all_data_axes(self.NET_T_NETWORK_USAGE_X_RANGE)
        net_grid_usage_total_data_x, net_grid_usage_total_data_y = \
            interface_net_graph.get_all_data_axes(self.NET_T_NETWORK_USAGE_X_RANGE)
        net_grid_usage_sent_plot_item = interface_net_graph.plot(
            net_grid_usage_sent_data_x, net_grid_usage_sent_data_y,
            pen=pyqtgraph.mkPen(
                color=CWTM_NetworkingBytesLabelsColours.BYTES_LABEL_BYTES_SENT, width=1)
        )
        net_grid_usage_recv_plot_item = interface_net_graph.plot(
            net_grid_usage_recv_data_x, net_grid_usage_recv_data_y,
            pen=pyqtgraph.mkPen(
                color=CWTM_NetworkingBytesLabelsColours.BYTES_LABEL_BYTES_RECEIVED, width=1)
        )
        net_grid_usage_total_plot_item = interface_net_graph.plot(
            net_grid_usage_total_data_x, net_grid_usage_total_data_y,
            pen=pyqtgraph.mkPen(
                color=CWTM_NetworkingBytesLabelsColours.BYTES_LABEL_BYTES_TOTAL, width=1)
        )
        interface_net_groupbox = self.add_full_size_widget_to_groupbox(
            interface_full_name, interface_net_graph
        )

        return CWTM_NetworkInterfaceGraphProperties(
            interface_net_graph, interface_net_groupbox,
            net_grid_usage_sent_data_x, net_grid_usage_sent_data_y,
            net_grid_usage_recv_data_x, net_grid_usage_recv_data_y,
            net_grid_usage_total_data_x, net_grid_usage_total_data_y,
            net_grid_usage_sent_plot_item, net_grid_usage_recv_plot_item,
            net_grid_usage_total_plot_item)

    def update_refresh_networking_page_resource_graphs(self):
        self.networking_interface_retrieval_worker.get_networking_interface_usage_loop(disable_loop=True)

    def start_networking_page_updater_thread(self):
        self.networking_interface_retrieval_thread = QThread()
        self.networking_interface_retrieval_worker = \
            CWTM_NetworkingInterfaceRetrievalWorker(
                timeout_interval=self.NET_T_NETWORKING_LIST_TABLE_UPDATE_FREQUENCY)
        self.networking_page_update_handler = CWTM_GlobalUpdateIntervalHandler(
            self.parent, thread_worker=self.networking_interface_retrieval_worker)
        self.networking_page_update_handler.register_selected_tab_update_interval_handler(
            refresh_function=self.update_refresh_networking_page_resource_graphs)  

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
        
        self.networking_interface_retrieval_thread.start()
