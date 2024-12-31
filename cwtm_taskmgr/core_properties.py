import enum
import psutil
import dataclasses

from . import sys_utils

from PyQt5.QtWidgets import QTableWidgetItem, QGroupBox
from PyQt5.QtGui import QColor

from pyqtgraph.graphicsItems import PlotDataItem
from pyqtgraph import PlotWidget


@dataclasses.dataclass
class CWTM_ResourceLevelBarParameters:
    x_offset:               int
    y_offset:               int
    total_bars:             int
    bar_height:             int
    bar_width:              int
    spacing:                int
    resource_bar_label:     str
    
    offset_factor:          int                     = 6


@dataclasses.dataclass
class CWTM_NetworkInterfaceUsageFrame:
    i_net_name:             str
    i_net_bytes_sent:       float
    i_net_bytes_received:   float

@dataclasses.dataclass
class CWTM_NetworkInterfaceGraphProperties:
    i_net_graph:            PlotWidget
    i_net_groupbox:         QGroupBox
    i_net_sent_data_x:      list
    i_net_sent_data_y:      list
    i_net_recv_data_x:      list
    i_net_recv_data_y:      list
    i_net_total_data_x:     list
    i_net_total_data_y:     list
    i_net_sent_plot_item:   PlotDataItem.PlotDataItem
    i_net_recv_plot_item:   PlotDataItem.PlotDataItem
    i_net_total_plot_item:  PlotDataItem.PlotDataItem
    i_net_full_name:        str                     = ""


@dataclasses.dataclass
class CWTM_ProcessInformationFrame:
    p_name:                 str
    p_pid:                  int
    p_username:             str
    p_cpu_usage:            float
    p_memory_usage:         psutil._pslinux.pmem
    p_description:          list[str] | None
    p_exe:                  str


@dataclasses.dataclass
class CWTM_ApplicationInformationFrame:
    gtk_app_name:           str | None
    gtk_app_pid:            sys_utils.Gtk.Image
    gtk_app_icon:           int


@dataclasses.dataclass
class CWTM_PerformanceStatusBarLabelsFrame:
    n_processes:            int
    v_mem_percent:          float
    cpu_usage:              float


@dataclasses.dataclass
class CWTM_PerformanceGraphCPUUsageFrame:
    user_cpu_usage:         list[int]
    kernel_cpu_usage:       list[int]


@dataclasses.dataclass
class CWTM_PerformanceSystemMemoryLabelsFrame:
    n_file_descriptors:     int
    n_sys_threads:          int
    n_sys_processes:        int
    total_sys_uptime:       str
    total_sys_mem_commit:   str


@dataclasses.dataclass
class CWTM_PerformanceGraphicalWidgetsFrame:
    current_cpu_usage:      float
    kernel_cpu_time:        float
    current_memory_usage:   float
    memory_used:            float
    memory_total:           float


@dataclasses.dataclass
class CWTM_ServiceInformationFrame:
    svc_name:               str
    svc_pid:                int
    svc_desc:               str
    svc_status:             str


@dataclasses.dataclass
class CWTM_UsersSystemInformationFrame:
    u_user_name:            str
    u_user_uid:             int
    u_is_logged_in:         bool
    u_real_name:            str
    u_home_dir:             str


@dataclasses.dataclass
class CWTM_TableWidgetItemProperties:
    item_label:             str
    item_type:              QTableWidgetItem        = QTableWidgetItem
    item_icon:              sys_utils.Gtk.Image     = None
    item_tool_tip:          str                     = None
    item_unit:              str                     = ""


class CWTM_TabWidgetColumnEnum(enum.IntEnum):
    TASK_MANAGER_APPLICATIONS_TAB                   = 0
    TASK_MANAGER_PROCESSES_TAB                      = enum.auto()
    TASK_MANAGER_SERVICES_TAB                       = enum.auto()
    TASK_MANAGER_PERFORMANCE_TAB                    = enum.auto()
    TASK_MANAGER_NETWORKING_TAB                     = enum.auto()
    TASK_MANAGER_USERS_TAB                          = enum.auto()


