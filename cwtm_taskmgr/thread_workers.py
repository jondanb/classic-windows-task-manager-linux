import psutil
import functools

from . import sys_utils
from .tm_tabbar.core_properties import (
    CWTM_TabWidgetColumnEnum,
    CWTM_GlobalUpdateIntervals
)
from .qt_components import (
    CWTM_TimeoutIntervalChangeSignal,
    CWTM_InformationRetrievalAuthorization
)

from PyQt5.QtCore import (
    pyqtSignal, pyqtSlot, Qt,
    QTimer, QThread, QObject
)
from PyQt5.QtWidgets import QTabWidget


class CWTM_NetworkingInterfaceRetrievalWorker(CWTM_TimeoutIntervalChangeSignal):
    """
    Worker class responsible for retrieving networking interface usage data at specified intervals
    and emitting signals with the updated information. It monitors network interfaces, detects
    disconnected interfaces, and calculates the bytes sent and received per interval.

    Attributes:
        ni_sig_usage_frame (pyqtSignal): Signal emitted with NIC usage data.
            - str: Network interface name.
            - float: Sent bytes per interval.
            - float: Received bytes per interval.
        ni_sig_disconnect_nic (pyqtSignal): Signal emitted when a network interface is disconnected.
            - str: Network interface name.
    """

    ni_sig_usage_frame = pyqtSignal(str, float, float)
    ni_sig_disconnect_nic = pyqtSignal(str)

    def __init__(self, timeout_interval: int, *args: list, **kwargs: dict) -> None:
        """
        Initializes the Networking Interface Retrieval Worker.

        Arguments:
            timeout_interval (int): The interval in milliseconds between data retrievals.
            *args: Extra arguments meant for the superclass (CWTM_TimeoutIntervalChangeSignal:QObject)
            **kwargs: Extra keyword arguments meant for the superclass (CWTM_TimeoutIntervalChangeSignal:QObject)
        """
        super().__init__(*args, **kwargs)
        self.timeout_interval: int = timeout_interval
        # To check bytes sent and bytes received, we need to compare two frames of network usage.
        self.last_data: dict[str, psutil._common.snetio] = {}

    def run(self):
        """
        Starts the networking interface usage retrieval loop.
        """
        self.get_networking_interface_usage_loop()

    def check_for_disconnected_network_interface(self, network_data):
        """
        Checks for any network interfaces that have been disconnected since the last check.
        Emits a signal for each disconnected interface and updates the internal tracking data.

        Arguments:
            network_data (dict): Current network data retrieved from psutil.net_io_counters().
                Keys are interface names, and values are psutil._common.snetio objects (their properties).
        """
        current_network_data_set: set[str] = set(network_data.keys())
        last_network_data_set: set[str] = set(self.last_data.keys())
        disconnected_interfaces: set[str] = last_network_data_set - current_network_data_set
        # Subtracting the two sets so that the disconnected interfaces are left in the subbed set

        for nic in disconnected_interfaces:
            del self.last_data[nic] # Delete the disconnected network interface
            self.ni_sig_disconnect_nic.emit(nic) # Dispatch deleted interface

    @CWTM_TimeoutIntervalChangeSignal.thread_worker_timeout_interval_loop()
    def get_networking_interface_usage_loop(self):
        """
        Retrieves the current networking interface usage data, calculates the bytes sent
        and received per interval for each active interface, and emits the corresponding signals.
        Also updates the internal state with the latest data.

        This method performs the following steps:
            1. Fetches current network I/O counters.
            2. Checks for any disconnected network interfaces.
            3. Clears the network list table in the parent UI component. (to be changed)
            4. Iterates through each network interface to calculate usage.
            5. Emits usage data for active interfaces.
        """
        current_data = psutil.net_io_counters(pernic=True)
        self.check_for_disconnected_network_interface(current_data)

        for nic, counters in current_data.items():
            if nic not in self.last_data:
                self.last_data[nic]: psutil._common.snetio = counters
                continue

            last_counters: psutil._common.snetio = self.last_data[nic]
            sent_bytes_per_interval: float = (
                counters.bytes_sent - last_counters.bytes_sent
            ) / (self.timeout_interval / 1000)
            recv_bytes_per_interval: float = (
                counters.bytes_recv - last_counters.bytes_recv
            ) / (self.timeout_interval / 1000)

            self.ni_sig_usage_frame.emit(nic, sent_bytes_per_interval, recv_bytes_per_interval)
            self.last_data[nic]: psutil._common.snetio = counters


