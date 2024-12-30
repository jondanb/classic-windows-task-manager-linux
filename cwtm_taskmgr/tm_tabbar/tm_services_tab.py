import dbus
import enum
import functools

from .. import sys_utils
from ..qt_components import CWTM_TableWidgetController
from ..core_properties import (
    CWTM_ServicesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_TabWidgetColumnEnum
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_ServicesInfoRetrievalWorker


from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    pyqtSlot,
    QThread
)
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ServicesTabCustomContextMenu


class CWTM_ServicesTab(CWTM_TableWidgetController):
    def __init__(self, parent):
        self.parent = parent

        self.SVC_T_SERVICES_LIST_TABLE_COLUMN_RATIO = (0.25, 0.1, 0.50, 0.15)
        self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_LOW # 4 seconds

        self.parent.svc_t_services_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.svc_t_services_list_table.customContextMenuRequested.connect(
            self.process_custom_applications_context_menu_request)

    def process_custom_applications_context_menu_request(self, position):
        current_selected_item = self.parent.svc_t_services_list_table.itemAt(position)
        
        if current_selected_item is None:
            return

        custom_applications_context_menu = CWTM_ServicesTabCustomContextMenu(parent=self.parent)
        custom_applications_context_menu.exec_(
            self.parent.svc_t_services_list_table.mapToGlobal(position))

    def update_services_page(self, system_all_services: list) -> None:
        self.parent.svc_t_services_list_table.setRowCount(0)
        self.parent.svc_t_services_list_table.setSortingEnabled(False)

        for (svc_name, svc_pid, svc_desc, svc_status) \
            in system_all_services:
            self.append_row_to_table(
                self.parent.svc_t_services_list_table, CWTM_ServicesTabTableColumns,
                CWTM_TableWidgetItemProperties(item_label=svc_name, item_tool_tip=svc_name),
                CWTM_TableWidgetItemProperties(item_label=str(svc_pid), 
                    item_type=CWTM_QNumericTableWidgetItem),
                CWTM_TableWidgetItemProperties(item_label=svc_desc, item_tool_tip=svc_desc),
                CWTM_TableWidgetItemProperties(svc_status.upper())
            )

        self.parent.svc_t_services_list_table.setSortingEnabled(True)

    @pyqtSlot()
    def update_refresh_services_page_svcs(self):
        #current_tab_widget = self.parent.task_manager_tab_widget.currentIndex()
        self.services_page_worker.get_all_services_information_loop(disable_loop=True)

    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the processes thread worker to emit system process information to the slot
        `update_processes_page`

        Arguments:
            - index: the current index of the tab widget
        """
        self.services_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_SERVICES_TAB)

    def start_services_page_updater_thread(self):
        self.services_page_thread = QThread()
        self.services_page_worker = CWTM_ServicesInfoRetrievalWorker(
            timeout_interval=self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY)
        # no need for CWTM_GlobalUpdateIntervalHandler since services won't be connected
        # to timeout interval changer

        self.services_page_worker.svc_sig_all_system_services.connect(
            self.update_services_page
        )
        self.services_page_worker.get_all_services_information_loop(
            force_run=True, disable_loop=True
        )
        self.services_page_worker.moveToThread(
            self.services_page_thread
        )
        self.parent.task_manager_tab_widget.currentChanged.connect(
            self.update_thread_worker_info_retrieval_authorization)

        self.services_page_thread.started.connect(
            self.services_page_worker.run
        )
        self.services_page_thread.start()