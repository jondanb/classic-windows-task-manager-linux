import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QVBoxLayout,
    QGroupBox, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont, QFontDatabase

from cwtm_taskmgr_ui.cwtm_taskmgr_ui import Ui_CWTM_TaskManagerMainWindow
from cwtm_taskmgr.qt_components import CWTM_MenuBarSignalHandler

from cwtm_taskmgr.tm_tabbar import (
    tm_applications_tab,
    tm_processes_tab,
    tm_performance_tab,
    tm_services_tab,
    tm_users_tab,
    tm_networking_tab
)


class Win7TaskManager(Ui_CWTM_TaskManagerMainWindow):
    def __init__(self, *args, old_style=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.old_style = old_style

        self.applications_tab = tm_applications_tab.CWTM_ApplicationsTab(self)
        self.processes_tab = tm_processes_tab.CWTM_ProcessesTab(self)
        self.performance_tab = tm_performance_tab.CWTM_PerformanceTab(self)
        self.services_tab = tm_services_tab.CWTM_ServicesTab(self)
        self.users_tab = tm_users_tab.CWTM_UsersTab(self)
        self.networking_tab = tm_networking_tab.CWTM_NetworkingTab(self)
        
        self.menubar_handler = CWTM_MenuBarSignalHandler(self)

        # Applications Tab
        self.applications_tab.setup_tab_page_table_widget(
            self.app_t_task_list_table,
            self.applications_tab.APP_T_TASK_LIST_TABLE_COLUMN_RATIO
        )
        self.applications_tab.start_applications_page_updater_thread()

        # Processes Tab
        self.processes_tab.setup_tab_page_table_widget(
            self.proc_t_proc_list_table,
            self.processes_tab.PROC_T_PROC_LIST_COLUMN_RATIO
        )
        self.processes_tab.start_processes_page_updater_thread()

        # Performance Tab
        self.performance_tab.setup_performance_tab_bars()
        self.performance_tab.setup_performance_tab_graphs()
        self.performance_tab.setup_performance_tab_menu_bar_slots()
        self.performance_tab.start_performance_page_updater_thread()

        # Services Tab
        self.services_tab.setup_tab_page_table_widget(
            self.svc_t_services_list_table,
            self.services_tab.SVC_T_SERVICES_LIST_TABLE_COLUMN_RATIO
        )
        self.services_tab.start_services_page_updater_thread()

        # Users Tab
        self.users_tab.setup_tab_page_table_widget(
            self.users_t_users_list_table, None
        )
        self.users_tab.start_users_page_updater_thread()

        # Networking Tab
        self.networking_tab.setup_tab_page_table_widget(
            self.net_t_network_list_table,
            QHeaderView.Stretch
        )
        self.networking_tab.setup_system_networking_interfaces()
        self.networking_tab.start_networking_page_updater_thread()

        # Menu Bar
        self.menubar_handler.setup_menu_bar_status_bar_labels()
        self.menubar_handler.setup_menubar_tab_visibility()
        self.menubar_handler.setup_menubar_signal_slots()

        # Style
        application_font = self.set_application_style()
        QApplication.setFont(application_font)

    def set_application_style(self):
        application_font = QFont()
        application_font_db_id = QFontDatabase.addApplicationFont(
            "./app_font/segoeui.ttf" if not self.old_style else \
            "./app_font/ms-sans-serif-1.ttf"
        )
        application_font_family = QFontDatabase.applicationFontFamilies(
            application_font_db_id
        )[0]
        
        application_font.setFamily(application_font_family)
        application_font.setPointSize(9 if not self.old_style else 8)

        if self.old_style:
            QApplication.setStyle("Windows")

        return application_font

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Win7TaskManager(old_style=False)
    
    main.show()
    sys.exit(app.exec_())