class CWTM_ProcessesInfoRetrievalWorker(CWTM_TimeoutIntervalChangeSignal, CWTM_InformationRetrievalAuthorization):
    """
    Worker class responsible for retrieving information about all running GTK processes
    at specified intervals. The retrieved data is emitted via a signal, which provides a list
    of process information.

    Attributes:
        proc_sig_processes_info (pyqtSignal): Signal emitted with a list of running GTK process info.
            - list: List of running process information.
    """

    proc_sig_processes_info = pyqtSignal(list)

    def __init__(self, timeout_interval: int, *args: tuple, **kwargs: dict) -> None:
        """
        Initializes the Processes Info Retrieval Worker.

        Args:
            timeout_interval (int): The interval in milliseconds between data retrievals.
            *args: Variable length argument list for additional parameters.
            **kwargs: Arbitrary keyword arguments for additional parameters.
        """
        super().__init__(*args, **kwargs)
        self.timeout_interval: int = timeout_interval

    def run(self) -> None:
        """
        Starts the process info retrieval loop.
        """
        self.get_all_gtk_running_processes_info_loop()

    @CWTM_TimeoutIntervalChangeSignal.thread_worker_timeout_interval_loop()
    def get_all_gtk_running_processes_info_loop(self, *, force_run: bool = False) -> None:
        """
        Retrieves information about all running GTK processes and emits the process info signal.
        If the current tab is not the task manager processes tab, the method does not perform the 
        retrieval unless force_run is set to True.

        Args:
            force_run (bool): If True, forces the retrieval of process information regardless of the tab selection.
        """
        if not force_run and not self._info_retrieval_authorization: # CWTM_InformationRetrievalAuthorization
            return
        
        *gtk_running_processes, = sys_utils.get_all_running_processes_info()
        self.proc_sig_processes_info.emit(gtk_running_processes)


class CWTM_ApplicationsInfoRetrievalWorker(CWTM_TimeoutIntervalChangeSignal, CWTM_InformationRetrievalAuthorization):
    """
    Worker class responsible for retrieving information about all running GTK applications
    at specified intervals. The retrieved data includes application names and icons, and is
    emitted via a signal.

    Attributes:
        app_sig_applications_info (pyqtSignal): Signal emitted with a list of running GTK application info.
            - list: List of application names and their corresponding icons.
    """

    app_sig_applications_info = pyqtSignal(list)

    def __init__(self, timeout_interval: int, *args: tuple, **kwargs: dict) -> None:
        """
        Initializes the Applications Info Retrieval Worker.

        Args:
            timeout_interval (int): The interval in milliseconds between data retrievals.
            *args: Variable length argument list for additional parameters.
            **kwargs: Arbitrary keyword arguments for additional parameters.
        """
        super().__init__(*args, **kwargs)
        self.timeout_interval: int = timeout_interval

    def run(self) -> None:
        """
        Starts the application info retrieval loop.
        """
        self.get_all_gtk_running_applications_info_loop()

    @CWTM_TimeoutIntervalChangeSignal.thread_worker_timeout_interval_loop()
    def get_all_gtk_running_applications_info_loop(self, *, force_run: bool = False) -> None:
        """
        Retrieves information about all running GTK applications, including their names and icons,
        and emits the application info signal. If the current tab is not the applications tab or if
        force_run is False, the method does not perform the retrieval.

        Args:
            force_run (bool): If True, forces the retrieval of application information regardless of the tab selection.
        """

        if not force_run and not self._info_retrieval_authorization:
            return
        
        gtk_running_apps: list = sys_utils.get_all_running_applications_names()
        gtk_running_apps_and_icons: list = sys_utils.get_all_running_applications(gtk_running_apps)
        self.app_sig_applications_info.emit(gtk_running_apps_and_icons)


