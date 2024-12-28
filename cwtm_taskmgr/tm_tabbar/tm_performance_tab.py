import copy
import math
import psutil
import pyqtgraph

from .. import sys_utils
from ..qt_widgets import (
    CWTM_ResourceLevelBarWidget,
    CWTM_ResourceGraphWidget
)
from ..qt_components import (
    CWTM_TableWidgetController,
    CWTM_GlobalUpdateIntervalHandler
)
from .core_properties import (
    CWTM_ResourceLevelBarParameters,
    CWTM_GlobalUpdateIntervals,
    CWTM_ResourceBarLevelColours
)
from ..thread_workers import CWTM_PerformanceInfoRetrievalWorker

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt, QTimer, QThread, QMetaObject
from PyQt5.QtGui import QColor


class CWTM_PerformanceTab(CWTM_TableWidgetController):
    def __init__(self, parent):
        self.parent = parent

        self.PERF_RESOURCE_USAGE_HISTORY_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL

        self.PERF_RESOURCE_USAGE_TOTAL_BARS = 20
        self.PERF_RESOURCE_USAGE_BAR_HEIGHT = 1
        self.PERF_RESOURCE_USAGE_BAR_WIDTH = 20
        self.PERF_RESOURCE_USAGE_BAR_SPACING = 2
        self.PERF_RESOURCE_USAGE_GRID_SIZE = 8 # 200:8 ratio
        self.PERF_RESOURCE_USAGE_X_RANGE = 200 # 200:8 ratio 

        self.PERF_CPU_USAGE_HISTORY_GRAPHS = []
        self.graphing_mode_per_cpu = False

        self.cpu_usage_history_layout = QHBoxLayout()
        self.parent.perf_cpu_usage_history.setLayout(
            self.cpu_usage_history_layout
        )

        self.show_kernel_times = False

    def setup_performance_tab_bars(self):
        cpu_resource_bar_parameters = CWTM_ResourceLevelBarParameters(
            x_offset=self.parent.perf_cpu_usage.size().width(),
            y_offset=self.parent.perf_cpu_usage.size().height(),
            total_bars=self.PERF_RESOURCE_USAGE_TOTAL_BARS,
            bar_height=self.PERF_RESOURCE_USAGE_BAR_HEIGHT,
            bar_width=self.PERF_RESOURCE_USAGE_BAR_WIDTH,
            spacing=self.PERF_RESOURCE_USAGE_BAR_SPACING,
            resource_bar_label="%"
        )
        
        cpu_usage_bar_layout = QVBoxLayout()
        self.parent.perf_cpu_usage.setLayout(cpu_usage_bar_layout)
        self.cpu_bar_widget = CWTM_ResourceLevelBarWidget(
            bar_parameters=cpu_resource_bar_parameters
        )
        self.cpu_bar_widget.setFixedSize(
            self.parent.perf_cpu_usage.size().width() - 15, # margin
            self.parent.perf_cpu_usage.size().height() - 30 # margin
        )

        cpu_usage_bar_layout.addWidget(self.cpu_bar_widget)

        memory_usage_bar_layout = QVBoxLayout()
        _, total_memory_available_unit = sys_utils.get_memory_size_info(
            psutil.virtual_memory().total
        )
        mem_resource_bar_parameters = copy.deepcopy(cpu_resource_bar_parameters)
        mem_resource_bar_parameters.resource_bar_label = total_memory_available_unit
        mem_resource_bar_parameters.x_offset = self.parent.perf_mem_usage.size().width()
        mem_resource_bar_parameters.y_offset = self.parent.perf_mem_usage.size().height()
        
        self.parent.perf_mem_usage.setLayout(memory_usage_bar_layout)
        self.memory_bar_widget = CWTM_ResourceLevelBarWidget(
            bar_parameters=mem_resource_bar_parameters
        )
        self.memory_bar_widget.setFixedSize(
            self.parent.perf_mem_usage.size().width() - 15, # margin
            self.parent.perf_mem_usage.size().height() - 30 # margin
        )

        memory_usage_bar_layout.addWidget(self.memory_bar_widget)

    def setup_performance_tab_menu_bar_slots(self):
        self.parent.tm_view_menu_cpu_one_graph_all_cpus.triggered.connect(
            self.switch_to_all_cpu_graphing)
        self.parent.tm_view_menu_cpu_one_graph_per_cpu.triggered.connect(
            self.switch_to_per_cpu_graphing)
        self.parent.tm_view_menu_show_kernel_times.triggered.connect(
            self.update_show_kernel_times_setting)

    def update_show_kernel_times_setting(self):
        if self.show_kernel_times:
            self.clear_kernel_time_resource_graph_lines()
        self.show_kernel_times = not self.show_kernel_times

    def clear_kernel_time_resource_graph_lines(self):
        for registered_cpu in self.PERF_CPU_USAGE_HISTORY_GRAPHS:
            (_, _, _, _, _, _, _, _, 
                cpu_grid_kernel_usage_plot_item) = registered_cpu
            cpu_grid_kernel_usage_plot_item.clear()

    def update_refresh_performance_page(self):
        self.performance_page_worker.get_all_resource_usage_loop(disable_loop=True)

    def register_cpu_core(self, *, per_cpu=False):
        cpu_core_count = psutil.cpu_count()
        grid_size_x = self.PERF_RESOURCE_USAGE_GRID_SIZE \
            if not self.graphing_mode_per_cpu \
            else self.PERF_RESOURCE_USAGE_GRID_SIZE // (cpu_core_count / 2)
        cpu_grid_widget = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=True, 
            dotted_grid_lines=self.parent.old_style, grid_size_x=grid_size_x,
        )
        cpu_graph_x_range = self.PERF_RESOURCE_USAGE_X_RANGE \
            if not per_cpu else self.PERF_RESOURCE_USAGE_X_RANGE // (cpu_core_count * 2)
        cpu_grid_usage_data_x, cpu_grid_usage_data_y = \
            cpu_grid_widget.get_all_data_axes(x_range=cpu_graph_x_range)
        cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y = \
            cpu_grid_widget.get_all_data_axes(x_range=cpu_graph_x_range)
        cpu_grid_usage_plot_pen = pyqtgraph.mkPen(color="g", width=1)
        cpu_grid_kernel_usage_plot_pen = pyqtgraph.mkPen(color="r", width=1)
        cpu_grid_usage_plot_item = cpu_grid_widget.plot(
            cpu_grid_usage_data_x, cpu_grid_usage_data_y,
            pen=cpu_grid_usage_plot_pen
        )
        cpu_grid_kernel_usage_plot_item = cpu_grid_widget.plot(
            cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y,
            pen=cpu_grid_kernel_usage_plot_pen
        )

        self.PERF_CPU_USAGE_HISTORY_GRAPHS.append((
            cpu_grid_widget, 
            cpu_grid_usage_data_x, cpu_grid_usage_data_y,
            cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y,
            cpu_grid_usage_plot_pen, cpu_grid_kernel_usage_plot_pen, 
            cpu_grid_usage_plot_item, cpu_grid_kernel_usage_plot_item
        ))

        return cpu_grid_widget

    def switch_to_per_cpu_graphing(
        self, *, no_graphing_mode_check=False, include_thread_switch=True):
        if self.graphing_mode_per_cpu and not no_graphing_mode_check:
            return

        if include_thread_switch:
            self.performance_page_worker.perf_sig_request_per_cpu_status_change.emit(True)

        self.setup_switch_cpu_graphing_modes(per_cpu=True)
        for _ in range(psutil.cpu_count()):
            self.cpu_usage_history_layout.addWidget(self.register_cpu_core(per_cpu=True))

    def switch_to_all_cpu_graphing(
        self, *, no_graphing_mode_check=False, include_thread_switch=True):
        if not self.graphing_mode_per_cpu and not no_graphing_mode_check:
            return

        if include_thread_switch:
            self.performance_page_worker.perf_sig_request_per_cpu_status_change.emit(False)
            
        self.setup_switch_cpu_graphing_modes(per_cpu=False)
        self.cpu_usage_history_layout.addWidget(self.register_cpu_core())

    def setup_switch_cpu_graphing_modes(self, *, per_cpu):
        self.graphing_mode_per_cpu = per_cpu
        self.PERF_CPU_USAGE_HISTORY_GRAPHS.clear()

        for cpu_core in reversed(range(self.cpu_usage_history_layout.count())): 
            self.cpu_usage_history_layout.itemAt(cpu_core).widget().setParent(None)

    def setup_performance_tab_graphs(self):
        self.switch_to_all_cpu_graphing(
            no_graphing_mode_check=True, include_thread_switch=False
        ) # since the thread has not been initialized yet

        memory_usage_history_layout = QVBoxLayout()
        self.parent.perf_mem_usage_history.setLayout(
            memory_usage_history_layout
        )
        self.memory_grid_widget = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=True, 
            dotted_grid_lines=self.parent.old_style, 
            grid_size_x=self.PERF_RESOURCE_USAGE_GRID_SIZE
        )
        self.mem_grid_usage_data_x, self.mem_grid_usage_data_y = \
                                    self.memory_grid_widget.get_all_data_axes(
                                        self.PERF_RESOURCE_USAGE_X_RANGE)
        self.mem_grid_usage_plot_pen = pyqtgraph.mkPen(color="#007FFD", width=2)
        self.mem_grid_usage_plot_item = self.memory_grid_widget.plot(
            self.mem_grid_usage_data_x, self.mem_grid_usage_data_y,
            pen=self.mem_grid_usage_plot_pen
        )
        memory_usage_history_layout.addWidget(self.memory_grid_widget)

    def update_system_memory_labels(
            self, n_file_descriptors, n_sys_threads, n_sys_processes,
            total_system_uptime, total_system_mem_commit
        ):
        self.parent.perf_system_handles_value.setText(str(n_file_descriptors))
        self.parent.perf_system_threads_value.setText(str(n_sys_threads))
        self.parent.perf_system_processes_value.setText(str(n_sys_processes))
        self.parent.perf_system_up_time_value.setText(total_system_uptime)
        self.parent.perf_system_commit_value.setText(total_system_mem_commit)
        
    def update_kernel_memory_labels(self, sys_swap_memory):
        memory_paged_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            sys_swap_memory.used)[:-2]
        memory_non_paged_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            sys_swap_memory.free)[:-2]

        self.parent.perf_kernel_mem_paged_value.setText(
            memory_paged_no_label_mb)
        self.parent.perf_kernel_mem_non_paged_value.setText(
            memory_non_paged_no_label_mb)

    def update_physical_memory_labels(self, virtual_memory):        
        memory_total_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.total)[:-2] # truncate MB label
        memory_cached_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.cached)[:-2] # truncate MB label
        memory_available_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.available)[:-2] # truncate MB label
        memory_free_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.free)[:-2] # truncate MB label

        self.parent.perf_physical_mem_total_value.setText(
            memory_total_no_label_mb)
        self.parent.perf_physical_mem_cached_value.setText(
            memory_cached_no_label_mb)
        self.parent.perf_physical_mem_available_value.setText(
            memory_available_no_label_mb)
        self.parent.perf_physical_mem_free_value.setText(
            memory_free_no_label_mb)

    def update_status_bar_labels(self, n_processes, v_mem_percent, cpu_usage):        
        self.parent.status_bar_processes_label.setText(
            f"Processes: {n_processes}")
        self.parent.status_bar_cpu_usage_label.setText(
            f"CPU Usage: {cpu_usage}%")
        self.parent.status_bar_physical_memory_label.setText(
            f"Physical Memory: {v_mem_percent}%")

    def update_cpu_usage_history_graphs(self, current_cpu_usage, current_cpu_kernel_usage):
        for cpu_core, (cpu_usage, kernel_cpu_usage) in enumerate(
            zip(current_cpu_usage, current_cpu_kernel_usage)):
            (cpu_grid_widget, 
                cpu_grid_usage_data_x, cpu_grid_usage_data_y,
                cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y,
                cpu_grid_usage_plot_pen, cpu_grid_kernel_usage_plot_pen, 
                cpu_grid_usage_plot_item, cpu_grid_kernel_usage_plot_item
            ) = self.PERF_CPU_USAGE_HISTORY_GRAPHS[cpu_core]

            cpu_grid_widget.update_plot(
                cpu_grid_usage_plot_item, cpu_usage,
                cpu_grid_usage_data_x, cpu_grid_usage_data_y)

            cpu_grid_widget.update_plot(
                cpu_grid_kernel_usage_plot_item, 
                kernel_cpu_usage if self.show_kernel_times else 0,
                cpu_grid_kernel_usage_data_x, cpu_grid_kernel_usage_data_y)

    def update_graphical_widgets(
        self, current_cpu_usage, current_kernel_usage, 
        current_memory_usage, memory_used, memory_total):
        current_kernel_usage = current_kernel_usage \
            if self.show_kernel_times else 0
        self.cpu_bar_widget.set_resource_value(
            current_cpu_usage, current_kernel_usage, 100,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_FILLED,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_EMPTY,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_KERNEL_USAGE_TIME_FILLED,
            QColor(0, 0, 0))
        self.memory_bar_widget.set_resource_value(
            memory_used, None, memory_total,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_FILLED,
            CWTM_ResourceBarLevelColours.BAR_COLOUR_CPU_USAGE_TIME_EMPTY,
            None, None)

        self.memory_grid_widget.update_plot(
            self.mem_grid_usage_plot_item, current_memory_usage,
            self.mem_grid_usage_data_x, self.mem_grid_usage_data_y
        )

    def start_performance_page_updater_thread(self):
        self.performance_page_thread = QThread()
        self.performance_page_worker = CWTM_PerformanceInfoRetrievalWorker(
            timeout_interval=self.PERF_RESOURCE_USAGE_HISTORY_UPDATE_FREQUENCY,
            per_cpu=self.graphing_mode_per_cpu
        )
        self.performance_page_update_handler = CWTM_GlobalUpdateIntervalHandler(
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
            self.update_graphical_widgets)

        self.performance_page_worker.moveToThread(
            self.performance_page_thread)
        self.performance_page_thread.started.connect(
            self.performance_page_worker.run)
        self.performance_page_thread.start()
