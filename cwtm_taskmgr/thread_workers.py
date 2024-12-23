import psutil
import functools

from . import sys_utils
from .tm_tabbar.core_properties import CWTM_TabWidgetColumnEnum

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
        gtk_running_apps_icons = sys_utils.get_all_running_applications(
            gtk_running_apps
        )
        self.app_sig_applications_info.emit(
            gtk_running_apps_icons
        )

# TODODODODODODOTODO OTODODOTODODO FUCKING DO THIS PLEASE

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