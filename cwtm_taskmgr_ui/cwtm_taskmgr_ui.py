# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowwosttf.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore

from resources import resources
from cwtm_taskmgr.core_properties import (
    CWTM_PriorityNicenessRanges,
    CWTM_PriorityNicenessLevels
)


class CWTM_ApplicationsTabCustomContextMenu(QMenu):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self.app_t_table_switch_to_action = QAction("       Switch To")  # bold
        self.app_t_table_bring_to_front_action = QAction("       Bring To Front")
        self.app_t_table_minimize_action = QAction("       Minimize")
        self.app_t_table_maximize_action = QAction("       Maximize")
        self.app_t_table_cascade_action = QAction("       Cascade")
        self.app_t_table_tile_horizontally_action = QAction("       Tile Horizontally")
        self.app_t_table_tile_vertically_action = QAction("       Tile Vertically")
        self.app_t_table_tile_end_task_action = QAction("       End Task")
        self.app_t_table_create_dump_file_action = QAction("       Create Dump File")
        self.app_t_table_go_to_process_action = QAction("       Go To Process")

        # Make "Switch To" action bold
        self.app_t_table_switch_to_action_font = self.app_t_table_switch_to_action.font()
        self.app_t_table_switch_to_action_font.setBold(True)
        self.app_t_table_switch_to_action.setFont(self.app_t_table_switch_to_action_font)

        # Disable unimplemented actions
        self.app_t_table_switch_to_action.setDisabled(True)  # Not Implemented
        self.app_t_table_bring_to_front_action.setDisabled(True)  # Not Implemented
        self.app_t_table_cascade_action.setDisabled(True)  # Not Implemented
        self.app_t_table_tile_horizontally_action.setDisabled(True)  # Not Implemented
        self.app_t_table_tile_vertically_action.setDisabled(True)  # Not Implemented
        self.app_t_table_create_dump_file_action.setDisabled(True) # Not Implemented

        # Add actions to the menu
        self.addAction(self.app_t_table_switch_to_action)
        self.addAction(self.app_t_table_bring_to_front_action)
        self.addSeparator()
        self.addAction(self.app_t_table_minimize_action)
        self.addAction(self.app_t_table_maximize_action)
        self.addAction(self.app_t_table_cascade_action)
        self.addAction(self.app_t_table_tile_horizontally_action)
        self.addAction(self.app_t_table_tile_vertically_action)
        self.addSeparator()
        self.addAction(self.app_t_table_tile_end_task_action)
        self.addAction(self.app_t_table_create_dump_file_action)
        self.addAction(self.app_t_table_go_to_process_action)


class CWTM_ProcessesTabCustomContextMenu(QMenu):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self.proc_open_file_location_action = QAction("       Open File Location")
        self.proc_end_process_action = QAction("       End Process")
        self.proc_end_process_tree_action = QAction("       End Process Tree")
        self.proc_debug_action = QAction("       Debug")
        self.proc_uac_virtualization_action = QAction("       UAC Virtualization")
        self.proc_create_dump_file_action = QAction("       Create Dump File")
        self.proc_set_affinity_action = QAction("       Set Affinity")
        self.proc_properties_action = QAction("       Properties")
        self.proc_go_to_service_action = QAction("       Go To Service(s)")

        self.proc_set_priority_menu = QMenu("       Set Priority")
        self.proc_set_priority_menu_action_group = QActionGroup(self.proc_set_priority_menu)

        self.proc_set_priority_realtime = QAction("Realtime")
        self.proc_set_priority_high = QAction("High")
        self.proc_set_priority_above_normal = QAction("Above normal")
        self.proc_set_priority_normal = QAction("Normal")
        self.proc_set_priority_below_normal = QAction("Below normal")
        self.proc_set_priority_low = QAction("Low")

        self.proc_set_priority_realtime.setCheckable(True)
        self.proc_set_priority_high.setCheckable(True)
        self.proc_set_priority_above_normal.setCheckable(True)
        self.proc_set_priority_normal.setCheckable(True)
        self.proc_set_priority_below_normal.setCheckable(True)
        self.proc_set_priority_low.setCheckable(True)

        self.proc_set_priority_normal.setChecked(True)

        self.proc_set_priority_realtime.niceness_level = CWTM_PriorityNicenessLevels.PRIORITY_LEVEL_REALTIME
        self.proc_set_priority_high.niceness_level = CWTM_PriorityNicenessLevels.PRIORITY_LEVEL_HIGH
        self.proc_set_priority_above_normal.niceness_level = CWTM_PriorityNicenessLevels.PRIORITY_LEVEL_ABOVE_NORMAL
        self.proc_set_priority_normal.niceness_level = CWTM_PriorityNicenessLevels.PRIORITY_LEVEL_NORMAL
        self.proc_set_priority_below_normal.niceness_level = CWTM_PriorityNicenessLevels.PRIORITY_LEVEL_BELOW_NORMAL
        self.proc_set_priority_low.niceness_level = CWTM_PriorityNicenessLevels.PRIORITY_LEVEL_LOW

        self.proc_set_priority_menu.addAction(self.proc_set_priority_realtime)
        self.proc_set_priority_menu.addAction(self.proc_set_priority_high)
        self.proc_set_priority_menu.addAction(self.proc_set_priority_above_normal)
        self.proc_set_priority_menu.addAction(self.proc_set_priority_normal)
        self.proc_set_priority_menu.addAction(self.proc_set_priority_below_normal)
        self.proc_set_priority_menu.addAction(self.proc_set_priority_low)

        self.proc_set_priority_menu_action_group.addAction(self.proc_set_priority_realtime)
        self.proc_set_priority_menu_action_group.addAction(self.proc_set_priority_high)
        self.proc_set_priority_menu_action_group.addAction(self.proc_set_priority_above_normal)
        self.proc_set_priority_menu_action_group.addAction(self.proc_set_priority_normal)
        self.proc_set_priority_menu_action_group.addAction(self.proc_set_priority_below_normal)
        self.proc_set_priority_menu_action_group.addAction(self.proc_set_priority_low)

        self.proc_set_priority_menu_action_group.setExclusive(True)

        # Disabled unimplemented actions
        self.proc_debug_action.setDisabled(True)  # Not Implemented
        self.proc_uac_virtualization_action.setDisabled(True)  # Not Implemented
        self.proc_create_dump_file_action.setDisabled(True)  # Not Implemented

        # Add actions to the menu
        self.addAction(self.proc_open_file_location_action)
        self.addSeparator()
        self.addAction(self.proc_end_process_action)
        self.addAction(self.proc_end_process_tree_action)
        self.addAction(self.proc_debug_action)
        self.addAction(self.proc_uac_virtualization_action)
        self.addAction(self.proc_create_dump_file_action)
        self.addSeparator()
        self.addAction(self.proc_set_priority_menu.menuAction())
        self.addAction(self.proc_set_affinity_action)
        self.addSeparator()
        self.addAction(self.proc_properties_action)
        self.addAction(self.proc_go_to_service_action)

    def set_priority_action_group_checked_from_niceness(self, process_niceness):
        if process_niceness in CWTM_PriorityNicenessRanges.PRIORITY_RANGE_REALTIME:
            self.proc_set_priority_realtime.setChecked(True)
        elif process_niceness in CWTM_PriorityNicenessRanges.PRIORITY_RANGE_HIGH:
            self.proc_set_priority_high.setChecked(True)
        elif process_niceness in CWTM_PriorityNicenessRanges.PRIORITY_RANGE_ABOVE_NORMAL:
            self.proc_set_priority_above_normal.setChecked(True)
        elif process_niceness in CWTM_PriorityNicenessRanges.PRIORITY_RANGE_NORMAL:
            self.proc_set_priority_normal.setChecked(True)
        elif process_niceness in CWTM_PriorityNicenessRanges.PRIORITY_RANGE_BELOW_NORMAL:
            self.proc_set_priority_below_normal.setChecked(True)
        else: # CWTM_PriorityNicenessRanges.PRIORITY_RANGE_LOW
            self.proc_set_priority_low.setChecked(True)


