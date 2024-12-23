import enum
import functools

from .core_properties import (
    CWTM_ApplicationsTabTableColumns,
    CWTM_TableWidgetItemProperties
)
from ..qt_components import (
    CWTM_TabManager, 
    CWTM_TaskManagerConfirmationDialog
)
from ..thread_workers import CWTM_ApplicationsInfoRetrievalWorker

from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    QThread,
    QObject
)
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


class CWTM_ApplicationsTab(CWTM_TabManager):
    def __init__(self, parent):
        self.parent = parent

        self.APP_T_TASK_LIST_TABLE_COLUMN_RATIO = (0.85, 0.15)
        self.APP_T_TASK_LIST_TABLE_UPDATE_FREQUENCY = 1000 # 1 second

        self.parent.app_t_task_list_table.setColumnHidden(
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID, True
        ) # maybe change later???

        self.parent.app_t_new_task_button.clicked.connect(
            self.process_signal_app_t_new_task_button)
        self.parent.app_t_switch_to_button.clicked.connect(
            self.process_signal_app_t_switch_to_button)
        self.parent.app_t_end_task_button.clicked.connect(
            self.process_signal_app_t_end_task_button)

    def process_signal_app_t_new_task_button(self):
        return NotImplemented
    
    def process_signal_app_t_switch_to_button(self):
        return NotImplemented
    
    def process_signal_app_t_end_task_button(self):
        selected_application_pid = CWTM_TabManager.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_PID
        )
        selected_application_name = CWTM_TabManager.get_current_selected_item_from_column(
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

    def start_applications_page_updater_thread(self):
        self.applications_page_thread = QThread()
        self.applications_page_worker = CWTM_ApplicationsInfoRetrievalWorker(
            timeout_interval=self.APP_T_TASK_LIST_TABLE_UPDATE_FREQUENCY,
            parent_tab_widget=self.parent.task_manager_tab_widget
        )
        self.applications_page_worker.app_sig_applications_info.connect(
            self.update_applications_page
        )
        self.applications_page_worker.get_all_gtk_running_applications_info(
            force_run=True
        )
        self.applications_page_worker.moveToThread(
            self.applications_page_thread
        )

        self.applications_page_thread.started.connect(
            self.applications_page_worker.run
        )
        self.applications_page_thread.start()
