import os
import shlex
import functools

from PyQt5.QtCore import (
    Qt, 
    QObject,
    pyqtSignal, 
    pyqtSlot,
    QThread,
    QPoint
)
from PyQt5.QtWidgets import (
    QAction, 
    QTableWidgetItem, 
    QDialog
)

from .. import sys_utils
from ..core_properties import (
    CWTM_ProcessesTabTableColumns,
    CWTM_ServicesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_TabWidgetColumnEnum,
    CWTM_GlobalUpdateIntervals,
    CWTM_ProcessInformationPacket,
)
from ..qt_components import (
    CWTM_TableWidgetController, 
    CWTM_TableWidgetUpdateInitializer,
    CWTM_TaskManagerConfirmationDialog,
    CWTM_GlobalUpdateIntervalHandler,
    CWTM_ErrorMessageDialog,
    CWTM_TaskManagerCPUAffinitySelectorDialog
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_ProcessesInfoRetrievalWorker

from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ProcessesTabCustomContextMenu


class CWTM_ProcessesTab(QObject, CWTM_TableWidgetController):
    def __init__(self, *args: list, parent: QObject, **kwargs: dict) -> None:
        """
        Initializes the processes tab for the task manager. This function sets up all the properties for
        the processes tab including the:
            - Processes QTableWidget column width ratio.
            - The update interval speed based on the enum properties of CWTM_GlobalUpdateIntervals.
            - All the button/custom context menu action signals and slots.

        Arguments:
            - args and kwargs: any arbitrary extra argument/keywork arguments to be passed into the
                main superclass. (QObject)
            - parent (QObject): Initialize the class with the parent as a property the superclass. 
        """
        super().__init__(*args, parent=parent, **kwargs)

        self.parent: QObject = parent

        self.PROC_T_PROC_LIST_COLUMN_RATIO: tuple[float] = (0.25, 0.10, 0.15,
                                              0.10, 0.15, 0.25)
        self.PROC_T_PROC_LIST_TABLE_UPDATE_FREQUENCY: CWTM_GlobalUpdateIntervals = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL

        self.parent.proc_t_proc_list_table.setColumnHidden(
            CWTM_ProcessesTabTableColumns._PROC_T_PROC_LIST_TABLE_EXECUTABLE, True
        ) # maybe change later???

        # Buttons
        self.parent.proc_t_end_process_button.clicked.connect(
            self.process_signal_proc_t_end_process_button)

        # Context Menu
        self.parent.proc_t_proc_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.proc_t_proc_list_table.customContextMenuRequested.connect(
            self.process_custom_process_context_menu_request)

        self.custom_processes_context_menu = CWTM_ProcessesTabCustomContextMenu(
            parent=self.parent)
        self.custom_processes_context_menu.proc_set_priority_menu.aboutToShow.connect(
            self.initialize_context_menu_action_priority_level)

        self.custom_processes_context_menu.proc_open_file_location_action.triggered.connect(
            self.process_context_menu_action_open_file_location)
        self.custom_processes_context_menu.proc_end_process_action.triggered.connect(
            self.process_signal_proc_t_end_process_button)
        self.custom_processes_context_menu.proc_end_process_tree_action.triggered.connect(
            functools.partial(self.process_signal_proc_t_end_process_button, True))
        self.custom_processes_context_menu.proc_properties_action.triggered.connect(
            self.process_context_menu_action_properties)
        self.custom_processes_context_menu.proc_go_to_service_action.triggered.connect(
            self.process_context_menu_action_go_to_service)
        self.custom_processes_context_menu.proc_set_priority_menu_action_group.triggered.connect(
            self.process_context_menu_action_set_priority)
        self.custom_processes_context_menu.proc_set_affinity_action.triggered.connect(
            self.process_context_menu_action_set_affinity)

    @pyqtSlot()
    def process_context_menu_action_open_file_location(self) -> None:
        """
        Slot to process the context menu action to open the selected process file location.
        It gets the selected process executable path and opens its parent directory via
        a global executable URI command. 
        """
        current_selected_process_executable: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns._PROC_T_PROC_LIST_TABLE_EXECUTABLE)

        executable_path_folder: str = os.path.dirname(current_selected_process_executable)
        sys_utils.execute_system_uri_command(executable_path_folder)

    @pyqtSlot()
    def process_context_menu_action_properties(self) -> None:
        """
        Slot to process the context menu action to open the selected process properties information
        window. It gets the selected process executable path and opens its properties window directly using
        its executable location.

        If this function cannot find the process executable path, then the properties window will not open.
        """
        current_selected_process_executable: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns._PROC_T_PROC_LIST_TABLE_EXECUTABLE)

        if not current_selected_process_executable:
            return

        sys_utils.show_file_properties(current_selected_process_executable)

    @pyqtSlot()
    def process_context_menu_action_set_affinity(self) -> None:
        """
        Slot to process the context menu action to set a process affinity. This function uses the dialog class
        CWTM_TaskManagerCPUAffinitySelectorDialog to process the CPU affinity selection process.
        """
        selected_process_pid: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        selected_process_name: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_IMAGE_NAME
        )

        cpu_affinity_selector_dialog: QDialog = CWTM_TaskManagerCPUAffinitySelectorDialog(
            proc_name=selected_process_name, proc_pid=int(selected_process_pid))
        cpu_affinity_selector_dialog.exec_()

    @pyqtSlot()
    def process_context_menu_action_go_to_service(self) -> None:
        """
        Slot to process the context menu action to reference a running process with its registered service.
        This function finds the service based on the process PID. If the process is not classified as a service
        based on its PID, then the function returns.
        """
        selected_process_pid: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID)

        service_tab_row: int = self.find_row_from_column_value(
            self.parent.svc_t_services_list_table, 
            CWTM_ServicesTabTableColumns.SVC_T_SERVICES_LIST_TABLE_PID,
            selected_process_pid)

        if service_tab_row > 0:
            self.parent.task_manager_tab_widget.setCurrentIndex(
                CWTM_TabWidgetColumnEnum.TASK_MANAGER_SERVICES_TAB)
            self.parent.svc_t_services_list_table.selectRow(service_tab_row)

    @pyqtSlot(QAction)
    @CWTM_ErrorMessageDialog.show_error_dialog_on_error(
        "You do not have the required permissions to set the priority of this process.\n"
        "This may be because you are setting a high priority to a process without root privileges.")
    def process_context_menu_action_set_priority(self, action: QAction) -> None:
        """
        Slot to process the context menu action to set the priority of a process by setting its niceness value.
        Typically, without root privileges, a process niceness value cannot be decreased (higher priority) and only
        able to be increased (lower priority). If this is the case, then the function will show an error dialog.

        Arguments:
            - action (QAction): the priority action along with its niceness level
        """
        selected_process_pid: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID)

        sys_utils.set_nice_of_process(int(selected_process_pid), action.niceness_level)

    @pyqtSlot()
    def initialize_context_menu_action_priority_level(self) -> None:
        """
        Slot to process the context menu when its about to show so that the priority level checkbox
        is properly initialized and set to its corresponding priority based on its niceness level.
        """
        selected_process_pid: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        process_niceness: int = sys_utils.get_nice_of_process(int(selected_process_pid))

        self.custom_processes_context_menu.set_priority_action_group_checked_from_niceness(
            process_niceness)

    @pyqtSlot(QPoint)
    def process_custom_process_context_menu_request(self, position: QPoint) -> None:
        """
        Slot to find the current selected item in the tab's table widget and pass it off to the
        custom context menu assigned to the QTableWidgetItem(s).

        Arguments:
            - position (QPoint): The position of the current selected item in the table widget.
        """
        current_selected_item: QTableWidgetItem = self.parent.proc_t_proc_list_table.itemAt(position)
        
        if current_selected_item is None:
            return
    
        self.custom_processes_context_menu.exec_(
            self.parent.proc_t_proc_list_table.mapToGlobal(position))

    @pyqtSlot(bool)
    def process_signal_proc_t_end_process_button(self, end_process_tree: bool=False) -> None:
        """
        Slot to process the action of ending a process in the processes tab.

        Arguments:
            - end_process_tree (bool): Whether the entire process tree should be terminated.
        """
        selected_process_pid: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        selected_process_name: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_IMAGE_NAME
        )

        if selected_process_pid is None:
            return

        confirmation_dialog: QDialog = CWTM_TaskManagerConfirmationDialog(
            parent=self.parent, proc_name=selected_process_name, 
            proc_pid=int(selected_process_pid), end_proc_tree=end_process_tree
        )
        confirmation_dialog.exec_()
        
    @pyqtSlot(list)
    def update_processes_page(self, gtk_running_processes: list[CWTM_ProcessInformationPacket]) -> None:
        """
        Slot to update the processes table widget with new proces information.

        Arguments:
            - gtk_running_processes (list[CWTM_ProcessInformationPacket]): 
                Contains a list of information packets for each running process.
        """
        current_selected_item: str = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )

        with CWTM_TableWidgetUpdateInitializer(self.parent.proc_t_proc_list_table, initialize_sorting=True):
            for process_information in gtk_running_processes:
                proc_memory_mb = sys_utils.convert_proc_mem_b_to_mb(
                    process_information.p_memory_usage.rss, include_unit_label=False)
                proc_desc = shlex.join(
                    process_information.p_description if process_information.p_description is not None else [])
                
                self.append_row_to_table(
                    self.parent.proc_t_proc_list_table, CWTM_ProcessesTabTableColumns,
                    CWTM_TableWidgetItemProperties(
                        item_label=process_information.p_name, item_tool_tip=process_information.p_name),
                    CWTM_TableWidgetItemProperties(item_label=str(process_information.p_pid), 
                        item_type=CWTM_QNumericTableWidgetItem),
                    CWTM_TableWidgetItemProperties(item_label=process_information.p_username),
                    CWTM_TableWidgetItemProperties(item_label=str(process_information.p_cpu_usage), 
                        item_type=CWTM_QNumericTableWidgetItem),
                    CWTM_TableWidgetItemProperties(item_label=proc_memory_mb,
                        item_type=CWTM_QNumericTableWidgetItem, item_unit="MB"),
                    CWTM_TableWidgetItemProperties(item_label=proc_desc, item_tool_tip=proc_desc),
                    CWTM_TableWidgetItemProperties(item_label=process_information.p_exe) # hidden
                )

        if current_selected_item is not None:
            self.reselect_item_from_value(
                self.parent.proc_t_proc_list_table,
                CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID,
                current_selected_item
            )

    @pyqtSlot()
    def update_refresh_processes_page(self) -> None:
        """
        Refreshes the processes page by requesting an information retrieval from the process'
        thread worker.
        """
        self.processes_page_worker.get_all_gtk_running_processes_info_loop()

    @pyqtSlot(int)
    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the processes thread worker to emit system process information to the slot
        `update_processes_page`

        Arguments:
            - index: the current index of the tab widget
        """
        self.processes_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB)

    def start_processes_page_updater_thread(self) -> None:
        """
        Starts the processes page updater thread loop.
        """
        self.processes_page_thread: QThread = QThread()
        self.processes_page_worker: CWTM_ProcessesInfoRetrievalWorker = CWTM_ProcessesInfoRetrievalWorker(
            timeout_interval=self.PROC_T_PROC_LIST_TABLE_UPDATE_FREQUENCY)
        self.processes_page_update_handler = CWTM_GlobalUpdateIntervalHandler(
            self.parent, thread_worker=self.processes_page_worker)
        self.processes_page_update_handler.register_selected_tab_update_interval_handler(
            refresh_function=self.update_refresh_processes_page)

        self.processes_page_worker.proc_sig_processes_info.connect(
            self.update_processes_page)

        self.processes_page_worker.moveToThread(self.processes_page_thread)
        self.parent.task_manager_tab_widget.currentChanged.connect(
            self.update_thread_worker_info_retrieval_authorization)

        self.processes_page_thread.started.connect(
            self.processes_page_worker.run)
        
        self.processes_page_thread.start()

        self.processes_page_worker.get_all_gtk_running_processes_info_loop(
            force_run=True, disable_loop=True)
