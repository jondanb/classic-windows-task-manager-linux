import os
import enum
import shlex
import functools

from .. import sys_utils
from ..core_properties import (
    CWTM_ProcessesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_TabWidgetColumnEnum,
    CWTM_GlobalUpdateIntervals
)
from ..qt_components import (
    CWTM_TableWidgetController, 
    CWTM_TaskManagerConfirmationDialog,
    CWTM_GlobalUpdateIntervalHandler,
    CWTM_ErrorMessageDialog
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_ProcessesInfoRetrievalWorker

from PyQt5.QtCore import (
    Qt, QTimer,
    pyqtSignal, pyqtSlot,
    QThread
)
from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ProcessesTabCustomContextMenu


class CWTM_ProcessesTab(CWTM_TableWidgetController):
    def __init__(self, parent):
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
        self.custom_applications_context_menu = CWTM_ProcessesTabCustomContextMenu(
            parent=self.parent)
        self.custom_applications_context_menu.proc_open_file_location_action.triggered.connect(
            self.process_context_menu_action_open_file_location)
        self.custom_applications_context_menu.proc_end_process_action.triggered.connect(
            self.process_signal_proc_t_end_process_button)
        self.custom_applications_context_menu.proc_end_process_tree_action.triggered.connect(
            functools.partial(self.process_signal_proc_t_end_process_button, True))

    def process_context_menu_action_open_file_location(self):
        current_selected_process_executable = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_EXECUTABLE)

        executable_path_folder = os.path.dirname(current_selected_process_executable)
        sys_utils.execute_system_uri_command(executable_path_folder)

    def process_custom_process_context_menu_request(self, position):
        current_selected_item = self.parent.proc_t_proc_list_table.itemAt(position)
        
        if current_selected_item is None:
            return

        self.custom_applications_context_menu.exec_(
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
    def update_processes_page(self, gtk_running_processes):
        current_selected_item = self.get_current_selected_item_from_column(
            self.parent.proc_t_proc_list_table,
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID
        )
        self.parent.proc_t_proc_list_table.setRowCount(0)
        self.parent.proc_t_proc_list_table.setSortingEnabled(False)

        for (p_name, p_pid, p_username, \
                p_cpu, p_mem, p_desc, p_exe) in gtk_running_processes:
            proc_memory_mb = sys_utils.convert_proc_mem_b_to_mb(
                p_mem.rss, include_unit_label=False)
            proc_desc = shlex.join(p_desc if p_desc is not None else [])
            
            self.append_row_to_table(
                self.parent.proc_t_proc_list_table, CWTM_ProcessesTabTableColumns,
                CWTM_TableWidgetItemProperties(item_label=p_name, item_tool_tip=p_name),
                CWTM_TableWidgetItemProperties(item_label=str(p_pid), 
                    item_type=CWTM_QNumericTableWidgetItem),
                CWTM_TableWidgetItemProperties(item_label=p_username),
                CWTM_TableWidgetItemProperties(item_label=str(p_cpu), 
                    item_type=CWTM_QNumericTableWidgetItem),
                CWTM_TableWidgetItemProperties(item_label=proc_memory_mb,
                    item_type=CWTM_QNumericTableWidgetItem, item_unit="MB"),
                CWTM_TableWidgetItemProperties(item_label=proc_desc, item_tool_tip=proc_desc),
                CWTM_TableWidgetItemProperties(item_label=p_exe) # hidden
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
