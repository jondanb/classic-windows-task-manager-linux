import psutil
import functools

from . import sys_utils
from .tm_tabbar.core_properties import (
    CWTM_TabWidgetColumnEnum,
    CWTM_GraphUpdateIntervals
)

from PyQt5.QtCore import (
    pyqtSignal, pyqtSlot, Qt,
    QTimer, QThread, QObject
)


class CWTM_PageUpdaterWorkerThread(QObject):    
    def __init__(self, tm_update_function):
        super().__init__()
        
        self.tm_update_function = tm_update_function


class CWTM_NetworkingInterfaceRetrievalWorker(QObject):
    ni_sig_usage_frame = pyqtSignal(str, float, float)
    ni_sig_disconnect_nic = pyqtSignal(str)

    def __init__(self, timeout_interval, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_interval = timeout_interval
        self.parent = parent
        self.last_data = {}

    def run(self):
        self.networking_interface_retrieval_timer = QTimer()
        self.networking_interface_retrieval_timer.timeout.connect(
            self.get_networking_interface_usage_frames
        )
        self.networking_interface_retrieval_timer.start(self.timeout_interval)

    def check_for_disconnected_network_interface(self, network_data):
        current_network_data_set, last_network_data_set = (
            set(network_data.keys()), set(self.last_data.keys())
        )
        nic_frame_total_difference = last_network_data_set - current_network_data_set

        for nic_frame_difference in list(nic_frame_total_difference):
            del self.last_data[nic_frame_difference]
            self.ni_sig_disconnect_nic.emit(nic_frame_difference)


    def get_networking_interface_usage_frames(self):
        current_data = psutil.net_io_counters(pernic=True)
        self.check_for_disconnected_network_interface(current_data)
        self.parent.net_t_network_list_table.setRowCount(0)

        for nic, counters in current_data.items():
            if nic not in self.last_data:
                self.last_data[nic] = counters
                continue

            last_counters = self.last_data[nic]
            sent_bytes_per_interval = (
                counters.bytes_sent - last_counters.bytes_sent
            ) / (self.timeout_interval / 1000)
            recv_bytes_per_interval = (
                counters.bytes_recv - last_counters.bytes_recv
            ) / (self.timeout_interval / 1000)

            self.ni_sig_usage_frame.emit(nic, sent_bytes_per_interval, recv_bytes_per_interval)
            self.last_data[nic] = counters

class CWTM_ProcessesInfoRetrievalWorker(QObject):
    proc_sig_processes_info = pyqtSignal(list)

    def __init__(self, timeout_interval, parent_tab_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_interval = timeout_interval
        self.parent_tab_widget = parent_tab_widget

    def run(self):        
        self.processes_update_timer = QTimer()
        self.processes_update_timer.timeout.connect(
            self.get_all_gtk_running_processes_info
        )
        self.processes_update_timer.start(self.timeout_interval)

    def get_all_gtk_running_processes_info(self, *, force_run=False):
        if not force_run and self.parent_tab_widget.currentIndex() != \
           CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB:
            return
        
        *gtk_running_processes, = sys_utils.get_all_running_processes_info()
        self.proc_sig_processes_info.emit(
            gtk_running_processes
        )

class CWTM_ApplicationsInfoRetrievalWorker(QObject):
    app_sig_applications_info = pyqtSignal(list)

    def __init__(self, timeout_interval, parent_tab_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_interval = timeout_interval
        self.parent_tab_widget = parent_tab_widget

    def run(self):        
        self.application_update_timer = QTimer()
        self.application_update_timer.timeout.connect(
            self.get_all_gtk_running_applications_info
        )
        self.application_update_timer.start(self.timeout_interval)

    def get_all_gtk_running_applications_info(self, *, force_run=False):
        if not force_run and self.parent_tab_widget.currentIndex() != \
          CWTM_TabWidgetColumnEnum.TASK_MANAGER_APPLICATIONS_TAB:
            return
        
        gtk_running_apps = sys_utils.get_all_running_applications_names()
        gtk_running_apps_and_icons = sys_utils.get_all_running_applications(
            gtk_running_apps
        )
        self.app_sig_applications_info.emit(
            gtk_running_apps_and_icons
        )

class CWTM_PerformanceInfoRetrievalWorker(QObject):
    perf_sig_memory_labels_info = pyqtSignal(psutil._pslinux.svmem)
    perf_sig_status_bar_labels_info = pyqtSignal(int, float, float)
    perf_sig_cpu_usage_history_graphs_info = pyqtSignal(list) # percpu or all cpu
    perf_sig_kernel_mem_labels_info = pyqtSignal(psutil._common.sswap)
    perf_sig_sys_mem_labels_info = pyqtSignal(int, int, int, str, str)

    perf_sig_graphical_widgets_info = pyqtSignal(float, float, float, float)

    def __init__(self, timeout_interval, parent_tab_widget, *args, per_cpu, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_interval = timeout_interval
        self.parent_tab_widget = parent_tab_widget
        self.per_cpu = per_cpu

    def run(self):
        """
        self.performance_update_timer = QTimer(self)
        self.performance_update_timer.timeout.connect(
            self.get_all_resource_usage
        )
        self.performance_update_timer.start(self.timeout_interval)
        """
        """
        while True:
            self.get_all_resource_usage()
            QThread.msleep(self.timeout_interval)"""
        self.get_all_resource_usage_loop()

    def get_system_memory_labels(self, total_processes, virtual_memory):
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

        self.perf_sig_sys_mem_labels_info.emit(
            n_file_descriptors, n_sys_threads, n_sys_processes,
            total_system_uptime, total_system_mem_commit
        )

    def get_cpu_usage_history_graphs(self):
        current_cpu_usage = [psutil.cpu_percent()] if not self.per_cpu \
                                else psutil.cpu_percent(percpu=True)

        self.perf_sig_cpu_usage_history_graphs_info.emit(current_cpu_usage)

    def get_all_resource_usage_frame(self):
        current_memory_info = psutil.virtual_memory()
        sys_swap_memory = psutil.swap_memory()
        *total_iter_processes, = psutil.process_iter()
        current_cpu_usage = psutil.cpu_percent()
        
        current_memory_usage = current_memory_info.percent
        memory_total, _ = sys_utils.get_memory_size_info(
            current_memory_info.total
        )
        memory_used, _ = sys_utils.get_memory_size_info(
            current_memory_info.used
        )

        self.get_system_memory_labels(total_iter_processes, current_memory_info)
        self.get_cpu_usage_history_graphs()

        self.perf_sig_kernel_mem_labels_info.emit(sys_swap_memory)
        self.perf_sig_memory_labels_info.emit(current_memory_info)
        self.perf_sig_status_bar_labels_info.emit(
            len(total_iter_processes), current_memory_usage, current_cpu_usage
        )

        self.perf_sig_graphical_widgets_info.emit(
            current_cpu_usage, current_memory_usage,
            memory_used, memory_total
        )

    def get_all_resource_usage_loop(self):
        if self.timeout_interval == CWTM_GraphUpdateIntervals.GRAPH_INTERVAL_PAUSED:
            QTimer.singleShot(100, self.get_all_resource_usage_loop) # wait 100 ms until it is not paused
        else:
            self.get_all_resource_usage_frame()
            QTimer.singleShot(self.timeout_interval, self.get_all_resource_usage_loop)


class CWTM_ServicesInfoRetrievalWorker(QObject):
    proc_sig_processes_info = pyqtSignal(list)
    proc_sig_clear_processes_info = pyqtSignal()

    def __init__(self, timeout_interval, parent_tab_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_interval = timeout_interval
        self.parent_tab_widget = parent_tab_widget

    def run(self):        
        self.processes_update_timer = QTimer()
        self.processes_update_timer.timeout.connect(
            self.get_all_gtk_running_processes_info
        )
        self.processes_update_timer.start(self.timeout_interval)

    def get_all_gtk_running_processes_info(self, *, force_run=False):
        if not force_run and self.parent_tab_widget.currentIndex() != \
           CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB:
            return
        
        self.proc_sig_clear_processes_info.emit()
        *gtk_running_processes, = sys_utils.get_all_running_processes_info()
        self.proc_sig_processes_info.emit(
            gtk_running_processes
        )

class CWTM_UsersInfoRetrievalWorker(QObject):
    proc_sig_processes_info = pyqtSignal(list)
    proc_sig_clear_processes_info = pyqtSignal()

    def __init__(self, timeout_interval, parent_tab_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout_interval = timeout_interval
        self.parent_tab_widget = parent_tab_widget

    def run(self):        
        self.processes_update_timer = QTimer()
        self.processes_update_timer.timeout.connect(
            self.get_all_gtk_running_processes_info
        )
        self.processes_update_timer.start(self.timeout_interval)

    def get_all_gtk_running_processes_info(self, *, force_run=False):
        if not force_run and self.parent_tab_widget.currentIndex() != \
           CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB:
            return
        
        self.proc_sig_clear_processes_info.emit()
        *gtk_running_processes, = sys_utils.get_all_running_processes_info()
        self.proc_sig_processes_info.emit(
            gtk_running_processes
        )