class CWTM_ApplicationsTabTableColumns(enum.IntEnum):
    APP_T_TASK_LIST_TABLE_TASK                      = 0
    APP_T_TASK_LIST_TABLE_STATUS                    = enum.auto()
    APP_T_TASK_LIST_TABLE_PID                       = enum.auto() # hidden


class CWTM_ProcessesTabTableColumns(enum.IntEnum):
    PROC_T_PROC_LIST_TABLE_IMAGE_NAME               = 0
    PROC_T_PROC_LIST_TABLE_PID                      = enum.auto()
    PROC_T_PROC_LIST_TABLE_USERNAME                 = enum.auto()
    PROC_T_PROC_LIST_TABLE_CPU                      = enum.auto()
    PROC_T_PROC_LIST_TABLE_MEMORY                   = enum.auto()
    PROC_T_PROC_LIST_TABLE_DESCRIPTION              = enum.auto()
    PROC_T_PROC_LIST_TABLE_EXECUTABLE               = enum.auto() # hidden


class CWTM_ServicesTabTableColumns(enum.IntEnum):
    SVC_T_SERVICES_LIST_TABLE_NAME                  = 0
    SVC_T_SERVICES_LIST_TABLE_PID                   = enum.auto()
    SVC_T_SERVICES_LIST_TABLE_DESCRIPTION           = enum.auto()
    SVC_T_SERVICES_LIST_TABLE_STATUS                = enum.auto()


class CWTM_NetworkingTabTableColumns(enum.IntEnum):
    NET_T_NETWORKING_LIST_TABLE_ADAPTER_NAME        = 0
    NET_T_NETWORKING_LIST_TABLE_NETWORK_UTILIZATION = enum.auto()
    NET_T_NETWORKING_LIST_TABLE_LINK_SPEED          = enum.auto()
    NET_T_NETWORKING_LIST_TABLE_STATE               = enum.auto()


class CWTM_UsersTabTableColumns(enum.IntEnum):
    USERS_T_USERS_LIST_TABLE_USER                   = 0
    USERS_T_USERS_LIST_TABLE_ID                     = enum.auto()
    USERS_T_USERS_LIST_TABLE_STATUS                 = enum.auto()
    USERS_T_USERS_LIST_TABLE_CLIENT_NAME            = enum.auto()
    USERS_T_USERS_LIST_TABLE_SESSION                = enum.auto()


class CWTM_MenuBarStatusBarLabels(enum.StrEnum):
    LABEL_NEW_TASK                  = "Runs a new program"
    LABEL_EXIT_TASK_MANAGER         = "Exits Task Manager"
    LABEL_ALWAYS_ON_TOP             = "Task Manager remains in front of all other windows unless minimized"
    LABEL_MINIMIZE_ON_USE           = "Task Manager is minimzed when a SwitchTo operation is performed"
    LABEL_HIDE_WHEN_MINIMIZED       = "Hide Task Manager when it is minimized"
    LABEL_SHOW_FULL_ACCOUNT_NAME    = "Shows the domain to which each user account belongs"
    LABEL_REFRESH_NOW               = "Force Task Manager to update now, regardless of Update Speed setting"
    LABEL_UPDATE_SPEED              = "Force Task Manager to update now, regardless of Update Speed setting"
    LABEL_HIGH                      = "Updates the display twice per second"
    LABEL_NORMAL                    = "Updates the display every one second"
    LABEL_LOW                       = "Updates the display every four seconds"
    LABEL_PAUSED                    = "Display does not automatically update"
    LABEL_HELP_TOPICS               = "Displays Task Manager help topics"
    LABEL_ABOUT_TASK_MANAGER        = "Displays program information, version number, and copyright"
    LABEL_NETWORK_ADAPTER_HISTORY   = "Force Task Manager to update now, regardless of Update Speed setting"
    LABEL_BYTES_SENT                = "Graph bytes sent (red)"
    LABEL_BYTES_RECEIVED            = "Graph bytes received (yellow)"
    LABEL_BYTES_TOTAL               = "Graph the sum of bytes sent and received (green)"
    LABEL_SELECT_COLUMNS            = "Select which columns will be visible on the Networking page"
    LABEL_SHOW_SCALE                = "Show the scale"
    LABEL_CPU_HISTORY               = "Force Task Manager to update now, regardless of Update Speed setting"
    LABEL_SHOW_KERNEL_TIMES         = "Displays kernel time in the performance graphs"
    LABEL_ONE_GRAPH_ALL_CPUS        = "A single history graph shows total CPU usage"
    LABEL_ONE_GRAPH_PER_CPU         = "Each CPU has its own history graph"


