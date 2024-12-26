# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_new_taskkzxATM.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore

from resources import resources


class Ui_CWTM_TaskManagerNewTaskDialog(QDialog):
    def setupUi(self, CWTM_TaskManagerNewTaskDialog):
        if not CWTM_TaskManagerNewTaskDialog.objectName():
            CWTM_TaskManagerNewTaskDialog.setObjectName(u"CWTM_TaskManagerNewTaskDialog")
        CWTM_TaskManagerNewTaskDialog.resize(415, 200)
        CWTM_TaskManagerNewTaskDialog.setMinimumSize(QSize(415, 200))
        CWTM_TaskManagerNewTaskDialog.setMaximumSize(QSize(415, 200))
        self.button_group_widget = QWidget(CWTM_TaskManagerNewTaskDialog)
        self.button_group_widget.setObjectName(u"button_group_widget")
        self.button_group_widget.setGeometry(QRect(-10, 140, 481, 81))

        with open ("./cwtm_taskmgr_ui/cwtm_button_group_widget.qss", "r") as btn_grp_wdgt:   
            self.button_group_widget.setStyleSheet(btn_grp_wdgt.read())

        self.browse_button = QPushButton(self.button_group_widget)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.setGeometry(QRect(320, 20, 81, 24))
        self.cancel_button = QPushButton(self.button_group_widget)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(230, 20, 80, 24))
        self.ok_button = QPushButton(self.button_group_widget)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setGeometry(QRect(140, 20, 80, 24))
        self.open_label = QLabel(CWTM_TaskManagerNewTaskDialog)
        self.open_label.setObjectName(u"open_label")
        self.open_label.setGeometry(QRect(20, 90, 49, 17))
        self.new_task_input_line_edit = QLineEdit(CWTM_TaskManagerNewTaskDialog)
        self.new_task_input_line_edit.setObjectName(u"new_task_input_line_edit")
        self.new_task_input_line_edit.setGeometry(QRect(60, 90, 341, 26))
        self.new_task_information_label = QLabel(CWTM_TaskManagerNewTaskDialog)
        self.new_task_information_label.setObjectName(u"new_task_information_label")
        self.new_task_information_label.setGeometry(QRect(60, 30, 331, 41))
        self.new_task_information_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.new_task_information_label.setWordWrap(True)
        self.main_application_icon = QLabel(CWTM_TaskManagerNewTaskDialog)
        self.main_application_icon.setObjectName(u"main_application_icon")
        self.main_application_icon.setGeometry(QRect(10, 30, 41, 41))
        self.main_application_icon.setPixmap(QPixmap(u":/icons/windows_taskmgr.png"))
        self.main_application_icon.setScaledContents(True)

        self.retranslateUi(CWTM_TaskManagerNewTaskDialog)

        QMetaObject.connectSlotsByName(CWTM_TaskManagerNewTaskDialog)
    # setupUi

    def retranslateUi(self, CWTM_TaskManagerNewTaskDialog):
        CWTM_TaskManagerNewTaskDialog.setWindowTitle(QCoreApplication.translate("CWTM_TaskManagerNewTaskDialog", u"Create New Task", None))
        CWTM_TaskManagerNewTaskDialog.setWindowIcon(QIcon(":/icons/windows_run.png"))
        self.browse_button.setText(QCoreApplication.translate("CWTM_TaskManagerNewTaskDialog", u"Browse...", None))
        self.cancel_button.setText(QCoreApplication.translate("CWTM_TaskManagerNewTaskDialog", u"Cancel", None))
        self.ok_button.setText(QCoreApplication.translate("CWTM_TaskManagerNewTaskDialog", u"OK", None))
        self.open_label.setText(QCoreApplication.translate("CWTM_TaskManagerNewTaskDialog", u"Open:", None))
        self.new_task_information_label.setText(QCoreApplication.translate("CWTM_TaskManagerNewTaskDialog", u"Type the name of a program, folder, document, or Internet resource, and Windows will open it for you.", None))
        self.main_application_icon.setText("")
    # retranslateUi

