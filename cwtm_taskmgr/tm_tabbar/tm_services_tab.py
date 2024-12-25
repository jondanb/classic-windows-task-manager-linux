import dbus
import enum
import functools

from .. import sys_utils
from ..qt_components import CWTM_TabManager
from .core_properties import (
    CWTM_ServicesTabTableColumns,
    CWTM_TableWidgetItemProperties,
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_PageUpdaterWorkerThread


from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    QThread,
    QObject
)
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class CWTM_ServicesTab(CWTM_TabManager):
    def __init__(self, parent):
        self.parent = parent

        self.SVC_T_SERVICES_LIST_TABLE_COLUMN_RATIO = (0.25, 0.1, 0.50, 0.15)
        self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY = 360_000 # 5 minutes

    def update_services_page(self):
        self.parent.svc_t_services_list_table.setRowCount(0)
        system_all_services = sys_utils.get_all_system_services()

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

    def start_services_page_updater_thread(self):
        self.services_page_thread = QThread()
        services_page_worker = CWTM_PageUpdaterWorkerThread(
            tm_update_function=functools.partial(
                self.__start_services_page_updater,
                self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY)
        )

        services_page_worker.moveToThread(self.services_page_thread)

        self.services_page_thread.started.connect(
            services_page_worker.tm_update_function
        )
        self.services_page_thread.start()

    def __start_services_page_updater(self, timeout_frequency):
        self.update_services_page()
        
        self.services_update_timer = QTimer()
        self.services_update_timer.timeout.connect(
            self.update_services_page
        )
        self.services_update_timer.start(timeout_frequency)
