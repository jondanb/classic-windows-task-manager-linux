from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QThread,
    QObject
)

from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ServicesTabCustomContextMenu

from ..qt_components import CWTM_TableWidgetController
from ..core_properties import (
    CWTM_ServicesTabTableColumns,
    CWTM_ProcessesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_TabWidgetColumnEnum,
    CWTM_ServiceInformationFrame
)
from ..qt_widgets import CWTM_QNumericTableWidgetItem
from ..thread_workers import CWTM_ServicesInfoRetrievalWorker


class CWTM_ServicesTab(QObject, CWTM_TableWidgetController):
    def __init__(self, *args, parent, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self.parent = parent

        self.SVC_T_SERVICES_LIST_TABLE_COLUMN_RATIO = (0.25, 0.1, 0.50, 0.15)
        self.SVC_T_SERVICES_LIST_TABLE_UPDATE_FREQUENCY = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_LOW # 4 seconds

        self.custom_services_context_menu = CWTM_ServicesTabCustomContextMenu(
            parent=self.parent)

        self.parent.svc_t_services_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.svc_t_services_list_table.customContextMenuRequested.connect(
            self.process_custom_services_context_menu_request)
        self.custom_services_context_menu.svcs_go_to_process_action.triggered.connect(
            self.process_context_menu_action_go_to_process)

    def process_context_menu_action_go_to_process(self):
        selected_service_pid = self.get_current_selected_item_from_column(
            self.parent.svc_t_services_list_table, 
            CWTM_ServicesTabTableColumns.SVC_T_SERVICES_LIST_TABLE_PID)

        process_tab_row = self.find_row_from_column_value(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID,
            selected_service_pid)

        if process_tab_row > 0:
            self.parent.task_manager_tab_widget.setCurrentIndex(
                CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB)
            self.parent.proc_t_proc_list_table.selectRow(process_tab_row)

    def process_custom_services_context_menu_request(self, position):
        current_selected_item = self.parent.svc_t_services_list_table.itemAt(position)
        
        if current_selected_item is None:
            return

        self.custom_services_context_menu.exec_(
            self.parent.svc_t_services_list_table.mapToGlobal(position))

    def update_services_page(self, system_all_services: list[CWTM_ServiceInformationFrame]) -> None:
        self.parent.svc_t_services_list_table.setRowCount(0)
        self.parent.svc_t_services_list_table.setSortingEnabled(False)

        for system_service in system_all_services:
            self.append_row_to_table(
                self.parent.svc_t_services_list_table, CWTM_ServicesTabTableColumns,
                CWTM_TableWidgetItemProperties(
                    item_label=system_service.svc_name, item_tool_tip=system_service.svc_name),
                CWTM_TableWidgetItemProperties(item_label=str(system_service.svc_pid), 
                    item_type=CWTM_QNumericTableWidgetItem),
                CWTM_TableWidgetItemProperties(
                    item_label=system_service.svc_desc, item_tool_tip=system_service.svc_desc),
                CWTM_TableWidgetItemProperties(system_service.svc_status.upper())
            )

        self.parent.svc_t_services_list_table.setSortingEnabled(True)

    @pyqtSlot()
    def update_refresh_services_page_svcs(self):
        #current_tab_widget = self.parent.task_manager_tab_widget.currentIndex()
        self.services_page_worker.get_all_services_information_loop(disable_loop=True)

    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the services thread worker to emit system service information to the slot
        `update_services_page`

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