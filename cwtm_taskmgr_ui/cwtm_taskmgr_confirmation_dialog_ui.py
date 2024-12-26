# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_confirmationGEPZUl.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_CWTMTaskManagerConfirmationDialog(QDialog):
    def setupUi(self, CWTMTaskManagerConfirmationDialog):
        if not CWTMTaskManagerConfirmationDialog.objectName():
            CWTMTaskManagerConfirmationDialog.setObjectName(u"CWTMTaskManagerConfirmationDialog")
        CWTMTaskManagerConfirmationDialog.resize(365, 170)
        CWTMTaskManagerConfirmationDialog.setMinimumSize(QSize(365, 170))
        CWTMTaskManagerConfirmationDialog.setMaximumSize(QSize(365, 170))
        self.button_group_widget = QWidget(CWTMTaskManagerConfirmationDialog)
        self.button_group_widget.setObjectName(u"button_group_widget")
        self.button_group_widget.setGeometry(QRect(-20, 130, 391, 51))

        with open ("./cwtm_taskmgr_ui/cwtm_button_group_widget.qss", "r") as btn_grp_wdgt:   
            self.button_group_widget.setStyleSheet(btn_grp_wdgt.read())
        
        self.cancel_button = QPushButton(self.button_group_widget)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(300, 10, 71, 24))
        self.confirm_button = QPushButton(self.button_group_widget)
        self.confirm_button.setObjectName(u"confirm_button")
        self.confirm_button.setGeometry(QRect(210, 10, 80, 24))
        self.end_process_title_label = QLabel(CWTMTaskManagerConfirmationDialog)
        self.end_process_title_label.setObjectName(u"end_process_title_label")
        self.end_process_title_label.setGeometry(QRect(10, 20, 341, 20))
        font = QFont()
        font.setPointSize(13)
        self.end_process_title_label.setFont(font)
        self.end_process_title_label.setStyleSheet(u"QLabel {\n"
"	color: rgb(0, 65, 156);\n"
"}")
        self.end_proces_information_label = QLabel(CWTMTaskManagerConfirmationDialog)
        self.end_proces_information_label.setObjectName(u"end_proces_information_label")
        self.end_proces_information_label.setGeometry(QRect(10, 50, 341, 81))
        self.end_proces_information_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.end_proces_information_label.setWordWrap(True)

        self.retranslateUi(CWTMTaskManagerConfirmationDialog)

        QMetaObject.connectSlotsByName(CWTMTaskManagerConfirmationDialog)
    # setupUi

    def retranslateUi(self, CWTMTaskManagerConfirmationDialog):
        CWTMTaskManagerConfirmationDialog.setWindowTitle(QCoreApplication.translate("CWTMTaskManagerConfirmationDialog", u"Dialog", None))
        self.cancel_button.setText(QCoreApplication.translate("CWTMTaskManagerConfirmationDialog", u"Cancel", None))
        self.confirm_button.setText(QCoreApplication.translate("CWTMTaskManagerConfirmationDialog", u"End Process", None))
        self.end_process_title_label.setText(QCoreApplication.translate("CWTMTaskManagerConfirmationDialog", u"Do you want to end 'PROCESS NAME'?", None))
        self.end_proces_information_label.setText(QCoreApplication.translate("CWTMTaskManagerConfirmationDialog", u"If an open program is associated with this process, it will close and you will lose any unsaved data. If you end a system process, it might result in an unstable system. Are you sure you want to continue?", None))
    # retranslateUi