class CWTM_PerformanceInfoRetrievalWorker(CWTM_TimeoutIntervalChangeSignal, CWTM_InformationRetrievalAuthorization):
    """
    Worker class responsible for retrieving system performance metrics at specified intervals,
    including memory usage, CPU usage, and swap memory information. The retrieved data is emitted
    through several signals, providing real-time system statistics.

    Attributes:
        perf_sig_memory_labels_info (pyqtSignal): Signal emitted with memory usage information.
            - psutil._pslinux.svmem: Virtual memory statistics.
        perf_sig_status_bar_labels_info (pyqtSignal): Signal emitted with status bar information.
            - int: Total number of processes.
            - float: Current memory usage percentage.
            - float: Current CPU usage percentage.
        perf_sig_cpu_usage_history_graphs_info (pyqtSignal): Signal emitted with CPU usage history.
            - list: List of CPU usage percentages.
            - list: List of kernel CPU usage percentages.
        perf_sig_kernel_mem_labels_info (pyqtSignal): Signal emitted with swap memory information.
            - psutil._common.sswap: Swap memory statistics.
        perf_sig_sys_mem_labels_info (pyqtSignal): Signal emitted with system memory labels.
            - int: Number of file descriptors.
            - int: Number of system threads.
            - int: Number of system processes.
            - str: System uptime.
            - str: Total and used commit memory.
        perf_sig_graphical_widgets_info (pyqtSignal): Signal emitted with graphical widget data.
            - float: CPU usage.
            - float: Kernel CPU time.
            - float: Memory usage percentage.
            - float: Memory used in MB.
            - float: Total memory in MB.
    """

    perf_sig_memory_labels_info = pyqtSignal(psutil._pslinux.svmem)
    perf_sig_status_bar_labels_info = pyqtSignal(int, float, float)
    perf_sig_cpu_usage_history_graphs_info = pyqtSignal(list, list)  # percpu or all cpu
    perf_sig_kernel_mem_labels_info = pyqtSignal(psutil._common.sswap)
    perf_sig_sys_mem_labels_info = pyqtSignal(int, int, int, str, str)

    perf_sig_graphical_widgets_info = pyqtSignal(float, float, float, float, float)

    perf_sig_request_per_cpu_status_change = pyqtSignal(bool)

    def __init__(self, timeout_interval: int, *args: tuple, per_cpu: bool, **kwargs: dict) -> None:
        """
        Initializes the Performance Info Retrieval Worker.

        Args:
            timeout_interval (int): The interval in milliseconds between data retrievals.
            per_cpu (bool): Flag indicating whether to retrieve per-CPU usage data.
            *args: Variable length argument list for additional parameters.
            **kwargs: Arbitrary keyword arguments for additional parameters.
        """
        super().__init__(*args, **kwargs)
        self.timeout_interval: int = timeout_interval
        self.per_cpu: bool = per_cpu

        self.perf_sig_request_per_cpu_status_change.connect(
            self.update_per_cpu_graphing_mode_status)

    def run(self) -> None:
        """
        Starts the resource usage retrieval loop.
        """
        self.get_all_resource_usage_loop()

    @pyqtSlot(bool)
    def update_per_cpu_graphing_mode_status(self, updated_status: bool) -> None:
        """
        Updates the `per_cpu` status variable using a signal and slot so it is run thread-safe

        Arguments:
            - updated_status (bool): The value `per_cpu` should be set to
        """
        self.per_cpu: bool = updated_status

    def get_system_memory_labels(self, total_processes: list, virtual_memory: psutil._pslinux.svmem) -> None:
        """
        Retrieves and emits system memory labels, including information about file descriptors,
        system threads, processes, and system uptime. It also provides commit memory statistics.

        Args:
            total_processes (list): List of all running processes on the system.
            virtual_memory (psutil._pslinux.svmem): Virtual memory statistics from psutil.
        """
        if not self._info_retrieval_authorization:
            return

        n_file_descriptors: int = sys_utils.get_number_of_handle_file_descriptors()
        n_sys_threads: int = sys_utils.get_number_of_total_threads(total_processes)
        n_sys_processes: int = len(total_processes)
        commit_mem_total, commit_mem_amount = sys_utils.get_total_system_commit_memory(virtual_memory)
        total_system_mem_commit: str = " / ".join((
            sys_utils.convert_proc_mem_b_to_mb(commit_mem_amount)[:-2],
            sys_utils.convert_proc_mem_b_to_mb(commit_mem_total)[:-2]
        ))
        total_system_uptime: str = sys_utils.format_seconds_to_timestamp(sys_utils.get_total_uptime_in_seconds())

        self.perf_sig_sys_mem_labels_info.emit(
            n_file_descriptors, n_sys_threads, n_sys_processes,
            total_system_uptime, total_system_mem_commit
        )

    def get_cpu_usage_history_graphs(self, cpu_usage: float, kernel_usage: float) -> tuple[list, list]:
        """
        Retrieves the CPU usage history, either for all CPUs or per-CPU, depending on the `per_cpu` flag.
        Returns two lists: one for the overall CPU usage and one for kernel CPU usage.

        Args:
            cpu_usage (float): The overall CPU usage percentage.
            kernel_usage (float): The overall kernel CPU usage percentage.

        Returns:
            tuple[list, list]: A tuple containing two lists:
                - List of CPU usage percentages.
                - List of kernel CPU usage percentages.
        """
        current_cpu_usage: list[float] = [cpu_usage] if not self.per_cpu else psutil.cpu_percent(percpu=True)
        current_cpu_kernel_usage: list[float] = [kernel_usage] if not self.per_cpu else [
            *map(lambda x: x.system, psutil.cpu_times_percent(percpu=True))]
        
        return current_cpu_usage, current_cpu_kernel_usage

    @CWTM_TimeoutIntervalChangeSignal.thread_worker_timeout_interval_loop()
    def get_all_resource_usage_loop(self) -> None:
        """
        Retrieves the system resource usage statistics, including memory usage, CPU usage, and swap memory.
        The retrieved data is emitted via various signals, including graphical widget data, status bar labels,
        and detailed system memory and CPU usage statistics.
        """
        current_cpu_usage: float = psutil.cpu_percent()
        kernel_cpu_time: float = psutil.cpu_times_percent().system
        current_cpu_graph_usage, current_cpu_kernel_graph_usage = self.get_cpu_usage_history_graphs(
            current_cpu_usage, kernel_cpu_time)

        *total_iter_processes, = psutil.process_iter()
        current_memory_info: psutil._pslinux.svmem = psutil.virtual_memory()
        current_memory_usage: float = current_memory_info.percent

        memory_total, _ = sys_utils.get_memory_size_info(current_memory_info.total)
        memory_used, _ = sys_utils.get_memory_size_info(current_memory_info.used)

        self.perf_sig_graphical_widgets_info.emit(
            current_cpu_usage, kernel_cpu_time,
            current_memory_usage, memory_used, memory_total,
        )

        self.perf_sig_cpu_usage_history_graphs_info.emit(current_cpu_graph_usage, current_cpu_kernel_graph_usage)
        self.perf_sig_status_bar_labels_info.emit(
            len(total_iter_processes), current_memory_usage, current_cpu_usage
        )

        if not self._info_retrieval_authorization:
            return

        sys_swap_memory: psutil._common.sswap = psutil.swap_memory()

        self.get_system_memory_labels(total_iter_processes, current_memory_info)

        self.perf_sig_kernel_mem_labels_info.emit(sys_swap_memory)
        self.perf_sig_memory_labels_info.emit(current_memory_info)


