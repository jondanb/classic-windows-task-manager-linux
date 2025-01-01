import os
import shlex
import functools

from PyQt5.QtCore import (
    Qt, 
    QTimer, 
    QObject,
    pyqtSignal, 
    pyqtSlot,
    QThread
)
from PyQt5.QtWidgets import QAction

from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ProcessesTabCustomContextMenu

from .. import sys_utils
from ..core_properties import (
    CWTM_ProcessesTabTableColumns,
    CWTM_ServicesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_TabWidgetColumnEnum,
    CWTM_GlobalUpdateIntervals,
    CWTM_ProcessInformationFrame,
    CWTM_PriorityNicenessLevels,
    CWTM_PriorityNicenessRanges
)
from ..qt_components import (
    CWTM_TableWidgetController, 
    CWTM_TaskManagerConfirmationDialog,
    CWTM_GlobalUpdateIntervalHandler,
    CWTM_ErrorMessageDialog
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_ProcessesInfoRetrievalWorker


class CWTM_ProcessesTab(QObject, CWTM_TableWidgetController):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

        self.PROC_T_PROC_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL
        self.PROC_T_PROC_LIST_COLUMN_RATIO = (0.25, 0.10, 0.15,
                                              0.10, 0.15, 0.25)

        self.parent.proc_t_proc_list_table.setColumnHidden(
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_EXECUTABLE, True
        ) # maybe change later???

        self.parent.proc_t_end_process_button.clicked.connect(
            self.process_signal_proc_t_end_process_button)
        self.parent.proc_t_proc_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.proc_t_proc_list_table.customContextMenuRequested.connect(
            self.process_custom_process_context_menu_request)
        self.custom_processes_context_menu = CWTM_ProcessesTabCustomContextMenu(
            parent=self.parent)
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
        self.custom_processes_context_menu.proc_set_priority_menu.aboutToShow.connect(
            self.initialize_context_menu_action_priority_level)

    def process_context_menu_action_open_file_location(self):
        current_selected_process_executable = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_EXECUTABLE)

        executable_path_folder = os.path.dirname(current_selected_process_executable)
        sys_utils.execute_system_uri_command(executable_path_folder)

    def process_context_menu_action_properties(self):
        current_selected_process_executable = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_EXECUTABLE)

        if not current_selected_process_executable:
            return

        sys_utils.show_file_properties(current_selected_process_executable)

    def process_context_menu_action_go_to_service(self):
        selected_process_pid = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID)

        service_tab_row = self.find_row_from_column_value(
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
        selected_process_pid = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID)

        sys_utils.set_nice_of_process(int(selected_process_pid), action.niceness_level)

    def initialize_context_menu_action_priority_level(self) -> None:
        selected_process_pid = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        process_niceness = sys_utils.get_nice_of_process(int(selected_process_pid))

        self.custom_processes_context_menu.set_priority_action_group_checked_from_niceness(
            process_niceness)


    def process_custom_process_context_menu_request(self, position):
        current_selected_item = self.parent.proc_t_proc_list_table.itemAt(position)
        
        if current_selected_item is None:
            return
    
        self.custom_processes_context_menu.exec_(
            self.parent.proc_t_proc_list_table.mapToGlobal(position))

    def process_signal_proc_t_end_process_button(self, end_process_tree=False):
        selected_process_pid = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        selected_process_name = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_IMAGE_NAME
        )

        if selected_process_pid is None:
            return

        confirmation_dialog = CWTM_TaskManagerConfirmationDialog(
            parent=self.parent, proc_name=selected_process_name, 
            proc_pid=int(selected_process_pid), end_proc_tree=end_process_tree
        )
        confirmation_dialog.exec_()
        
    #slot
    def update_processes_page(self, gtk_running_processes: list[CWTM_ProcessInformationFrame]) -> None:
        current_selected_item = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        self.parent.proc_t_proc_list_table.setRowCount(0)
        self.parent.proc_t_proc_list_table.setSortingEnabled(False)

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
        self.parent.proc_t_proc_list_table.setSortingEnabled(True)

        if current_selected_item is not None:
            self.reselect_item_from_value(
                self.parent.proc_t_proc_list_table,
                CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID,
                current_selected_item
            )

    #@pyqtSlot(int)
    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the processes thread worker to emit system process information to the slot
        `update_processes_page`

        Arguments:
            - index: the current index of the tab widget
        """
        self.processes_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB)

    #slot
    def update_refresh_processes_page_proc(self) -> None:
        self.processes_page_worker.get_all_gtk_running_processes_info_loop()

    def start_processes_page_updater_thread(self):
        self.processes_page_thread = QThread()
        self.processes_page_worker = CWTM_ProcessesInfoRetrievalWorker(
            timeout_interval=self.PROC_T_PROC_LIST_TABLE_UPDATE_FREQUENCY)
        self.processes_page_update_handler = CWTM_GlobalUpdateIntervalHandler(
            self.parent, thread_worker=self.processes_page_worker)
        self.processes_page_update_handler.register_selected_tab_update_interval_handler(
            refresh_function=self.update_refresh_processes_page_proc)

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
