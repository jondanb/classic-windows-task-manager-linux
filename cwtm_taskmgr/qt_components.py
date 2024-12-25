
import functools

from . import sys_utils
from .tm_tabbar.core_properties import (
    CWTM_ProcessesTabTableColumns,
    CWTM_ApplicationsTabTableColumns,
    CWTM_TabWidgetColumnEnum,
    CWTM_MenuBarStatusBarLabels,
    CWTM_MenuBarDynamicMenuFlags,
    CWTM_GlobalUpdateIntervals,
    CWTM_MENU_BAR_DYNAMIC_MENU_VISIBILITY_MAPPING,
)
from cwtm_taskmgr_ui.cwtm_taskmgr_dialog_ui import (
    Ui_CWTMTaskManagerConfirmationDialog
)

from PyQt5.QtWidgets import (
    QTableWidget, 
    QHeaderView, 
    QAbstractItemView,
    QGroupBox,
    QVBoxLayout
)
from PyQt5.QtCore import Qt


class CWTM_TaskManagerConfirmationDialog(Ui_CWTMTaskManagerConfirmationDialog):
    def __init__(self, *args, proc_name, proc_pid, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.proc_name = proc_name
        self.proc_pid = proc_pid

        self.set_process_name(self.proc_name)

        self.cancel_button.clicked.connect(
            self.close
        )
        self.confirm_button.clicked.connect(
            self.close
        )
        self.confirm_button.clicked.connect(
            functools.partial(sys_utils.end_process_by_pid, proc_pid)
        )

    def set_process_name(self, process_name):
        self.end_process_title_label.setText(
            f"Do you want to end \"{process_name}\"?"
        )

class CWTM_TabManager:
    def append_row_to_table(self, table_widget, table_enum, *row_data):
        # make sure the table can't be sorted while populating
        table_widget.setSortingEnabled(False)

        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)

        for column, row_properties in zip(list(table_enum), row_data):
            row_item_label = row_properties.item_label
            q_table_item_object = row_properties.item_type(row_item_label)

            if row_properties.item_icon is not None:
                q_table_item_object.setIcon(
                    sys_utils.gtk_image_to_qicon(row_properties.item_icon)
                )

            if row_properties.item_tool_tip:
                q_table_item_object.setToolTip(row_properties.item_tool_tip)

            table_widget.setItem(
                row_position, column, q_table_item_object
            )
            
        table_widget.setSortingEnabled(True)

    def set_table_column_ratios(self, table_widget, header_ratio):
        total_width = table_widget.viewport().width()
        for i, ratio in enumerate(header_ratio):
            table_widget.setColumnWidth(i, int(total_width * ratio))

    def setup_tab_page_table_widget(self, table_widget, header_ratio):
        table_widget.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft
        )
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        if isinstance(header_ratio, (tuple, list)):
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            table_widget.resizeEvent = lambda _: self.set_table_column_ratios(
                table_widget, header_ratio
            )
        elif isinstance(header_ratio, int): # Must be QHeaderView resize mode
            table_widget.horizontalHeader().setSectionResizeMode(header_ratio)
        
        table_widget.verticalHeader().setVisible(False)
        table_widget.verticalHeader().setDefaultSectionSize(10)
        table_widget.setShowGrid(False)

    def add_full_size_widget_to_groupbox(self, groupbox_name, groupbox_widget):
        widget_groupbox = QGroupBox(groupbox_name)
        widget_groupbox_layout = QVBoxLayout()

        widget_groupbox_layout.addWidget(groupbox_widget)
        widget_groupbox.setLayout(widget_groupbox_layout)

        return widget_groupbox

    def reselect_item_from_value(self, table_widget, table_column, previous_selected_item):
        # prevent item from being focused when table rows change
        table_widget.setAutoScroll(False)
        
        for row in range(table_widget.rowCount()):
            current_item = table_widget.item(row, table_column)
            current_item_value = current_item.text() \
                                 if current_item is not None else ""

            if previous_selected_item == current_item_value:
                table_widget.selectRow(row)

        table_widget.setAutoScroll(True)

    @staticmethod
    def get_current_selected_item_from_column(table_widget, table_column):
        table_widget_selection_model = table_widget.selectionModel()

        if not table_widget_selection_model.hasSelection():
            return None

        current_selected_row = table_widget_selection_model.selectedRows()[0]
        current_selected_item = table_widget.item(
            current_selected_row.row(), table_column
        )

        # can't return `current_selected_item` directly due to the C/C++
        # wrapper deleting it after use
        if current_selected_item is not None:
            return current_selected_item.text()