class CWTM_ServicesInfoRetrievalWorker(CWTM_TimeoutIntervalChangeSignal, CWTM_InformationRetrievalAuthorization):
    svc_sig_all_system_services = pyqtSignal(list)

    def __init__(self, timeout_interval:int, *args: dict, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)

        self.timeout_interval = timeout_interval

    def run(self):
        self.get_all_services_information_loop()

    @CWTM_TimeoutIntervalChangeSignal.thread_worker_timeout_interval_loop(no_timeout_pause_check=True)
    def get_all_services_information_loop(self, *, force_run: bool = False):
        if not force_run and not self._info_retrieval_authorization:
            return

        *system_all_services, = sys_utils.get_all_system_services()
        self.svc_sig_all_system_services.emit(system_all_services)

class CWTM_UsersInfoRetrievalWorker(CWTM_TimeoutIntervalChangeSignal, CWTM_InformationRetrievalAuthorization):
    users_sig_user_account_info = pyqtSignal(list, list)

    def __init__(self, timeout_interval:int, *args: dict, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)

        self.timeout_interval = timeout_interval

    def run(self):
        self.get_all_users_information_loop()

    @CWTM_TimeoutIntervalChangeSignal.thread_worker_timeout_interval_loop(no_timeout_pause_check=True)
    def get_all_users_information_loop(self, *, force_run: bool = False):
        if not force_run and not self._info_retrieval_authorization:
            return

        *system_user_details, = sys_utils.get_all_user_accounts_details()
        *user_gtk_icons, = sys_utils.get_user_account_type_icon(system_user_details)
        self.users_sig_user_account_info.emit(system_user_details, user_gtk_icons)