class CWTM_ServicesTabCustomContextMenu(QMenu):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self.svcs_start_service_action = QAction("       Start Service")
        self.svcs_stop_service_action = QAction("       Stop Service")
        self.svcs_go_to_process_action = QAction("       Go to Process")

        # Add actions to the menu
        self.addAction(self.svcs_start_service_action)
        self.addAction(self.svcs_stop_service_action)
        self.addSeparator()
        self.addAction(self.svcs_go_to_process_action)


class CWTM_UsersTabCustomContextMenu(QMenu):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self.usrs_send_message_action = QAction("       Send Message")  # bold
        self.usrs_connect_action = QAction("       Connect")
        self.usrs_disconnect_action = QAction("       Disconnect")
        self.usrs_log_off_action = QAction("       Log Off")
        self.usrs_remote_control_action = QAction("       Remote Control")

        # Make "Send Message" action bold
        self.usrs_send_message_action_font = self.usrs_send_message_action.font()
        self.usrs_send_message_action_font.setBold(True)
        self.usrs_send_message_action.setFont(self.usrs_send_message_action_font)

        # Disabled unimplemented actions
        self.usrs_send_message_action.setDisabled(True)  # Not Implemented
        self.usrs_log_off_action.setDisabled(True)  # Not Implemented
        self.usrs_remote_control_action.setDisabled(True)  # Not Implemented

        # Add actions to the menu
        self.addAction(self.usrs_send_message_action)
        self.addSeparator()
        self.addAction(self.usrs_connect_action)
        self.addAction(self.usrs_disconnect_action)
        self.addAction(self.usrs_log_off_action)
        self.addAction(self.usrs_remote_control_action)


