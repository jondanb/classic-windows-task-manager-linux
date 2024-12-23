import enum
import functools

from .. import sys_utils
from .core_properties import (
    CWTM_UsersTabTableColumns,
    CWTM_TableWidgetItemProperties
)
from ..qt_components import CWTM_TabManager
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


class CWTM_UsersTab(CWTM_TabManager):
    def __init__(self, parent):
        self.parent = parent

        self.USERS_T_USERS_LIST_TABLE_UPDATE_FREQUENCY = 300_000 # 5 minutes
            
    def update_users_page(self):
        self.parent.users_t_users_list_table.setRowCount(0)
        
        *system_user_details, = sys_utils.get_all_user_accounts_details()
        user_gtk_icons = sys_utils.get_user_account_type_icon(system_user_details)

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

    def start_users_page_updater_thread(self):
        self.users_page_thread = QThread()
        users_page_worker = CWTM_PageUpdaterWorkerThread(
            tm_update_function=functools.partial(
                self.__start_users_page_updater,
                self.USERS_T_USERS_LIST_TABLE_UPDATE_FREQUENCY)
        )

        users_page_worker.moveToThread(self.users_page_thread)

        self.users_page_thread.started.connect(
            users_page_worker.tm_update_function
        )
        self.users_page_thread.start()


    def __start_users_page_updater(self, timeout_frequency):
        self.update_users_page()
        
        self.users_update_timer = QTimer()
        self.users_update_timer.timeout.connect(
            self.update_users_page
        )
        self.users_update_timer.start(timeout_frequency)