class CWTM_GlobalUpdateIntervalHandler:
    def __init__(self, parent, thread_worker):
        self.parent = parent
        self.thread_worker = thread_worker

    def register_selected_tab_update_interval_handler(self, *, refresh_function):
        self.parent.tm_view_menu_us_menu_high.triggered.connect(lambda:
            self.switch_selected_tab_update_speed(CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_HIGH))
        self.parent.tm_view_menu_us_menu_normal.triggered.connect(lambda:
            self.switch_selected_tab_update_speed(CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_NORMAL))
        self.parent.tm_view_menu_us_menu_low.triggered.connect(lambda:
            self.switch_selected_tab_update_speed(CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_LOW))
        self.parent.tm_view_menu_us_menu_paused.triggered.connect(lambda:
            self.switch_selected_tab_update_speed(CWTM_GlobalUpdateIntervals.GLOBAL_UPDATE_INTERVAL_PAUSED))

        self.parent.tm_view_menu_refresh_now.triggered.connect(
            refresh_function)

    def switch_selected_tab_update_speed(self, update_interval):
        self.thread_worker.timeout_interval = update_interval


class CWTM_MenuBarSignalHandler:
    def __init__(self, parent):
        self.parent = parent
        self.default_tab = CWTM_TabWidgetColumnEnum.TASK_MANAGER_APPLICATIONS_TAB

    def handle_tab_switch(self, tab_index):        
        if tab_index in CWTM_MENU_BAR_DYNAMIC_MENU_VISIBILITY_MAPPING:
            self._set_menu_visibility(
                CWTM_MENU_BAR_DYNAMIC_MENU_VISIBILITY_MAPPING[tab_index]
            )

        if tab_index != CWTM_TabWidgetColumnEnum.TASK_MANAGER_APPLICATIONS_TAB:
            self.parent.task_manager_windows_menu.menuAction().setVisible(False)
        else:
            self.parent.task_manager_windows_menu.menuAction().setVisible(True)

    def setup_menubar_signal_slots(self):
        self.parent.tm_file_menu_exit_task_manager.triggered.connect(
            self.parent.close)

    def setup_menubar_tab_visibility(self):
        self.parent.task_manager_tab_widget.currentChanged.connect(
            self.handle_tab_switch)
        self.parent.task_manager_tab_widget.setCurrentIndex(self.default_tab)
        self._set_menu_visibility(
            CWTM_MENU_BAR_DYNAMIC_MENU_VISIBILITY_MAPPING[self.default_tab]
        )

    def _set_menu_visibility(self, dynamic_menu_flags):
        self.parent.tm_view_menu_select_columns.setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.SELECT_COLUMNS))
        self.parent.tm_options_menu_show_full_account_name.setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.SHOW_FULL_ACCOUNT_NAME))
        self.parent.tm_view_menu_menu_cpu_history.menuAction().setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.CPU_HISTORY))
        self.parent.tm_view_menu_show_kernel_times.setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.SHOW_KERNEL_TIMES))
        self.parent.tm_view_menu_network_adapter_history.menuAction().setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.NETWORK_ADAPTER_HISTORY))
        self.parent.tm_options_menu_show_scale.setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.SHOW_SCALE))
        self.parent.tm_view_menu_menu_update_speed.menuAction().setVisible(
            bool(dynamic_menu_flags & CWTM_MenuBarDynamicMenuFlags.UPDATE_SPEED))

    def setup_menu_bar_status_bar_labels(self):
        self.parent.tm_file_menu_new_task_run.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_NEW_TASK)
        self.parent.tm_file_menu_exit_task_manager.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_EXIT_TASK_MANAGER)
        self.parent.tm_options_menu_always_on_top.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_ALWAYS_ON_TOP)
        self.parent.tm_options_menu_minimize_on_use.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_MINIMIZE_ON_USE)
        self.parent.tm_options_menu_hide_when_minimized.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_HIDE_WHEN_MINIMIZED)
        self.parent.tm_options_menu_show_scale.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_SHOW_SCALE)
        self.parent.tm_options_menu_show_full_account_name.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_SHOW_FULL_ACCOUNT_NAME)
        self.parent.tm_view_menu_refresh_now.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_REFRESH_NOW)
        self.parent.tm_view_menu_us_menu_high.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_HIGH)
        self.parent.tm_view_menu_us_menu_normal.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_NORMAL)
        self.parent.tm_view_menu_us_menu_low.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_LOW)
        self.parent.tm_view_menu_us_menu_paused.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_PAUSED)
        self.parent.tm_view_menu_select_columns.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_SELECT_COLUMNS)
        self.parent.tm_view_menu_cpu_one_graph_all_cpus.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_ONE_GRAPH_ALL_CPUS)
        self.parent.tm_view_menu_cpu_one_graph_per_cpu.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_ONE_GRAPH_PER_CPU)
        self.parent.tm_view_menu_show_kernel_times.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_SHOW_KERNEL_TIMES)
        self.parent.tm_view_menu_network_adapter_history.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_NETWORK_ADAPTER_HISTORY)
        self.parent.tm_view_menu_nas_bytes_sent.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_BYTES_SENT)
        self.parent.tm_view_menu_nas_bytes_received.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_BYTES_RECEIVED)
        self.parent.tm_view_menu_nas_bytes_total.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_BYTES_TOTAL)
        self.parent.tm_help_menu_task_manager_help_topics.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_HELP_TOPICS)
        self.parent.tm_help_menu_about_task_manager.setStatusTip(
            CWTM_MenuBarStatusBarLabels.LABEL_ABOUT_TASK_MANAGER)