class Ui_CWTM_TaskManagerMainWindow(QMainWindow):
    def setupUi(self, CWTM_TaskManagerMainWindow):
        if not CWTM_TaskManagerMainWindow.objectName():
            CWTM_TaskManagerMainWindow.setObjectName(u"CWTM_TaskManagerMainWindow")
        CWTM_TaskManagerMainWindow.resize(530, 565)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CWTM_TaskManagerMainWindow.sizePolicy().hasHeightForWidth())
        CWTM_TaskManagerMainWindow.setSizePolicy(sizePolicy)
        CWTM_TaskManagerMainWindow.setMinimumSize(QSize(530, 565))
        CWTM_TaskManagerMainWindow.setMaximumSize(QSize(530, 565))
        
        self.centralwidget = QWidget(CWTM_TaskManagerMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.task_manager_tab_widget = QTabWidget(self.centralwidget)
        self.task_manager_tab_widget.setObjectName(u"task_manager_tab_widget")

        with open("./cwtm_taskmgr_ui/qt_stylesheets/cwtm_tab_widget.qss", "r") as tab_widget_stylesheet_file:
            self.task_manager_tab_widget.setStyleSheet(tab_widget_stylesheet_file.read())
            
        self.applications_tab = QWidget()
        self.applications_tab.setObjectName(u"applications_tab")
        self.app_t_task_list_table = QTableWidget(self.applications_tab)
        if (self.app_t_task_list_table.columnCount() < 3):
            self.app_t_task_list_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.app_t_task_list_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.app_t_task_list_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.app_t_task_list_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.app_t_task_list_table.setObjectName(u"app_t_task_list_table")
        self.app_t_task_list_table.setGeometry(QRect(0, 0, 510, 441))
        self.app_t_new_task_button = QPushButton(self.applications_tab)
        self.app_t_new_task_button.setObjectName(u"app_t_new_task_button")
        self.app_t_new_task_button.setGeometry(QRect(400, 450, 111, 24))
        self.app_t_switch_to_button = QPushButton(self.applications_tab)
        self.app_t_switch_to_button.setObjectName(u"app_t_switch_to_button")
        self.app_t_switch_to_button.setGeometry(QRect(280, 450, 111, 24))
        self.app_t_end_task_button = QPushButton(self.applications_tab)
        self.app_t_end_task_button.setObjectName(u"app_t_end_task_button")
        self.app_t_end_task_button.setGeometry(QRect(160, 450, 111, 24))
        self.task_manager_tab_widget.addTab(self.applications_tab, "")
        self.processes_tab = QWidget()
        self.processes_tab.setObjectName(u"processes_tab")
        self.proc_t_proc_list_table = QTableWidget(self.processes_tab)
        if (self.proc_t_proc_list_table.columnCount() < 7):
            self.proc_t_proc_list_table.setColumnCount(7)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(5, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.proc_t_proc_list_table.setHorizontalHeaderItem(6, __qtablewidgetitem8)

        self.proc_t_proc_list_table.setObjectName(u"proc_t_proc_list_table")
        self.proc_t_proc_list_table.setGeometry(QRect(0, 0, 510, 441))
        self.proc_t_end_process_button = QPushButton(self.processes_tab)
        self.proc_t_end_process_button.setObjectName(u"proc_t_end_process_button")
        self.proc_t_end_process_button.setGeometry(QRect(400, 450, 111, 24))
        self.task_manager_tab_widget.addTab(self.processes_tab, "")
        self.services_tab = QWidget()
        self.services_tab.setObjectName(u"services_tab")
        self.svc_t_services_list_table = QTableWidget(self.services_tab)
        if (self.svc_t_services_list_table.columnCount() < 4):
            self.svc_t_services_list_table.setColumnCount(4)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.svc_t_services_list_table.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.svc_t_services_list_table.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.svc_t_services_list_table.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.svc_t_services_list_table.setHorizontalHeaderItem(3, __qtablewidgetitem11)
        self.svc_t_services_list_table.setObjectName(u"svc_t_services_list_table")
        self.svc_t_services_list_table.setGeometry(QRect(0, 0, 510, 441))
        self.svc_t_services_button = QToolButton(self.services_tab)
        self.svc_t_services_button.setObjectName(u"svc_t_services_button")
        self.svc_t_services_button.setGeometry(QRect(390, 450, 120, 24))
        self.task_manager_tab_widget.addTab(self.services_tab, "")
        self.performance_tab = QWidget()
        self.performance_tab.setObjectName(u"performance_tab")
        self.verticalLayout_3 = QVBoxLayout(self.performance_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.perf_widget = QWidget(self.performance_tab)
        self.perf_widget.setObjectName(u"perf_widget")
        self.perf_cpu_usage = QGroupBox(self.perf_widget)
        self.perf_cpu_usage.setObjectName(u"perf_cpu_usage")
        self.perf_cpu_usage.setGeometry(QRect(10, 10, 91, 140))
        self.perf_cpu_usage_history = QGroupBox(self.perf_widget)
        self.perf_cpu_usage_history.setObjectName(u"perf_cpu_usage_history")
        self.perf_cpu_usage_history.setGeometry(QRect(110, 10, 390, 140))
        #self.perf_cpu_usage_history_h_layout = QHBoxLayout(self.perf_cpu_usage_history)
        #self.perf_cpu_usage_history_h_layout.setObjectName(u"perf_cpu_usage_history_h_layout")
        self.perf_mem_usage_history = QGroupBox(self.perf_widget)
        self.perf_mem_usage_history.setObjectName(u"perf_mem_usage_history")
        self.perf_mem_usage_history.setGeometry(QRect(110, 150, 390, 140))
        self.perf_physical_mem = QGroupBox(self.perf_widget)
        self.perf_physical_mem.setObjectName(u"perf_physical_mem")
        self.perf_physical_mem.setGeometry(QRect(10, 300, 181, 101))
        self.perf_physical_mem_total_label = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_total_label.setObjectName(u"perf_physical_mem_total_label")
        self.perf_physical_mem_total_label.setGeometry(QRect(10, 20, 49, 17))
        self.perf_physical_mem_total_value = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_total_value.setObjectName(u"perf_physical_mem_total_value")
        self.perf_physical_mem_total_value.setGeometry(QRect(78, 20, 91, 20))
        self.perf_physical_mem_total_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_physical_mem_cached_label = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_cached_label.setObjectName(u"perf_physical_mem_cached_label")
        self.perf_physical_mem_cached_label.setGeometry(QRect(10, 40, 49, 17))
        self.perf_physical_mem_cached_value = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_cached_value.setObjectName(u"perf_physical_mem_cached_value")
        self.perf_physical_mem_cached_value.setGeometry(QRect(78, 40, 91, 20))
        self.perf_physical_mem_cached_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_physical_mem_available_value = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_available_value.setObjectName(u"perf_physical_mem_available_value")
        self.perf_physical_mem_available_value.setGeometry(QRect(78, 60, 91, 20))
        self.perf_physical_mem_available_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_physical_mem_available_label = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_available_label.setObjectName(u"perf_physical_mem_available_label")
        self.perf_physical_mem_available_label.setGeometry(QRect(10, 60, 49, 17))
        self.perf_physical_mem_free_value = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_free_value.setObjectName(u"perf_physical_mem_free_value")
        self.perf_physical_mem_free_value.setGeometry(QRect(78, 80, 91, 20))
        self.perf_physical_mem_free_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_physical_mem_free_label = QLabel(self.perf_physical_mem)
        self.perf_physical_mem_free_label.setObjectName(u"perf_physical_mem_free_label")
        self.perf_physical_mem_free_label.setGeometry(QRect(10, 80, 49, 17))
        self.perf_system = QGroupBox(self.perf_widget)
        self.perf_system.setObjectName(u"perf_system")
        self.perf_system.setGeometry(QRect(200, 300, 181, 121))
        self.perf_system_handles_value = QLabel(self.perf_system)
        self.perf_system_handles_value.setObjectName(u"perf_system_handles_value")
        self.perf_system_handles_value.setGeometry(QRect(78, 20, 91, 20))
        self.perf_system_handles_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_system_handles_label = QLabel(self.perf_system)
        self.perf_system_handles_label.setObjectName(u"perf_system_handles_label")
        self.perf_system_handles_label.setGeometry(QRect(10, 20, 49, 17))
        self.perf_system_threads_value = QLabel(self.perf_system)
        self.perf_system_threads_value.setObjectName(u"perf_system_threads_value")
        self.perf_system_threads_value.setGeometry(QRect(78, 40, 91, 20))
        self.perf_system_threads_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_system_threads_label = QLabel(self.perf_system)
        self.perf_system_threads_label.setObjectName(u"perf_system_threads_label")
        self.perf_system_threads_label.setGeometry(QRect(10, 40, 61, 17))
        self.perf_system_processes_value = QLabel(self.perf_system)
        self.perf_system_processes_value.setObjectName(u"perf_system_processes_value")
        self.perf_system_processes_value.setGeometry(QRect(78, 60, 91, 20))
        self.perf_system_processes_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_system_processes_label = QLabel(self.perf_system)
        self.perf_system_processes_label.setObjectName(u"perf_system_processes_label")
        self.perf_system_processes_label.setGeometry(QRect(10, 60, 61, 17))
        self.perf_system_up_time_value = QLabel(self.perf_system)
        self.perf_system_up_time_value.setObjectName(u"perf_system_up_time_value")
        self.perf_system_up_time_value.setGeometry(QRect(78, 80, 91, 20))
        self.perf_system_up_time_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_system_up_time_label = QLabel(self.perf_system)
        self.perf_system_up_time_label.setObjectName(u"perf_system_up_time_label")
        self.perf_system_up_time_label.setGeometry(QRect(10, 80, 49, 17))
        self.perf_system_commit_value = QLabel(self.perf_system)
        self.perf_system_commit_value.setObjectName(u"perf_system_commit_value")
        self.perf_system_commit_value.setGeometry(QRect(98, 100, 71, 17))
        self.perf_system_commit_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_system_commit_label = QLabel(self.perf_system)
        self.perf_system_commit_label.setObjectName(u"perf_system_commit_label")
        self.perf_system_commit_label.setGeometry(QRect(10, 100, 81, 17))
        self.perf_kernel_memory = QGroupBox(self.perf_widget)
        self.perf_kernel_memory.setObjectName(u"perf_kernel_memory")
        self.perf_kernel_memory.setGeometry(QRect(10, 400, 181, 61))
        self.perf_kernel_mem_paged_value = QLabel(self.perf_kernel_memory)
        self.perf_kernel_mem_paged_value.setObjectName(u"perf_kernel_mem_paged_value")
        self.perf_kernel_mem_paged_value.setGeometry(QRect(78, 20, 91, 20))
        self.perf_kernel_mem_paged_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_kernel_mem_paged_label = QLabel(self.perf_kernel_memory)
        self.perf_kernel_mem_paged_label.setObjectName(u"perf_kernel_mem_paged_label")
        self.perf_kernel_mem_paged_label.setGeometry(QRect(10, 20, 49, 17))
        self.perf_kernel_mem_non_paged_value = QLabel(self.perf_kernel_memory)
        self.perf_kernel_mem_non_paged_value.setObjectName(u"perf_kernel_mem_non_paged_value")
        self.perf_kernel_mem_non_paged_value.setGeometry(QRect(78, 40, 91, 20))
        self.perf_kernel_mem_non_paged_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.perf_kernel_mem_non_paged_label = QLabel(self.perf_kernel_memory)
        self.perf_kernel_mem_non_paged_label.setObjectName(u"perf_kernel_mem_non_paged_label")
        self.perf_kernel_mem_non_paged_label.setGeometry(QRect(10, 40, 61, 17))
        self.perf_mem_usage = QGroupBox(self.perf_widget)
        self.perf_mem_usage.setObjectName(u"perf_mem_usage")
        self.perf_mem_usage.setGeometry(QRect(10, 150, 91, 140))
        self.perf_resource_monitor_button = QToolButton(self.perf_widget)
        self.perf_resource_monitor_button.setObjectName(u"perf_resource_monitor_button")
        self.perf_resource_monitor_button.setGeometry(QRect(200, 430, 181, 24))

        self.perf_resource_monitor_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.perf_resource_monitor_button_icon = QPixmap(":/icons/windows_uac.png")
        self.perf_resource_monitor_button.setIcon(QIcon(self.perf_resource_monitor_button_icon))


        self.svc_t_services_button_icon = QPixmap(":/icons/windows_uac.png")
        self.svc_t_services_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.svc_t_services_button.setIcon(QIcon(self.svc_t_services_button_icon))


        self.verticalLayout_3.addWidget(self.perf_widget)

        self.task_manager_tab_widget.addTab(self.performance_tab, "")
        self.networking_tab = QWidget()
        self.networking_tab.setObjectName(u"networking_tab")
        self.net_t_network_list_table = QTableWidget(self.networking_tab)
        if (self.net_t_network_list_table.columnCount() < 4):
            self.net_t_network_list_table.setColumnCount(4)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.net_t_network_list_table.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.net_t_network_list_table.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.net_t_network_list_table.setHorizontalHeaderItem(2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.net_t_network_list_table.setHorizontalHeaderItem(3, __qtablewidgetitem15)
        self.net_t_network_list_table.setObjectName(u"net_t_network_list_table")
        self.net_t_network_list_table.setGeometry(QRect(0, 350, 510, 121))
        self.verticalLayoutWidget = QWidget(self.networking_tab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 511, 341))
        self.net_t_vbox_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.net_t_vbox_layout.setObjectName(u"net_t_vbox_layout")
        self.net_t_vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.task_manager_tab_widget.addTab(self.networking_tab, "")
        self.users_tab = QWidget()
        self.users_tab.setObjectName(u"users_tab")
        self.users_t_users_list_table = QTableWidget(self.users_tab)
        if (self.users_t_users_list_table.columnCount() < 5):
            self.users_t_users_list_table.setColumnCount(5)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.users_t_users_list_table.setHorizontalHeaderItem(0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.users_t_users_list_table.setHorizontalHeaderItem(1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.users_t_users_list_table.setHorizontalHeaderItem(2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.users_t_users_list_table.setHorizontalHeaderItem(3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.users_t_users_list_table.setHorizontalHeaderItem(4, __qtablewidgetitem20)
        self.users_t_users_list_table.setObjectName(u"users_t_users_list_table")
        self.users_t_users_list_table.setGeometry(QRect(0, 0, 510, 441))
        self.users_t_send_message_button = QPushButton(self.users_tab)
        self.users_t_send_message_button.setObjectName(u"users_t_send_message_button")
        self.users_t_send_message_button.setGeometry(QRect(400, 450, 111, 24))
        self.users_t_logoff_button = QPushButton(self.users_tab)
        self.users_t_logoff_button.setObjectName(u"users_t_logoff_button")
        self.users_t_logoff_button.setGeometry(QRect(280, 450, 111, 24))
        self.users_t_disconnect_button = QPushButton(self.users_tab)
        self.users_t_disconnect_button.setObjectName(u"users_t_disconnect_button")
        self.users_t_disconnect_button.setGeometry(QRect(160, 450, 111, 24))
        self.task_manager_tab_widget.addTab(self.users_tab, "")

        self.verticalLayout_2.addWidget(self.task_manager_tab_widget)

        CWTM_TaskManagerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CWTM_TaskManagerMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 530, 22))
        CWTM_TaskManagerMainWindow.setMenuBar(self.menubar)

        self.task_manager_file_menu = QMenu(self.menubar)
        self.task_manager_file_menu.setObjectName(u"task_manager_file_menu")
        self.task_manager_options_menu = QMenu(self.menubar)
        self.task_manager_options_menu.setObjectName(u"task_manager_options_menu")
        self.task_manager_view_menu = QMenu(self.menubar)
        self.task_manager_view_menu.setObjectName(u"task_manager_view_menu")
        self.tm_view_menu_menu_update_speed = QMenu(self.task_manager_view_menu)
        self.tm_view_menu_menu_update_speed_group = QActionGroup(self.tm_view_menu_menu_update_speed)
        self.tm_view_menu_menu_update_speed.setObjectName(u"tm_view_menu_menu_update_speed")
        self.tm_view_menu_menu_cpu_history = QMenu(self.task_manager_view_menu)
        self.tm_view_menu_menu_cpu_history.setObjectName(u"tm_view_menu_menu_cpu_history")
        self.tm_view_menu_network_adapter_history = QMenu(self.task_manager_view_menu)
        self.tm_view_menu_network_adapter_history.setObjectName(u"tm_view_menu_network_adapter_history")
        self.task_manager_windows_menu = QMenu(self.menubar)
        self.task_manager_windows_menu.setObjectName(u"task_manager_windows_menu")
        self.task_manager_help_menu = QMenu(self.menubar)
        self.task_manager_help_menu.setObjectName(u"task_manager_help_menu")

        self.tm_file_menu_new_task_run = QAction(CWTM_TaskManagerMainWindow)
        self.tm_file_menu_new_task_run.setObjectName(u"tm_file_menu_new_task_run")
        self.tm_file_menu_exit_task_manager = QAction(CWTM_TaskManagerMainWindow)
        self.tm_file_menu_exit_task_manager.setObjectName(u"tm_file_menu_exit_task_manager")
        self.tm_options_menu_always_on_top = QAction(CWTM_TaskManagerMainWindow)
        self.tm_options_menu_always_on_top.setObjectName(u"tm_options_menu_always_on_top")
        self.tm_options_menu_always_on_top.setCheckable(True)
        self.tm_options_menu_always_on_top.triggered.connect(self.set_window_always_on_top)

        self.tm_options_menu_minimize_on_use = QAction(CWTM_TaskManagerMainWindow)
        self.tm_options_menu_minimize_on_use.setObjectName(u"tm_options_menu_minimize_on_use")
        self.tm_options_menu_minimize_on_use.setCheckable(True)
        self.tm_options_menu_hide_when_minimized = QAction(CWTM_TaskManagerMainWindow)
        self.tm_options_menu_hide_when_minimized.setObjectName(u"tm_options_menu_hide_when_minimized")
        self.tm_options_menu_hide_when_minimized.setCheckable(True)
        self.tm_view_menu_refresh_now = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_refresh_now.setObjectName(u"tm_view_menu_refresh_now")
        self.tm_view_menu_us_menu_high = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_us_menu_high.setObjectName(u"tm_view_menu_us_menu_high")
        self.tm_view_menu_us_menu_high.setCheckable(True)
        self.tm_view_menu_us_menu_normal = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_us_menu_normal.setObjectName(u"tm_view_menu_us_menu_normal")
        self.tm_view_menu_us_menu_normal.setCheckable(True)
        self.tm_view_menu_us_menu_normal.setChecked(True)
        self.tm_view_menu_us_menu_low = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_us_menu_low.setObjectName(u"tm_view_menu_us_menu_low")
        self.tm_view_menu_us_menu_low.setCheckable(True)
        self.tm_view_menu_us_menu_paused = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_us_menu_paused.setObjectName(u"tm_view_menu_us_menu_paused")
        self.tm_view_menu_us_menu_paused.setCheckable(True)
        self.tm_view_menu_select_columns = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_select_columns.setObjectName(u"tm_view_menu_select_columns")
        self.tm_windows_menu_tile_horizontally = QAction(CWTM_TaskManagerMainWindow)
        self.tm_windows_menu_tile_horizontally.setObjectName(u"tm_windows_menu_tile_horizontally")
        self.tm_windows_menu_tile_vertically = QAction(CWTM_TaskManagerMainWindow)
        self.tm_windows_menu_tile_vertically.setObjectName(u"tm_windows_menu_tile_vertically")
        self.tm_windows_menu_maximize = QAction(CWTM_TaskManagerMainWindow)
        self.tm_windows_menu_maximize.setObjectName(u"tm_windows_menu_maximize")
        self.tm_windows_menu_minimize = QAction(CWTM_TaskManagerMainWindow)
        self.tm_windows_menu_minimize.setObjectName(u"tm_windows_menu_minimize")
        self.tm_windows_menu_cascade = QAction(CWTM_TaskManagerMainWindow)
        self.tm_windows_menu_cascade.setObjectName(u"tm_windows_menu_cascade")
        self.tm_windows_menu_bring_to_front = QAction(CWTM_TaskManagerMainWindow)
        self.tm_windows_menu_bring_to_front.setObjectName(u"tm_windows_menu_bring_to_front")
        self.tm_help_menu_task_manager_help_topics = QAction(CWTM_TaskManagerMainWindow)
        self.tm_help_menu_task_manager_help_topics.setObjectName(u"tm_help_menu_task_manager_help_topics")
        self.tm_help_menu_about_task_manager = QAction(CWTM_TaskManagerMainWindow)
        self.tm_help_menu_about_task_manager.setObjectName(u"tm_help_menu_about_task_manager")
        self.tm_view_menu_show_kernel_times = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_show_kernel_times.setObjectName(u"tm_view_menu_show_kernel_times")
        self.tm_view_menu_cpu_one_graph_all_cpus = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_cpu_one_graph_all_cpus.setObjectName(u"tm_view_menu_cpu_one_graph_all_cpus")
        self.tm_view_menu_cpu_one_graph_per_cpu = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_cpu_one_graph_per_cpu.setObjectName(u"tm_view_menu_cpu_one_graph_per_cpu")
        self.tm_view_menu_nas_bytes_sent = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_nas_bytes_sent.setObjectName(u"tm_view_menu_nas_bytes_sent")
        self.tm_view_menu_nas_bytes_sent.setCheckable(True)
        self.tm_view_menu_nas_bytes_sent.setChecked(True)
        self.tm_view_menu_nas_bytes_received = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_nas_bytes_received.setObjectName(u"tm_view_menu_nas_bytes_received")
        self.tm_view_menu_nas_bytes_received.setCheckable(True)
        self.tm_view_menu_nas_bytes_received.setChecked(True)
        self.tm_view_menu_nas_bytes_total = QAction(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_nas_bytes_total.setObjectName(u"tm_view_menu_nas_bytes_total")
        self.tm_view_menu_nas_bytes_total.setCheckable(True)
        self.actionAuto_Scale = QAction(CWTM_TaskManagerMainWindow)
        self.actionAuto_Scale.setObjectName(u"actionAuto_Scale")
        self.actionAuto_Scale.setCheckable(True)
        self.tm_options_menu_show_full_account_name = QAction(CWTM_TaskManagerMainWindow)
        self.tm_options_menu_show_full_account_name.setObjectName(u"tm_options_menu_show_full_account_name")
        self.tm_options_menu_show_full_account_name.setCheckable(True)
        self.tm_options_menu_show_scale = QAction(CWTM_TaskManagerMainWindow)
        self.tm_options_menu_show_scale.setObjectName(u"tm_options_menu_show_scale")
        self.tm_options_menu_show_scale.setCheckable(True)
        self.tm_options_menu_show_scale.setChecked(True)

        self.statusbar = QStatusBar(CWTM_TaskManagerMainWindow)
        self.statusbar.setObjectName(u"statusbar")

        self.status_bar_processes_label = QLabel("Processes: 0")
        self.status_bar_cpu_usage_label = QLabel("CPU Usage: 0%")
        self.status_bar_physical_memory_label = QLabel("Physical Memory: 0%")

        self.statusbar.addWidget(self.status_bar_processes_label)
        self.statusbar.addWidget(VLine())
        self.statusbar.addWidget(self.status_bar_cpu_usage_label)
        self.statusbar.addWidget(VLine())
        self.statusbar.addWidget(self.status_bar_physical_memory_label)
        
        CWTM_TaskManagerMainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.task_manager_file_menu.menuAction())
        self.menubar.addAction(self.task_manager_options_menu.menuAction())
        self.menubar.addAction(self.task_manager_view_menu.menuAction())
        self.menubar.addAction(self.task_manager_windows_menu.menuAction())
        self.menubar.addAction(self.task_manager_help_menu.menuAction())
        self.task_manager_file_menu.addSeparator()
        self.task_manager_file_menu.addAction(self.tm_file_menu_new_task_run)
        self.task_manager_file_menu.addSeparator()
        self.task_manager_file_menu.addAction(self.tm_file_menu_exit_task_manager)
        self.task_manager_options_menu.addAction(self.tm_options_menu_always_on_top)
        self.task_manager_options_menu.addAction(self.tm_options_menu_minimize_on_use)
        self.task_manager_options_menu.addAction(self.tm_options_menu_hide_when_minimized)
        self.task_manager_options_menu.addSeparator()
        self.task_manager_options_menu.addAction(self.tm_options_menu_show_scale)
        self.task_manager_options_menu.addAction(self.tm_options_menu_show_full_account_name)
        self.task_manager_view_menu.addAction(self.tm_view_menu_refresh_now)
        self.task_manager_view_menu.addAction(self.tm_view_menu_menu_update_speed.menuAction())
        self.task_manager_view_menu.addSeparator()
        self.task_manager_view_menu.addAction(self.tm_view_menu_network_adapter_history.menuAction())
        self.task_manager_view_menu.addSeparator()
        self.task_manager_view_menu.addAction(self.tm_view_menu_select_columns)
        self.task_manager_view_menu.addAction(self.tm_view_menu_menu_cpu_history.menuAction())
        self.task_manager_view_menu.addAction(self.tm_view_menu_show_kernel_times)
        self.tm_view_menu_menu_update_speed.addAction(self.tm_view_menu_us_menu_high)
        self.tm_view_menu_menu_update_speed.addAction(self.tm_view_menu_us_menu_normal)
        self.tm_view_menu_menu_update_speed.addAction(self.tm_view_menu_us_menu_low)
        self.tm_view_menu_menu_update_speed.addAction(self.tm_view_menu_us_menu_paused)
        self.tm_view_menu_menu_update_speed_group.addAction(self.tm_view_menu_us_menu_high)
        self.tm_view_menu_menu_update_speed_group.addAction(self.tm_view_menu_us_menu_normal)
        self.tm_view_menu_menu_update_speed_group.addAction(self.tm_view_menu_us_menu_low)
        self.tm_view_menu_menu_update_speed_group.addAction(self.tm_view_menu_us_menu_paused)

        self.tm_view_menu_menu_cpu_history.addAction(self.tm_view_menu_cpu_one_graph_all_cpus)
        self.tm_view_menu_menu_cpu_history.addAction(self.tm_view_menu_cpu_one_graph_per_cpu)
        self.tm_view_menu_network_adapter_history.addAction(self.tm_view_menu_nas_bytes_sent)
        self.tm_view_menu_network_adapter_history.addAction(self.tm_view_menu_nas_bytes_received)
        self.tm_view_menu_network_adapter_history.addAction(self.tm_view_menu_nas_bytes_total)
        self.task_manager_windows_menu.addAction(self.tm_windows_menu_tile_horizontally)
        self.task_manager_windows_menu.addAction(self.tm_windows_menu_tile_vertically)
        self.task_manager_windows_menu.addAction(self.tm_windows_menu_maximize)
        self.task_manager_windows_menu.addAction(self.tm_windows_menu_minimize)
        self.task_manager_windows_menu.addAction(self.tm_windows_menu_cascade)
        self.task_manager_windows_menu.addAction(self.tm_windows_menu_bring_to_front)
        self.task_manager_help_menu.addAction(self.tm_help_menu_task_manager_help_topics)
        self.task_manager_help_menu.addSeparator()
        self.task_manager_help_menu.addAction(self.tm_help_menu_about_task_manager)

        self.retranslateUi(CWTM_TaskManagerMainWindow)
        self.tm_view_menu_menu_update_speed_group.setExclusive(True)

        self.task_manager_tab_widget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(CWTM_TaskManagerMainWindow)
    # setupUi

    def retranslateUi(self, CWTM_TaskManagerMainWindow):
        CWTM_TaskManagerMainWindow.setWindowTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Classic Windows Task Manager", None))
        CWTM_TaskManagerMainWindow.setWindowIcon(QIcon(":/icons/windows_taskmgr.png"))

        self.tm_file_menu_new_task_run.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"New Task (Run...)", None))
        self.tm_file_menu_exit_task_manager.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Exit Task Manager", None))
        self.tm_options_menu_always_on_top.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Always On Top", None))
        self.tm_options_menu_minimize_on_use.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Minimize On Use", None))
        self.tm_options_menu_hide_when_minimized.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Hide When Minimized", None))
        self.tm_view_menu_refresh_now.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Refresh Now", None))
#if QT_CONFIG(shortcut)
        self.tm_view_menu_refresh_now.setShortcut(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.tm_view_menu_us_menu_high.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"High", None))
        self.tm_view_menu_us_menu_normal.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Normal", None))
        self.tm_view_menu_us_menu_low.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Low", None))
        self.tm_view_menu_us_menu_paused.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Paused", None))
        self.tm_view_menu_select_columns.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Select Columns...", None))
        self.tm_windows_menu_tile_horizontally.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Tile Horizontally", None))
        self.tm_windows_menu_tile_vertically.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Tile Vertically", None))
        self.tm_windows_menu_maximize.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Minimize", None))
        self.tm_windows_menu_minimize.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Maximize", None))
        self.tm_windows_menu_cascade.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Cascade", None))
        self.tm_windows_menu_bring_to_front.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Bring To Front", None))
        self.tm_help_menu_task_manager_help_topics.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Task Manager Help Topics", None))
        self.tm_help_menu_about_task_manager.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"About Task Manager", None))
        self.tm_view_menu_show_kernel_times.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Show Kernel Times", None))
        self.tm_view_menu_cpu_one_graph_all_cpus.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"One Graph, All CPUs", None))
        self.tm_view_menu_cpu_one_graph_per_cpu.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"One Graph, Per CPU", None))
        self.tm_view_menu_nas_bytes_sent.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Bytes Sent", None))
        self.tm_view_menu_nas_bytes_received.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Bytes Received", None))
        self.tm_view_menu_nas_bytes_total.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Bytes Total", None))
        self.actionAuto_Scale.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Auto Scale", None))
        self.tm_options_menu_show_full_account_name.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Show Full Account Name", None))
        self.tm_options_menu_show_scale.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Show Scale", None))

        ___qtablewidgetitem = self.app_t_task_list_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Task", None));
        ___qtablewidgetitem1 = self.app_t_task_list_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Status", None));
        ___qtablewidgetitem2 = self.app_t_task_list_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"PID", None));
        self.app_t_new_task_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"New Task...", None))
        self.app_t_switch_to_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Switch To", None))
        self.app_t_end_task_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"End Task", None))
        self.task_manager_tab_widget.setTabText(self.task_manager_tab_widget.indexOf(self.applications_tab), QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Applications", None))
        ___qtablewidgetitem2 = self.proc_t_proc_list_table.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Image Name", None));
        ___qtablewidgetitem3 = self.proc_t_proc_list_table.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"PID", None));
        ___qtablewidgetitem4 = self.proc_t_proc_list_table.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Username", None));
        ___qtablewidgetitem5 = self.proc_t_proc_list_table.horizontalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"CPU", None));
        ___qtablewidgetitem6 = self.proc_t_proc_list_table.horizontalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Memory (MB)", None));
        ___qtablewidgetitem7 = self.proc_t_proc_list_table.horizontalHeaderItem(5)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Description", None));
        ___qtablewidgetitem8 = self.proc_t_proc_list_table.horizontalHeaderItem(6)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Executable", None));
        self.proc_t_end_process_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"End Process", None))
        self.task_manager_tab_widget.setTabText(self.task_manager_tab_widget.indexOf(self.processes_tab), QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Processes", None))
        ___qtablewidgetitem8 = self.svc_t_services_list_table.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Name", None));
        ___qtablewidgetitem9 = self.svc_t_services_list_table.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"PID", None));
        ___qtablewidgetitem10 = self.svc_t_services_list_table.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Description", None));
        ___qtablewidgetitem11 = self.svc_t_services_list_table.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Status", None));
        self.svc_t_services_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Services", None))
        self.task_manager_tab_widget.setTabText(self.task_manager_tab_widget.indexOf(self.services_tab), QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Services", None))
        self.perf_cpu_usage.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"CPU Usage", None))
        self.perf_cpu_usage_history.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"CPU Usage History", None))
        self.perf_mem_usage_history.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Memory Usage History", None))
        self.perf_physical_mem.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Physical Memory (MB)", None))
        self.perf_physical_mem_total_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Total", None))
        self.perf_physical_mem_total_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_physical_mem_cached_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Cached", None))
        self.perf_physical_mem_cached_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_physical_mem_available_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_physical_mem_available_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Available", None))
        self.perf_physical_mem_free_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_physical_mem_free_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Free", None))
        self.perf_system.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"System", None))
        self.perf_system_handles_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_system_handles_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Handles", None))
        self.perf_system_threads_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_system_threads_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Threads", None))
        self.perf_system_processes_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_system_processes_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Processes", None))
        self.perf_system_up_time_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_system_up_time_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Up Time", None))
        self.perf_system_commit_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_system_commit_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Commit (MB)", None))
        self.perf_kernel_memory.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Kernel Memory (MB)", None))
        self.perf_kernel_mem_paged_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_kernel_mem_paged_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Paged", None))
        self.perf_kernel_mem_non_paged_value.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"0", None))
        self.perf_kernel_mem_non_paged_label.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Nonpaged", None))
        self.perf_mem_usage.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Memory", None))
        self.perf_resource_monitor_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Resource Monitor...", None))
        self.task_manager_tab_widget.setTabText(self.task_manager_tab_widget.indexOf(self.performance_tab), QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Performance", None))
        ___qtablewidgetitem12 = self.net_t_network_list_table.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Adapter Name", None));
        ___qtablewidgetitem13 = self.net_t_network_list_table.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Network Utilization", None));
        ___qtablewidgetitem14 = self.net_t_network_list_table.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Link Speed", None));
        ___qtablewidgetitem15 = self.net_t_network_list_table.horizontalHeaderItem(3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"State", None));
        self.task_manager_tab_widget.setTabText(self.task_manager_tab_widget.indexOf(self.networking_tab), QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Networking", None))
        ___qtablewidgetitem16 = self.users_t_users_list_table.horizontalHeaderItem(0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"User", None));
        ___qtablewidgetitem17 = self.users_t_users_list_table.horizontalHeaderItem(1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"ID", None));
        ___qtablewidgetitem18 = self.users_t_users_list_table.horizontalHeaderItem(2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Status", None));
        ___qtablewidgetitem19 = self.users_t_users_list_table.horizontalHeaderItem(3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Client Name", None));
        ___qtablewidgetitem20 = self.users_t_users_list_table.horizontalHeaderItem(4)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Session", None));
        self.users_t_send_message_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Send Message...", None))
        self.users_t_logoff_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Logoff", None))
        self.users_t_disconnect_button.setText(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Disconnect", None))
        self.task_manager_tab_widget.setTabText(self.task_manager_tab_widget.indexOf(self.users_tab), QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Users", None))
    
        self.task_manager_file_menu.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"File", None))
        self.task_manager_options_menu.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Options", None))
        self.task_manager_view_menu.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"View", None))
        self.tm_view_menu_menu_update_speed.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Update Speed", None))
        self.tm_view_menu_menu_cpu_history.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"CPU History", None))
        self.tm_view_menu_network_adapter_history.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Network Adapter History", None))
        self.task_manager_windows_menu.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Windows", None))
        self.task_manager_help_menu.setTitle(QCoreApplication.translate("CWTM_TaskManagerMainWindow", u"Help", None))
    # retranslateUi

    @pyqtSlot(bool)
    def set_window_always_on_top(self, checked):
        flags = self.windowFlags()
        
        if checked:
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint
        
        self.setWindowFlags(flags)
        self.show()


class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(self.VLine|self.Sunken)