class CWTM_MenuBarDynamicMenuFlags(enum.IntFlag):
    SELECT_COLUMNS                                  = enum.auto()
    SHOW_FULL_ACCOUNT_NAME                          = enum.auto()
    CPU_HISTORY                                     = enum.auto()
    SHOW_KERNEL_TIMES                               = enum.auto()
    NETWORK_ADAPTER_HISTORY                         = enum.auto()
    SHOW_SCALE                                      = enum.auto()
    UPDATE_SPEED                                    = enum.auto()


class CWTM_GlobalUpdateIntervals(enum.IntEnum):
    GLOBAL_UPDATE_INTERVAL_HIGH                     = 500 # half second
    GLOBAL_UPDATE_INTERVAL_NORMAL                   = 1000 # second
    GLOBAL_UPDATE_INTERVAL_LOW                      = 4000 # 4 seconds
    GLOBAL_UPDATE_INTERVAL_PAUSED                   = -1
    

class CWTM_ResourceBarLevelColours:
    BAR_COLOUR_CPU_USAGE_TIME_FILLED                = QColor(0, 255, 0) # green
    BAR_COLOUR_CPU_USAGE_TIME_EMPTY                 = QColor(0, 100, 0) # dark green
    BAR_COLOUR_KERNEL_USAGE_TIME_FILLED             = QColor(255, 0, 0) # red


class CWTM_NetworkingBytesLabelsColours:
    BYTES_LABEL_BYTES_SENT                          = QColor(255, 0, 0) # red
    BYTES_LABEL_BYTES_RECEIVED                      = QColor(255, 255, 0) # yellow
    BYTES_LABEL_BYTES_TOTAL                         = QColor(0, 255, 0) # green


CWTM_MENU_BAR_DYNAMIC_MENU_VISIBILITY_MAPPING = {
    CWTM_TabWidgetColumnEnum.TASK_MANAGER_NETWORKING_TAB: (
        CWTM_MenuBarDynamicMenuFlags.SELECT_COLUMNS |
        CWTM_MenuBarDynamicMenuFlags.NETWORK_ADAPTER_HISTORY |
        CWTM_MenuBarDynamicMenuFlags.SHOW_SCALE |
        CWTM_MenuBarDynamicMenuFlags.UPDATE_SPEED
    ),
    CWTM_TabWidgetColumnEnum.TASK_MANAGER_PERFORMANCE_TAB: (
        CWTM_MenuBarDynamicMenuFlags.CPU_HISTORY |
        CWTM_MenuBarDynamicMenuFlags.SHOW_KERNEL_TIMES |
        CWTM_MenuBarDynamicMenuFlags.UPDATE_SPEED
    ),
    CWTM_TabWidgetColumnEnum.TASK_MANAGER_USERS_TAB: (
        CWTM_MenuBarDynamicMenuFlags.SELECT_COLUMNS |
        CWTM_MenuBarDynamicMenuFlags.SHOW_FULL_ACCOUNT_NAME |
        CWTM_MenuBarDynamicMenuFlags.UPDATE_SPEED
    ),
    CWTM_TabWidgetColumnEnum.TASK_MANAGER_APPLICATIONS_TAB: (
        CWTM_MenuBarDynamicMenuFlags.UPDATE_SPEED
    ),
    CWTM_TabWidgetColumnEnum.TASK_MANAGER_PROCESSES_TAB: (
        CWTM_MenuBarDynamicMenuFlags.SELECT_COLUMNS |
        CWTM_MenuBarDynamicMenuFlags.UPDATE_SPEED
    ),
    CWTM_TabWidgetColumnEnum.TASK_MANAGER_SERVICES_TAB: 0 # Nothing
}