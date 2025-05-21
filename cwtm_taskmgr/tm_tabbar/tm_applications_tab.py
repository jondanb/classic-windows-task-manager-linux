from PyQt5.QtCore import (
    Qt, 
    pyqtSignal, 
    pyqtSlot,
    QThread,
    QObject,
    QPoint
)
from PyQt5.QtWidgets import QTableWidgetItem, QDialog

from ..core_properties import (
    CWTM_ApplicationsTabTableColumns,
    CWTM_ProcessesTabTableColumns,
    CWTM_TableWidgetItemProperties,
    CWTM_GlobalUpdateIntervals,
    CWTM_TabWidgetColumnEnum,
    CWTM_ApplicationInformationPacket
)
from ..qt_components import (
    CWTM_TableWidgetController, 
    CWTM_TaskManagerConfirmationDialog,
    CWTM_GlobalUpdateIntervalHandler,
    CWTM_TaskManagerNewTaskDialog,
    CWTM_TableWidgetUpdateInitializer
)
from ..thread_workers import CWTM_ApplicationsInfoRetrievalWorker

from cwtm_taskmgr_ui.cwtm_taskmgr_ui import CWTM_ApplicationsTabCustomContextMenu


class CWTM_ApplicationsTab(QObject, CWTM_TableWidgetController):
    def __init__(self, *args: list, parent: QObject, **kwargs: dict) -> None:
        """
        Initializes the applications tab for the task manager. This function sets up all the properties for
        the applications tab including the:
            - Applications QTableWidget column width ratio.
            - The update interval speed based on the enum properties of CWTM_GlobalUpdateIntervals.
            - All the button/custom context menu action signals and slots.

        Arguments:
            - args and kwargs: any arbitrary extra argument/keywork arguments to be passed into the
                main superclass. (QObject)
            - parent (QObject): Initialize the class with the parent as a property the superclass. 
        """
        super().__init__(*args, parent=parent, **kwargs)
        
        self.parent: QObject = parent

        self.APP_T_TASK_LIST_TABLE_COLUMN_RATIO: tuple[float] = (0.85, 0.15)
        self.APP_T_TASK_LIST_TABLE_UPDATE_FREQUENCY: CWTM_GlobalUpdateIntervals = \
            CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL

        self.parent.app_t_task_list_table.setColumnHidden(
            CWTM_ApplicationsTabTableColumns._APP_T_TASK_LIST_TABLE_PID, True
        ) # maybe change later???

        # Buttons
        self.parent.app_t_end_task_button.clicked.connect(
            self.process_signal_app_t_end_task_button)
        self.parent.app_t_new_task_button.clicked.connect(
            self.process_signal_app_t_new_task_button)
        self.parent.tm_file_menu_new_task_run.triggered.connect(
            self.process_signal_app_t_new_task_button)

        # Context Menu
        self.custom_applications_context_menu = CWTM_ApplicationsTabCustomContextMenu(
            parent=self.parent)
        self.parent.app_t_task_list_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parent.app_t_task_list_table.customContextMenuRequested.connect(
            self.process_custom_applications_context_menu_request)

        self.custom_applications_context_menu.app_t_table_tile_end_task_action.triggered.connect(
            self.process_signal_app_t_end_task_button)
        self.custom_applications_context_menu.app_t_table_go_to_process_action.triggered.connect(
            self.process_context_menu_action_go_to_process)

    @pyqtSlot()
    def process_context_menu_action_go_to_process(self) -> None:
        """
        Slot to process the action of referencing a process in the processes tab based on the PID
        of the application. If the process is somehow not found (by PID), it will not switch to the 
        processes tab with the selected application's process info selected.
        """
        selected_application_pid: str = self.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table, 
            CWTM_ApplicationsTabTableColumns._APP_T_TASK_LIST_TABLE_PID)

        process_tab_row: int = self.find_row_from_column_value(
            self.parent.proc_t_proc_list_table, 
            CWTM_ProcessesTabTableColumns.PROC_T_PROC_LIST_TABLE_PID,
            selected_application_pid)

        if process_tab_row > 0:
            self.parent.task_manager_tab_widget.setCurrentIndex(
                CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB)
            self.parent.proc_t_proc_list_table.selectRow(process_tab_row)

    @pyqtSlot(QPoint)
    def process_custom_applications_context_menu_request(self, position: QPoint) -> None:
        """
        Slot to find the current selected item in the tab's table widget and pass it off to the
        custom context menu assigned to the QTableWidgetItem(s).

        Arguments:
            - position (QPoint): The position of the current selected item in the table widget.
        """
        current_selected_item: QTableWidgetItem = self.parent.app_t_task_list_table.itemAt(position)

        if current_selected_item is None:
            return

        self.custom_applications_context_menu.exec_(
            self.parent.app_t_task_list_table.mapToGlobal(position))

    @pyqtSlot()
    def process_signal_app_t_new_task_button(self) -> None:
        """
        Slot to initialize the new task dialog when creating a new task.
        """
        new_task_dialog: QDialog = CWTM_TaskManagerNewTaskDialog(parent=self.parent)
        new_task_dialog.exec_()
    
    @pyqtSlot()
    def process_signal_app_t_end_task_button(self) -> None:
        """
        Slot to process the action of ending a task in the applications tab.
        """
        selected_application_pid: str = CWTM_TableWidgetController.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns._APP_T_TASK_LIST_TABLE_PID
        )
        selected_application_name: str = CWTM_TableWidgetController.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns.APP_T_TASK_LIST_TABLE_TASK
        )

        if selected_application_pid is None:
            return

        confirmation_dialog: QDialog = CWTM_TaskManagerConfirmationDialog(
            proc_name=selected_application_name, proc_pid=int(selected_application_pid)
        )
        confirmation_dialog.exec_()

    @pyqtSlot(list)
    def update_applications_page(self, gtk_running_apps_icons: list[CWTM_ApplicationInformationPacket]) -> None:
        """
        Slot to update the applications table widget with new application information.

        Arguments:
            - gtk_running_apps_icons (list[CWTM_ApplicationInformationPacket]): 
                Contains a list of information packets for each running application.
        """
        current_selected_item: str = self.get_current_selected_item_from_column(
            self.parent.app_t_task_list_table,
            CWTM_ApplicationsTabTableColumns._APP_T_TASK_LIST_TABLE_PID
        )
        
        with CWTM_TableWidgetUpdateInitializer(self.parent.app_t_task_list_table):
            for gtk_application in gtk_running_apps_icons:
                if not gtk_application.gtk_app_name:
                    continue

                self.append_row_to_table(
                    self.parent.app_t_task_list_table, CWTM_ApplicationsTabTableColumns,
                    CWTM_TableWidgetItemProperties(
                        item_label=gtk_application.gtk_app_name, item_icon=gtk_application.gtk_app_icon),
                    CWTM_TableWidgetItemProperties(item_label="Running"), # maybe change later
                    CWTM_TableWidgetItemProperties(item_label=str(gtk_application.gtk_app_pid)) # for private use, maybe also change later
                )

        if current_selected_item is not None:
            self.reselect_item_from_value(
                self.parent.app_t_task_list_table,
                CWTM_ApplicationsTabTableColumns._APP_T_TASK_LIST_TABLE_PID,
                current_selected_item
            )

    @pyqtSlot()
    def update_refresh_applications_page(self) -> None:
        """
        Refreshes the applications page by requesting an information retrieval from the application's
        thread worker.
        """
        self.applications_page_worker.get_all_gtk_running_applications_info_loop(disable_loop=True)

    @pyqtSlot(int)
    def update_thread_worker_info_retrieval_authorization(self, index: int) -> None:
        """
        Authorizes the applications thread worker to emit system application information to the slot
        `update_applications_page`

        Arguments:
            - index (int): the current index of the tab widget
        """
        self.applications_page_worker._information_retrieval_authorization.emit(
            index == CWTM_TabWidgetColumnEnum.TASK_MANAGER_APPLICATIONS_TAB)

    def start_applications_page_updater_thread(self):
        """
        Starts the applications page updater thread loop.
        """
        self.applications_page_thread: QThread = QThread()
        self.applications_page_worker: CWTM_ApplicationsInfoRetrievalWorker = CWTM_ApplicationsInfoRetrievalWorker(
            timeout_interval=self.APP_T_TASK_LIST_TABLE_UPDATE_FREQUENCY)
        self.applications_page_update_handler = CWTM_GlobalUpdateIntervalHandler(
            self.parent, thread_worker=self.applications_page_worker)
        self.applications_page_update_handler.register_selected_tab_update_interval_handler(
            refresh_function=self.update_refresh_applications_page)

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
