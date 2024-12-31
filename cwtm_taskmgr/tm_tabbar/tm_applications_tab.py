import enum

from PyQt5.QtCore import (
    Qt, QTimer, 
    pyqtSignal, 
    QThread
)
from PyQt5.QtWidgets import (
    QTableWidgetItem, QHeaderView, 
    QMenu, QAction
)

from ..core_properties import (
    CWTM_ApplicationsTabTableColumns,
    CWTM_ProcessesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_TabWidgetColumnEnum
)
from ..qt_components import (
    CWTM_TableWidgetController, 
    CWTM_TaskManagerConfirmationDialog,
    CWTM_GlobalUpdateIntervalHandler,
    CWTM_TaskManagerNewTaskDialog,
    CWTM_ErrorMessageDialog
)
from ..thread_workers import CWTM_ApplicationsInfoRetrievalWorker
from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ApplicationsTabCustomContextMenu


class CWTM_ApplicationsTab(CWTM_TableWidgetController):
    def __init__(self, parent):
        self.parent = parent

        self.APP_T_TASK_LIST_TABLE_COLUMN_RATIO = (0.85, 0.15)
        self.APP_T_TASK_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL

        self.parent.app_t_task_list_table.setColumnHidden(
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID, True
        ) # maybe change later???
        self.parent.app_t_task_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.app_t_task_list_table.customContextMenuRequested.connect(
            self.process_custom_applications_context_menu_request)

        self.custom_applications_context_menu = CWTM_ApplicationsTabCustomContextMenu(
            parent=self.parent)
        self.parent.app_t_end_task_button.clicked.connect(
            self.process_signal_app_t_end_task_button)
        self.parent.app_t_new_task_button.clicked.connect(
            self.process_signal_app_t_new_task_button)
        self.parent.tm_file_menu_new_task_run.triggered.connect(
            self.process_signal_app_t_new_task_button)
        self.custom_applications_context_menu.app_t_table_tile_end_task_action.triggered.connect(
            self.process_signal_app_t_end_task_button)
        self.custom_applications_context_menu.app_t_table_go_to_process_action.triggered.connect(
            self.process_context_menu_action_go_to_process)

    def process_context_menu_action_go_to_process(self):
        selected_application_pid = self.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table, 
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID)

        process_tab_row = self.find_row_from_column_value(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID,
            selected_application_pid)

        if process_tab_row > 0:
            self.parent.task_manager_tab_widget.setCurrentIndex(
                CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB)
            self.parent.proc_t_proc_list_table.selectRow(process_tab_row)

    def process_custom_applications_context_menu_request(self, position):
        current_selected_item = self.parent.app_t_task_list_table.itemAt(position)
        
        if current_selected_item is None:
            return

        self.custom_applications_context_menu.exec_(
            self.parent.app_t_task_list_table.mapToGlobal(position))

    def process_signal_app_t_new_task_button(self):
        new_task_dialog = CWTM_TaskManagerNewTaskDialog(parent=self.parent)
        new_task_dialog.exec_()
    
    def process_signal_app_t_end_task_button(self, *_):
        selected_application_pid = CWTM_TableWidgetController.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID
        )
        selected_application_name = CWTM_TableWidgetController.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_TASK
        )

        if selected_application_pid is None:
            return

        confirmation_dialog = CWTM_TaskManagerConfirmationDialog(
            proc_name=selected_application_name, proc_pid=int(selected_application_pid)
        )
        confirmation_dialog.exec_()

    def update_applications_page(self, gtk_running_apps_icons):
        current_selected_item = self.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID
        )
        
        self.parent.app_t_task_list_table.setRowCount(0)
        
        for gtk_app_name, gtk_app_pid, gtk_app_icon in gtk_running_apps_icons:
            if not gtk_app_name:
                continue

            self.append_row_to_table(
                self.parent.app_t_task_list_table, CWTM_ApplicationsTabTableColumns,
                CWTM_TableWidgetItemProperties(item_label=gtk_app_name, item_icon=gtk_app_icon),
                CWTM_TableWidgetItemProperties(item_label="Running"), # maybe change later
                CWTM_TableWidgetItemProperties(item_label=str(gtk_app_pid)) # for private use, maybe also change later
            )

        if current_selected_item is not None:
            self.reselect_item_from_value(
                self.parent.app_t_task_list_table,
                CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID,
                current_selected_item
            )

    def update_refresh_applications_page_apps(self):
        self.applications_page_worker.get_all_gtk_running_applications_info_loop(disable_loop=True)

    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the applications thread worker to emit system application information to the slot
        `update_applications_page`

        Arguments:
            - index: the current index of the tab widget
        """
        self.applications_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_APPLICATIONS_TAB)

    def start_applications_page_updater_thread(self):
        self.applications_page_thread = QThread()
        self.applications_page_worker = CWTM_ApplicationsInfoRetrievalWorker(
            timeout_interval=self.APP_T_TASK_LIST_TABLE_UPDATE_FREQUENCY)
        self.applications_page_update_handler = CWTM_GlobalUpdateIntervalHandler(
            self.parent, thread_worker=self.applications_page_worker)
        self.applications_page_update_handler.register_selected_tab_update_interval_handler(
            refresh_function=self.update_refresh_applications_page_apps)

        self.applications_page_worker.app_sig_applications_info.connect(
            self.update_applications_page
        )
        self.applications_page_worker.get_all_gtk_running_applications_info_loop(
            force_run=True, disable_loop=True
        )
        self.applications_page_worker.moveToThread(
            self.applications_page_thread
        )
        self.parent.task_manager_tab_widget.currentChanged.connect(
            self.update_thread_worker_info_retrieval_authorization)

        self.applications_page_thread.started.connect(
            self.applications_page_worker.run
        )
        self.applications_page_thread.start()
