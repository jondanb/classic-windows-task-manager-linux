import dbus
import enum
import functools

from .. import sys_utils
from ..qt_components import CWTM_TableWidgetController
from .core_properties import (
    CWTM_ServicesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_ServicesInfoRetrievalWorker


from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    pyqtSlot,
    QThread,
    QObject
)
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class CWTM_ServicesTab(CWTM_TableWidgetController):
    def __init__(self, parent):
        self.parent = parent

        self.SVC_T_SERVICES_LIST_TABLE_COLUMN_RATIO = (0.25, 0.1, 0.50, 0.15)
        self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_LOW # 4 seconds

    def update_services_page(self, system_all_services: list) -> None:
        self.parent.svc_t_services_list_table.setRowCount(0)

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

    @pyqtSlot()
    def update_refresh_services_page_svcs(self):
        #current_tab_widget = self.parent.task_manager_tab_widget.currentIndex()
        self.services_page_worker.get_all_services_information_frame()

    def start_services_page_updater_thread(self):
        self.services_page_thread = QThread()
        self.services_page_worker = CWTM_ServicesInfoRetrievalWorker(
            parent_tab_widget=self.parent.task_manager_tab_widget, #change
            timeout_interval=self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY)
        # no need for CWTM_GlobalUpdateIntervalHandler since services won't be connected
        # to timeout interval changer

        self.services_page_worker.svc_sig_all_system_services.connect(
            self.update_services_page
        )
        self.services_page_worker.get_all_services_information_frame(
            force_run=True
        )
        self.services_page_worker.moveToThread(
            self.services_page_thread
        )

        self.services_page_thread.started.connect(
            self.services_page_worker.run
        )
        self.services_page_thread.start()