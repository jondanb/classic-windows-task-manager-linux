import enum
import functools

from .. import sys_utils
from .core_properties import (
    CWTM_UsersTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_TabWidgetColumnEnum
)
from ..qt_components import CWTM_TableWidgetController
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_UsersInfoRetrievalWorker

from PyQt5.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    pyqtSlot,
    QThread,
    QObject
)
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView 


class CWTM_UsersTab(CWTM_TableWidgetController):
    def __init__(self, parent):
        self.parent = parent

        self.USERS_T_USERS_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL
            
    def update_users_page(self, system_user_details: list, user_gtk_icons: list):
        self.parent.users_t_users_list_table.setRowCount(0)

        for user_gtk_icon, (u_user_name, u_user_uid, u_is_logged_in,
             u_real_name, u_home_dir) in zip(user_gtk_icons, system_user_details):
            is_logged_in_label = "Active" if u_is_logged_in else "Disconnected"

            self.append_row_to_table(
                self.parent.users_t_users_list_table, CWTM_UsersTabTableColumns,
                CWTM_TableWidgetItemProperties(item_label=u_user_name, 
                    item_icon=user_gtk_icon),
                CWTM_TableWidgetItemProperties(item_label=str(u_user_uid), 
                    item_type=CWTM_QNumericTableWidgetItem),
                CWTM_TableWidgetItemProperties(item_label=is_logged_in_label),
                CWTM_TableWidgetItemProperties(item_label=u_real_name),
                CWTM_TableWidgetItemProperties(item_label=u_home_dir)
            ) 

    @pyqtSlot()
    def update_refresh_user_page_usrs(self):
        #current_tab_widget = self.parent.task_manager_tab_widget.currentIndex()
        self.users_page_worker.get_all_users_information_frame()

    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the processes thread worker to emit system process information to the slot
        `update_processes_page`

        Arguments:
            - index: the current index of the tab widget
        """
        self.users_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_USERS_TAB)

    def start_users_page_updater_thread(self):
        self.users_page_thread = QThread()
        self.users_page_worker = CWTM_UsersInfoRetrievalWorker(
            timeout_interval=self.USERS_T_USERS_LIST_TABLE_UPDATE_FREQUENCY)
        # no need for CWTM_GlobalUpdateIntervalHandler since user won't be connected
        # to timeout interval changer for users tab

        self.users_page_worker.users_sig_user_account_info.connect(
            self.update_users_page
        )
        self.users_page_worker.get_all_users_information_frame(
            force_run=True
        )
        self.users_page_worker.moveToThread(
            self.users_page_thread
        )

        self.users_page_thread.started.connect(
            self.users_page_worker.run
        )
        self.users_page_thread.start()
