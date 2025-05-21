import copy
import math
import psutil
import pyqtgraph

from PyQt5.QtCore import (
    Qt, 
    QThread, 
    pyqtSlot, 
    QObject
)
from PyQt5.QtGui import (
    QColor, 
    QPen
)
from PyQt5.QtWidgets import (
    QVBoxLayout, 
    QHBoxLayout
)

from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem

from .. import sys_utils
from ..qt_widgets import (
    CWTM_ResourceLevelBarWidget,
    CWTM_ResourceGraphWidget
)
from ..qt_components import (
    CWTM_TableWidgetController,
    CWTM_GlobalUpdateIntervalHandler
)
from ..core_properties import (
    CWTM_ResourceLevelBarParameters,
    CWTM_GlobalUpdateIntervals,
    CWTM_ResourceBarLevelColours,
    CWTM_TabWidgetColumnEnum,
    CWTM_PerformanceResourceGraphWidgetProperties,
    CWTM_PerformanceStatusBarLabelsPacket,
    CWTM_PerformanceGraphCPUUsagePacket,
    CWTM_PerformanceSystemMemoryLabelsPacket,
    CWTM_PerformanceGraphicalWidgetsPacket
)
from ..thread_workers import CWTM_PerformanceInfoRetrievalWorker


class CWTM_PerformanceTab(QObject, CWTM_TableWidgetController):
    def __init__(self, *args: list, parent: QObject, **kwargs: dict) -> None:
        """
        Initializes the performance tab for the task manager. This function sets up all the properties for
        the performance tab including the:
            - The update interval speed based on the enum properties of CWTM_GlobalUpdateIntervals.
            - The graphical performance widgets sizes and properties.

        Arguments:
            - args and kwargs: any arbitrary extra argument/keywork arguments to be passed into the
                main superclass. (QObject)
            - parent (QObject): Initialize the class with the parent as a property the superclass. 
        """
        super().__init__(*args, parent=parent, **kwargs)

        self.parent: QObject = parent

        self.PERF_RESOURCE_USAGE_HISTORY_UPDATE_FREQUENCY: CWTM_GlobalUpdateIntervals = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL

        self.PERF_RESOURCE_USAGE_TOTAL_BARS: int = 20
        self.PERF_RESOURCE_USAGE_BAR_HEIGHT: int = 1
        self.PERF_RESOURCE_USAGE_BAR_WIDTH: int = 20
        self.PERF_RESOURCE_USAGE_BAR_SPACING: int = 2
        self.PERF_RESOURCE_USAGE_GRID_SIZE: int = 8 # 200:8 ratio
        self.PERF_RESOURCE_USAGE_X_RANGE: int = 200 # 200:8 ratio 

        self.PERF_CPU_USAGE_HISTORY_GRAPHS: list = []
        self.graphing_mode_per_cpu: bool = False

        self.cpu_usage_history_layout: QHBoxLayout = QHBoxLayout()
        self.parent.perf_cpu_usage_history.setLayout(
            self.cpu_usage_history_layout
        )

        self.show_kernel_times: bool = False
        self.cpu_core_count: int = psutil.cpu_count()

        # Menubar Actions
        self.parent.tm_view_menu_cpu_one_graph_all_cpus.triggered.connect(
            self.switch_to_all_cpu_graphing)
        self.parent.tm_view_menu_cpu_one_graph_per_cpu.triggered.connect(
            self.switch_to_per_cpu_graphing)
        self.parent.tm_view_menu_show_kernel_times.triggered.connect(
            self.update_show_kernel_times_setting)

    def setup_performance_tab_graphs(self) -> None:
        """
        Sets up the performance tab resource graphical widgets
        """
        self.switch_to_all_cpu_graphing(
            no_graphing_mode_check=True, include_thread_switch=False
        ) # since the thread has not been initialized yet

        memory_usage_history_layout: QVBoxLayout = QVBoxLayout()
        self.parent.perf_mem_usage_history.setLayout(
            memory_usage_history_layout
        )
        self.memory_grid_widget: CWTM_ResourceGraphWidget = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=True, 
            dotted_grid_lines=self.parent.old_style, 
            grid_size_x=self.PERF_RESOURCE_USAGE_GRID_SIZE
        )
        self.mem_grid_usage_data_x, self.mem_grid_usage_data_y = \
                                    self.memory_grid_widget.get_all_data_axes(
                                        self.PERF_RESOURCE_USAGE_X_RANGE)
        self.mem_grid_usage_plot_pen: QPen = pyqtgraph.mkPen(color="#007FFD", width=3)
        self.mem_grid_usage_plot_item: PlotDataItem = self.memory_grid_widget.plot(
            self.mem_grid_usage_data_x, self.mem_grid_usage_data_y,
            pen=self.mem_grid_usage_plot_pen
        )
        memory_usage_history_layout.addWidget(self.memory_grid_widget)

    def setup_performance_tab_bars(self) -> None:
        """
        Sets up the performance tab resource usage graphical widgets which consists of the memory usage level bar graph.
        and the cpu usage level bar graph.
        """
        cpu_resource_bar_parameters: CWTM_ResourceLevelBarParameters = CWTM_ResourceLevelBarParameters(
            x_offset=self.parent.perf_cpu_usage.size().width(),
            y_offset=self.parent.perf_cpu_usage.size().height(),
            total_bars=self.PERF_RESOURCE_USAGE_TOTAL_BARS,
            bar_height=self.PERF_RESOURCE_USAGE_BAR_HEIGHT,
            bar_width=self.PERF_RESOURCE_USAGE_BAR_WIDTH,
            spacing=self.PERF_RESOURCE_USAGE_BAR_SPACING,
            resource_bar_label="%"
        )
        
        cpu_usage_bar_layout: QVBoxLayout = QVBoxLayout()
        self.parent.perf_cpu_usage.setLayout(cpu_usage_bar_layout)
        self.cpu_bar_widget: CWTM_ResourceLevelBarWidget = CWTM_ResourceLevelBarWidget(
            bar_parameters=cpu_resource_bar_parameters
        )
        self.cpu_bar_widget.setFixedSize(
            self.parent.perf_cpu_usage.size().width() - 15, # margin
            self.parent.perf_cpu_usage.size().height() - 30 # margin
        )

        cpu_usage_bar_layout.addWidget(self.cpu_bar_widget)
        memory_usage_bar_layout: QVBoxLayout = QVBoxLayout()
        _, total_memory_available_unit = sys_utils.get_memory_size_info(
            psutil.virtual_memory().total
        )
        mem_resource_bar_parameters: CWTM_ResourceLevelBarParameters = copy.deepcopy(cpu_resource_bar_parameters)
        mem_resource_bar_parameters.resource_bar_label: str = total_memory_available_unit
        mem_resource_bar_parameters.x_offset: int = self.parent.perf_mem_usage.size().width()
        mem_resource_bar_parameters.y_offset: int = self.parent.perf_mem_usage.size().height()
        
        self.parent.perf_mem_usage.setLayout(memory_usage_bar_layout)
        self.memory_bar_widget: CWTM_ResourceLevelBarWidget = CWTM_ResourceLevelBarWidget(
            bar_parameters=mem_resource_bar_parameters
        )
        self.memory_bar_widget.setFixedSize(
            self.parent.perf_mem_usage.size().width() - 15, # margin
            self.parent.perf_mem_usage.size().height() - 30 # margin
        )

        memory_usage_bar_layout.addWidget(self.memory_bar_widget)

    @pyqtSlot()
    def update_show_kernel_times_setting(self) -> None:
        """
        Slot to process the menubar context menu action to show the cpu kernel time usage in red.
        """
        if self.show_kernel_times:
            self.clear_kernel_time_resource_graph_lines()
        self.show_kernel_times: bool = not self.show_kernel_times

    def clear_kernel_time_resource_graph_lines(self) -> None:
        """
        Clears the kernel time (red line) on each registered cpu core graphical widget.
        """
        for registered_cpu in self.PERF_CPU_USAGE_HISTORY_GRAPHS:
            registered_cpu.g_krnl_usage_plot_item.clear()

    def register_cpu_core(self, *, per_cpu: bool=False) -> CWTM_ResourceGraphWidget:
        """
        Initialize CPU core graphical resource widget and register it in the CPU core class variable list.

        Arguments:
            - per_cpu (bool): Whether it should rescale the CPU graph xrange to fit the the screen for the
                amount of CPUs on the machine.
        """
        grid_size_x: int = self.PERF_RESOURCE_USAGE_GRID_SIZE \
            if not self.graphing_mode_per_cpu \
            else self.PERF_RESOURCE_USAGE_GRID_SIZE // (self.cpu_core_count / 2)
        cpu_grid_widget: CWTM_ResourceGraphWidget = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=True, 
            dotted_grid_lines=self.parent.old_style, grid_size_x=grid_size_x,
        )
        cpu_graph_x_range: int = self.PERF_RESOURCE_USAGE_X_RANGE \
            if not per_cpu else self.PERF_RESOURCE_USAGE_X_RANGE // (self.cpu_core_count * 2)
        cpu_grid_usage_data_x, cpu_grid_usage_data_y = \
            cpu_grid_widget.get_all_data_axes(x_range=cpu_graph_x_range)
        cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y = \
            cpu_grid_widget.get_all_data_axes(x_range=cpu_graph_x_range)
        cpu_grid_usage_plot_pen: QPen = pyqtgraph.mkPen(color="g", width=1)
        cpu_grid_kernel_usage_plot_pen: QPen = pyqtgraph.mkPen(color="r", width=1)
        cpu_grid_usage_plot_item: PlotDataItem = cpu_grid_widget.plot(
            cpu_grid_usage_data_x, cpu_grid_usage_data_y,
            pen=cpu_grid_usage_plot_pen
        )
        cpu_grid_kernel_usage_plot_item: PlotDataItem = cpu_grid_widget.plot(
            cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y,
            pen=cpu_grid_kernel_usage_plot_pen
        )

        perforamance_graph_widget_properties: CWTM_PerformanceResourceGraphWidgetProperties = \
            CWTM_PerformanceResourceGraphWidgetProperties(
                cpu_grid_widget, cpu_grid_usage_data_x, cpu_grid_usage_data_y,
                cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y,
                cpu_grid_usage_plot_pen, cpu_grid_kernel_usage_plot_pen, 
                cpu_grid_usage_plot_item, cpu_grid_kernel_usage_plot_item)

        self.PERF_CPU_USAGE_HISTORY_GRAPHS.append(perforamance_graph_widget_properties)

        return cpu_grid_widget

    @pyqtSlot()
    def switch_to_per_cpu_graphing(
        self, *, no_graphing_mode_check: bool=False, include_thread_switch: bool=True) -> None:
        """
        Switches to per-cpu graphing mode. If the graphing mode is already set to per-cpu and this
        function is called, then it will exit as long as `no_graphing_mode_check` is False.

        This function is responsible for adding a graph for each registered CPU core in the graphical
        resource groupbox widget layout. 

        Arguments:
            - no_graphing_mode_check (bool): If this is set to true, it will not exit if
                the graphing mode is already set to per-cpu.
            - include_thread_switch (bool): If the thread worker should be informed of the
                graphing mode change so that it can relay proper information.

        """
        if self.graphing_mode_per_cpu and not no_graphing_mode_check:
            return

        if include_thread_switch:
            self.performance_page_worker.perf_sig_request_per_cpu_status_change.emit(True)

        self.setup_switch_cpu_graphing_modes(per_cpu=True)
        for _ in range(self.cpu_core_count):
            self.cpu_usage_history_layout.addWidget(self.register_cpu_core(per_cpu=True))

    @pyqtSlot()
    def switch_to_all_cpu_graphing(
        self, *, no_graphing_mode_check: bool=False, include_thread_switch: bool=True) -> None:
        """
        Switches to all-cpu graphing mode. If the graphing mode is already set to all-cpu and this
        function is called, then it will exit as long as `no_graphing_mode_check` is False.

        This function is responsible for adding a graph for the average usage value for the CPU cores
        on the machine.

        Arguments:
            - no_graphing_mode_check (bool): If this is set to true, it will not exit if
                the graphing mode is already set to all-cpu.
            - include_thread_switch (bool): If the thread worker should be informed of the
                graphing mode change so that it can relay proper information.

        """
        if not self.graphing_mode_per_cpu and not no_graphing_mode_check:
            return

        if include_thread_switch:
            self.performance_page_worker.perf_sig_request_per_cpu_status_change.emit(False)
            
        self.setup_switch_cpu_graphing_modes(per_cpu=False)
        self.cpu_usage_history_layout.addWidget(self.register_cpu_core())

    def setup_switch_cpu_graphing_modes(self, *, per_cpu: bool) -> None:
        """
        Clears up the resource graph(s) and their registered CPU list based on the graphing mode.

        Arguments:
            - per_cpu (bool): If the graphing mode is per-cpu
        """
        self.graphing_mode_per_cpu = per_cpu
        self.PERF_CPU_USAGE_HISTORY_GRAPHS.clear()

        for cpu_core in reversed(range(self.cpu_usage_history_layout.count())): 
            self.cpu_usage_history_layout.itemAt(cpu_core).widget().setParent(None)

    @pyqtSlot(CWTM_PerformanceSystemMemoryLabelsPacket)
    def update_system_memory_labels(
        self, system_memory_labels: CWTM_PerformanceSystemMemoryLabelsPacket) -> None:
        """
        Update the resource labels in the system groupbox.

        Arguments:
            - system_memory_labels (CWTM_PerformanceSystemMemoryLabelsPacket): The information packet
                containing the:
                - Number of open file descriptors/handles
                - Number of running threads
                - Number of running processes
                - Total system uptime
                - Total system memory commit
        """
        self.parent.perf_system_handles_value.setText(
            str(system_memory_labels.n_file_descriptors))
        self.parent.perf_system_threads_value.setText(
            str(system_memory_labels.n_sys_threads))
        self.parent.perf_system_processes_value.setText(
            str(system_memory_labels.n_sys_processes))
        self.parent.perf_system_up_time_value.setText(
            system_memory_labels.total_sys_uptime)
        self.parent.perf_system_commit_value.setText(
            system_memory_labels.total_sys_mem_commit)
        
    @pyqtSlot(psutil._common.sswap)
    def update_kernel_memory_labels(self, sys_swap_memory: psutil._common.sswap) -> None:
        """
        Update the resource labels in the kernel memory groupbox.

        Arguments:
            - sys_swap_memory (psutil._common.sswap): The sswap information containing:
                - Used system swap memory
                - Free system swap memory
        """
        memory_paged_no_label_mb: str = sys_utils.convert_proc_mem_b_to_mb(
            sys_swap_memory.used)[:-2]
        memory_non_paged_no_label_mb: str = sys_utils.convert_proc_mem_b_to_mb(
            sys_swap_memory.free)[:-2]

        self.parent.perf_kernel_mem_paged_value.setText(
            memory_paged_no_label_mb)
        self.parent.perf_kernel_mem_non_paged_value.setText(
            memory_non_paged_no_label_mb)

    @pyqtSlot(psutil._pslinux.svmem)
    def update_physical_memory_labels(self, virtual_memory: psutil._pslinux.svmem) -> None:
        """
        Update the resource labels in the physical memory groupbox.

        Arguments:
            - virtual_memory (pssutil._pslinux.svmem): The svmem information containing:
                - Total system memory
                - Cached system memory
                - Available system memory
                - Free system memory
        """
        memory_total_no_label_mb: str = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.total)[:-2] # truncate MB label
        memory_cached_no_label_mb: str = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.cached)[:-2] # truncate MB label
        memory_available_no_label_mb: str = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.available)[:-2] # truncate MB label
        memory_free_no_label_mb: str = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.free)[:-2] # truncate MB label

        self.parent.perf_physical_mem_total_value.setText(
            memory_total_no_label_mb)
        self.parent.perf_physical_mem_cached_value.setText(
            memory_cached_no_label_mb)
        self.parent.perf_physical_mem_available_value.setText(
            memory_available_no_label_mb)
        self.parent.perf_physical_mem_free_value.setText(
            memory_free_no_label_mb)

    @pyqtSlot(CWTM_PerformanceStatusBarLabelsPacket)
    def update_status_bar_labels(self, status_bar_labels: CWTM_PerformanceStatusBarLabelsPacket) -> None: 
        """
        Update the resource labels in the status bar.

        Arguments:
            - status_bar_labels (CWTM_PerformanceStatusBarLabelsPacket): The information packet containing the:
                - Number of running processes
                - Average CPU usage
                - Memory usage
        """       
        self.parent.status_bar_processes_label.setText(
            f"Processes: {status_bar_labels.n_processes}")
        self.parent.status_bar_cpu_usage_label.setText(
            f"CPU Usage: {status_bar_labels.cpu_usage}%")
        self.parent.status_bar_physical_memory_label.setText(
            f"Physical Memory: {status_bar_labels.v_mem_percent}%")

    @pyqtSlot(CWTM_PerformanceGraphCPUUsagePacket)
    def update_cpu_usage_history_graphs(self, current_system_cpu_usage: CWTM_PerformanceGraphCPUUsagePacket) -> None:
        """
        Update the cpu usage resource graphical widget(s)

        Arguments:
            - current_system_cpu_usage (CWTM_PerformanceGraphCPUUsagePacket): The information packet containing the:
                - User CPU usage
                - Kernel CPU usage
        """     
        for cpu_core, (cpu_usage, kernel_cpu_usage) in enumerate(zip(
                current_system_cpu_usage.user_cpu_usage,
                current_system_cpu_usage.kernel_cpu_usage)):

            current_registered_cpu = self.PERF_CPU_USAGE_HISTORY_GRAPHS[cpu_core]

            current_registered_cpu.g_widget_object.update_plot(
                current_registered_cpu.g_usage_plot_item, 
                cpu_usage,
                current_registered_cpu.g_usage_data_x, 
                current_registered_cpu.g_usage_data_y)

            current_registered_cpu.g_widget_object.update_plot(
                current_registered_cpu.g_krnl_usage_plot_item, 
                kernel_cpu_usage if self.show_kernel_times else 0,
                current_registered_cpu.g_krnl_usage_data_x, 
                current_registered_cpu.g_krnl_usage_data_y)

    @pyqtSlot(CWTM_PerformanceGraphicalWidgetsPacket)
    def update_resource_bar_graphs(self, graphical_widgets_resources: CWTM_PerformanceGraphicalWidgetsPacket) -> None:
        """
        Update the resource bar graphs for the CPU and memory usage.

        Arguments:
            - graphical_widgets_resources (CWTM_PerformanceGraphicalWidgetsPacket): The information packet containing the:
                - Current average CPU usage
                - Used memory
                - Total memory
                - Current memory usage
        """  
        current_kernel_usage = graphical_widgets_resources.kernel_cpu_time \
            if self.show_kernel_times else 0
        self.cpu_bar_widget.set_resource_value(
            graphical_widgets_resources.current_cpu_usage, current_kernel_usage, 100,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_FILLED,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_EMPTY,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_KERNEL_USAGE_TIME_FILLED,
            QColor(0, 0, 0))
        self.memory_bar_widget.set_resource_value(
            graphical_widgets_resources.memory_used, None, 
            graphical_widgets_resources.memory_total,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_FILLED,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_EMPTY,
            None, None)

        self.memory_grid_widget.update_plot(
            self.mem_grid_usage_plot_item, 
            graphical_widgets_resources.current_memory_usage,
            self.mem_grid_usage_data_x, self.mem_grid_usage_data_y
        )

    @pyqtSlot()
    def update_refresh_performance_page(self) -> None:
        """
        Refreshes the performance page by requesting an information retrieval from the performance's
        thread worker.
        """
        self.performance_page_worker.get_all_resource_usage_loop(disable_loop=True)

    @pyqtSlot(int)
    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the processes thread worker to emit system process information to the slot
        `update_processes_page`

        Arguments:
            - index (int): the current index of the tab widget
        """
        self.performance_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_PERFORMANCE_TAB)

    def start_performance_page_updater_thread(self):
        """
        Starts the performance page updater thread loop.
        """
        self.performance_page_thread: QThread = QThread()
        self.performance_page_worker: CWTM_PerformanceInfoRetrievalWorker = CWTM_PerformanceInfoRetrievalWorker(
            timeout_interval=self.PERF_RESOURCE_USAGE_HISTORY_UPDATE_FREQUENCY,
            per_cpu=self.graphing_mode_per_cpu
        )
        self.performance_page_update_handler: CWTM_GlobalUpdateIntervalHandler = CWTM_GlobalUpdateIntervalHandler(
            self.parent, thread_worker=self.performance_page_worker)
        self.performance_page_update_handler.register_selected_tab_update_interval_handler(
            refresh_function=self.update_refresh_performance_page)

        self.performance_page_worker.perf_sig_memory_labels_info.connect(
            self.update_physical_memory_labels)
        self.performance_page_worker.perf_sig_status_bar_labels_info.connect(
            self.update_status_bar_labels)
        self.performance_page_worker.perf_sig_cpu_usage_history_graphs_info.connect(
            self.update_cpu_usage_history_graphs)
        self.performance_page_worker.perf_sig_kernel_mem_labels_info.connect(
            self.update_kernel_memory_labels)
        self.performance_page_worker.perf_sig_sys_mem_labels_info.connect(
            self.update_system_memory_labels)

        self.performance_page_worker.perf_sig_graphical_widgets_info.connect(
            self.update_resource_bar_graphs)

        self.performance_page_worker.moveToThread(
            self.performance_page_thread)
        self.parent.task_manager_tab_widget.currentChanged.connect(
            self.update_thread_worker_info_retrieval_authorization)
        self.performance_page_thread.started.connect(
            self.performance_page_worker.run)
        self.performance_page_thread.start()
