import copy
import psutil
import pyqtgraph

from .. import sys_utils
from ..qt_widgets import (
    CWTM_ResourceLevelBarWidget,
    CWTM_ResourceGraphWidget
)
from ..qt_components import CWTM_TabManager
from .core_properties import CWTM_ResourceLevelBarParameters

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor


class CWTM_PerformanceTab(CWTM_TabManager):
    def __init__(self, parent):
        self.parent = parent

        self.PERF_RESOURCE_USAGE_HISTORY_UPDATE_FREQUENCY = 1000

        self.PERF_RESOURCE_USAGE_TOTAL_BARS = 20
        self.PERF_RESOURCE_USAGE_BAR_HEIGHT = 1
        self.PERF_RESOURCE_USAGE_BAR_WIDTH = 20
        self.PERF_RESOURCE_USAGE_BAR_SPACING = 2

        self.PERF_CPU_USAGE_HISTORY_GRAPHS = []
        self.GRAPHING_MODE_PER_CPU = False

        self.cpu_usage_history_layout = QHBoxLayout()
        self.parent.perf_cpu_usage_history.setLayout(
            self.cpu_usage_history_layout
        )
        self.parent.tm_view_menu_cpuh_one_graph_all_cpus.triggered.connect(
            self.switch_to_all_cpu_graphing)
        self.parent.tm_view_menu_cpuh_one_graph_per_cpu.triggered.connect(
            self.switch_to_per_cpu_graphing)

    def setup_performance_tab_bars(self):
        cpu_resource_bar_parameters = CWTM_ResourceLevelBarParameters(
            x_offset=self.parent.perf_cpu_usage.size().width(),
            y_offset=self.parent.perf_cpu_usage.size().height(),
            total_bars=self.PERF_RESOURCE_USAGE_TOTAL_BARS,
            bar_height=self.PERF_RESOURCE_USAGE_BAR_HEIGHT,
            bar_width=self.PERF_RESOURCE_USAGE_BAR_WIDTH,
            bar_colour=QColor(0, 255, 0),
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

    def register_cpu_core(self):
        cpu_core_count = psutil.cpu_count()
        cpu_grid_widget = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=True, dotted_grid_lines=self.parent.old_style,
            grid_size_x=4 if not self.GRAPHING_MODE_PER_CPU else 4 * cpu_core_count,
        )
        cpu_grid_usage_data_x, cpu_grid_usage_data_y = \
                                    cpu_grid_widget.get_all_data_axes()
        cpu_grid_usage_plot_pen = pyqtgraph.mkPen(color="g", width=1)
        cpu_grid_usage_plot_item = cpu_grid_widget.plot(
            cpu_grid_usage_data_x, cpu_grid_usage_data_y,
            pen=cpu_grid_usage_plot_pen
        )

        self.PERF_CPU_USAGE_HISTORY_GRAPHS.append((
            cpu_grid_widget, cpu_grid_usage_data_x, cpu_grid_usage_data_y,
            cpu_grid_usage_plot_pen, cpu_grid_usage_plot_item
        ))

        return cpu_grid_widget


    def switch_to_per_cpu_graphing(self, *, no_graphing_mode_check=False):
        if self.GRAPHING_MODE_PER_CPU and not no_graphing_mode_check:
            return

        self._setup_switch_cpu_graphing_modes(per_cpu=True)
        for _ in range(psutil.cpu_count()):
            self.cpu_usage_history_layout.addWidget(self.register_cpu_core())

    def switch_to_all_cpu_graphing(self, *, no_graphing_mode_check=False):
        if not self.GRAPHING_MODE_PER_CPU and not no_graphing_mode_check:
            return
            
        self._setup_switch_cpu_graphing_modes(per_cpu=False)
        self.cpu_usage_history_layout.addWidget(self.register_cpu_core())

    def _setup_switch_cpu_graphing_modes(self, *, per_cpu):
        self.GRAPHING_MODE_PER_CPU = per_cpu
        self.PERF_CPU_USAGE_HISTORY_GRAPHS.clear()

        for cpu_core in reversed(range(self.cpu_usage_history_layout.count())): 
            self.cpu_usage_history_layout.itemAt(cpu_core).widget().setParent(None)


    def setup_performance_tab_graphs(self):
        self.switch_to_all_cpu_graphing(no_graphing_mode_check=True)

        memory_usage_history_layout = QVBoxLayout()
        self.parent.perf_mem_usage_history.setLayout(
            memory_usage_history_layout
        )
        self.memory_grid_widget = CWTM_ResourceGraphWidget(
            grid_color='g', percentage=True, dotted_grid_lines=self.parent.old_style
        )
        self.mem_grid_usage_data_x, self.mem_grid_usage_data_y = \
                                    self.memory_grid_widget.get_all_data_axes()
        self.mem_grid_usage_plot_pen = pyqtgraph.mkPen(color="#007FFD", width=2)
        self.mem_grid_usage_plot_item = self.memory_grid_widget.plot(
            self.mem_grid_usage_data_x, self.mem_grid_usage_data_y,
            pen=self.mem_grid_usage_plot_pen
        )
        memory_usage_history_layout.addWidget(self.memory_grid_widget)

    def update_system_memory_labels(self, total_processes, virtual_memory):
        n_file_descriptors = sys_utils.get_number_of_handle_file_descriptors()
        n_sys_threads = sys_utils.get_number_of_total_threads(total_processes)
        n_sys_processes = len(total_processes)
        commit_mem_total, commit_mem_amount = sys_utils.get_total_system_commit_memory(
            virtual_memory
        )
        total_system_mem_commit = " / ".join(
            (sys_utils.convert_proc_mem_b_to_mb(commit_mem_amount)[:-2],
             sys_utils.convert_proc_mem_b_to_mb(commit_mem_total)[:-2])
        )
        total_system_uptime = sys_utils.format_seconds_to_timestamp(
            sys_utils.get_total_uptime_in_seconds()
        )

        self.parent.perf_system_handles_value.setText(str(n_file_descriptors))
        self.parent.perf_system_threads_value.setText(str(n_sys_threads))
        self.parent.perf_system_processes_value.setText(str(n_sys_processes))
        self.parent.perf_system_up_time_value.setText(total_system_uptime)
        self.parent.perf_system_commit_value.setText(total_system_mem_commit)
        
    def update_kernel_memory_labels(self, sys_swap_memory):
        memory_paged_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            sys_swap_memory.used
        )[:-2]
        memory_non_paged_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            sys_swap_memory.free
        )[:-2]

        self.parent.perf_kernel_mem_paged_value.setText(
            memory_paged_no_label_mb
        )
        self.parent.perf_kernel_mem_non_paged_value.setText(
            memory_non_paged_no_label_mb
        )

    def update_physical_memory_labels(self, virtual_memory):        
        memory_total_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.total
        )[:-2] # truncate MB label
        memory_cached_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.cached
        )[:-2] # truncate MB label
        memory_available_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.available
        )[:-2] # truncate MB label
        memory_free_no_label_mb = sys_utils.convert_proc_mem_b_to_mb(
            virtual_memory.free
        )[:-2] # truncate MB label

        self.parent.perf_physical_mem_total_value.setText(
            memory_total_no_label_mb
        )
        self.parent.perf_physical_mem_cached_value.setText(
            memory_cached_no_label_mb
        )
        self.parent.perf_physical_mem_available_value.setText(
            memory_available_no_label_mb
        )
        self.parent.perf_physical_mem_free_value.setText(
            memory_free_no_label_mb
        )

    def update_status_bar_labels(self, n_processes, v_mem_percent, cpu_usage):        
        self.parent.status_bar_processes_label.setText(
            f"Processes: {n_processes}"
        )
        self.parent.status_bar_cpu_usage_label.setText(
            f"CPU Usage: {cpu_usage}%"
        )
        self.parent.status_bar_physical_memory_label.setText(
            f"Physical Memory: {v_mem_percent}%"
        )

    def update_cpu_usage_history_graphs(self):
        current_cpu_usage = [psutil.cpu_percent()] if not self.GRAPHING_MODE_PER_CPU \
                                else psutil.cpu_percent(percpu=True)

        for cpu_core, cpu_usage in enumerate(current_cpu_usage):
            (cpu_grid_widget, 
                cpu_grid_usage_data_x, cpu_grid_usage_data_y,
                cpu_grid_usage_plot_pen, cpu_grid_usage_plot_item
            ) = self.PERF_CPU_USAGE_HISTORY_GRAPHS[cpu_core]

            cpu_grid_widget.update_plot(
                cpu_grid_usage_plot_item, cpu_usage,
                cpu_grid_usage_data_x, cpu_grid_usage_data_y
            )

    def update_all_resource_usage(self):
        current_memory_info = psutil.virtual_memory()
        sys_swap_memory = psutil.swap_memory()
        *total_iter_processes, = psutil.process_iter()
        current_cpu_usage = psutil.cpu_percent()
        
        current_memory_usage = current_memory_info.percent

        self.update_physical_memory_labels(current_memory_info)
        self.update_kernel_memory_labels(sys_swap_memory)
        self.update_system_memory_labels(
            total_iter_processes, current_memory_info
        )
        self.update_status_bar_labels(
            len(total_iter_processes), current_memory_usage, current_cpu_usage
        )

        memory_total, _ = sys_utils.get_memory_size_info(
            current_memory_info.total
        )
        memory_used, _ = sys_utils.get_memory_size_info(
            current_memory_info.used
        )

        self.cpu_bar_widget.set_resource_value(current_cpu_usage, 100)
        self.memory_bar_widget.set_resource_value(memory_used, memory_total)

        self.update_cpu_usage_history_graphs()
        self.memory_grid_widget.update_plot(
            self.mem_grid_usage_plot_item, current_memory_usage,
            self.mem_grid_usage_data_x, self.mem_grid_usage_data_y
        )

    def start_performance_page_updater(self):
        self.update_all_resource_usage()
        
        self.performance_update_timer = QTimer()
        self.performance_update_timer.timeout.connect(
            self.update_all_resource_usage
        )
        self.performance_update_timer.start(
            self.PERF_RESOURCE_USAGE_HISTORY_UPDATE_FREQUENCY
        )
