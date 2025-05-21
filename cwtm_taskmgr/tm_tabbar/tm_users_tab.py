from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QThread,
    QObject
)

from ..core_properties import (
    CWTM_UsersTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_TabWidgetColumnEnum,
    CWTM_UsersSystemInformationPacket
)
from ..qt_components import (
    CWTM_TableWidgetController,
    CWTM_TableWidgetUpdateInitializer
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_UsersInfoRetrievalWorker

from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_UsersTabCustomContextMenu


class CWTM_UsersTab(QObject, CWTM_TableWidgetController):
    def __init__(self, *args, parent, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        
        self.parent = parent

        self.USERS_T_USERS_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL

        self.parent.users_t_users_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.users_t_users_list_table.customContextMenuRequested.connect(
            self.process_custom_users_context_menu_request)

        self.parent.users_t_logoff_button.setDisabled(True) # Not Implemented
        self.parent.users_t_send_message_button.setDisabled(True) # Not Implemented

    def process_custom_users_context_menu_request(self, position):
        current_selected_item = self.parent.users_t_users_list_table.itemAt(position)
        
        if current_selected_item is None:
            return

        custom_applications_context_menu = CWTM_UsersTabCustomContextMenu(parent=self.parent)
        custom_applications_context_menu.exec_(
            self.parent.users_t_users_list_table.mapToGlobal(position))
            
    def update_users_page(
        self, system_user_details: list[CWTM_UsersSystemInformationPacket], user_gtk_icons: list) -> None:
        with CWTM_TableWidgetUpdateInitializer(self.parent.users_t_users_list_table):
            for user_gtk_icon, user_information in zip(user_gtk_icons, system_user_details):
                is_logged_in_label = "Active" if user_information.u_is_logged_in else "Disconnected"

                self.append_row_to_table(
                    self.parent.users_t_users_list_table, CWTM_UsersTabTableColumns,
                    CWTM_TableWidgetItemProperties(
                        item_label=user_information.u_user_name, item_icon=user_gtk_icon),
                    CWTM_TableWidgetItemProperties(
                        item_label=str(user_information.u_user_uid), item_type=CWTM_QNumericTableWidgetItem),
                    CWTM_TableWidgetItemProperties(item_label=is_logged_in_label),
                    CWTM_TableWidgetItemProperties(item_label=user_information.u_real_name),
                    CWTM_TableWidgetItemProperties(item_label=user_information.u_home_dir)
                ) 

    @pyqtSlot()
    def update_refresh_user_page_usrs(self):
        self.users_page_worker.get_all_users_information_loop(disable_loop=True)

    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the users thread worker to emit system user information to the slot
        `update_users_page`

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
        self.users_page_worker.get_all_users_information_loop(
            force_run=True, disable_loop=True
        )
        self.users_page_worker.moveToThread(
            self.users_page_thread
        )
        self.parent.task_manager_tab_widget.currentChanged.connect(
            self.update_thread_worker_info_retrieval_authorization)

        self.users_page_thread.started.connect(
            self.users_page_worker.run
        )
        self.users_page_thread.start()
