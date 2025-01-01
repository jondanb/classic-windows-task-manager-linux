# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_affinity_selectoroDgndG.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_CWTM_CPUAffinitySelectorDialog(QDialog):
    def setupUi(self, CWTM_CPUAffinitySelectorDialog):
        if not CWTM_CPUAffinitySelectorDialog.objectName():
            CWTM_CPUAffinitySelectorDialog.setObjectName(u"CWTM_CPUAffinitySelectorDialog")
        CWTM_CPUAffinitySelectorDialog.resize(350, 360)
        CWTM_CPUAffinitySelectorDialog.setMinimumSize(QSize(350, 360))
        CWTM_CPUAffinitySelectorDialog.setMaximumSize(QSize(350, 360))
        self.check_box_list_widget = QListWidget(CWTM_CPUAffinitySelectorDialog)
        __qlistwidgetitem = QListWidgetItem(self.check_box_list_widget)
        __qlistwidgetitem.setCheckState(Qt.Unchecked);
        __qlistwidgetitem.setFlags(Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.check_box_list_widget.setObjectName(u"check_box_list_widget")
        self.check_box_list_widget.setGeometry(QRect(10, 60, 331, 251))
        self.process_affinity_label = QLabel(CWTM_CPUAffinitySelectorDialog)
        self.process_affinity_label.setObjectName(u"process_affinity_label")
        self.process_affinity_label.setGeometry(QRect(10, 20, 321, 17))
        self.ok_button = QPushButton(CWTM_CPUAffinitySelectorDialog)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setGeometry(QRect(170, 320, 80, 24))
        self.cancel_button = QPushButton(CWTM_CPUAffinitySelectorDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(260, 320, 80, 24))

        self.retranslateUi(CWTM_CPUAffinitySelectorDialog)

        QMetaObject.connectSlotsByName(CWTM_CPUAffinitySelectorDialog)
    # setupUi

    def retranslateUi(self, CWTM_CPUAffinitySelectorDialog):
        CWTM_CPUAffinitySelectorDialog.setWindowTitle(QCoreApplication.translate("CWTM_CPUAffinitySelectorDialog", u"Dialog", None))

        __sortingEnabled = self.check_box_list_widget.isSortingEnabled()
        self.check_box_list_widget.setSortingEnabled(False)
        ___qlistwidgetitem = self.check_box_list_widget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("CWTM_CPUAffinitySelectorDialog", u"<All Processors>", None));
        ___qlistwidgetitem.setData(Qt.UserRole, "all_processors")
        self.check_box_list_widget.setSortingEnabled(__sortingEnabled)

        self.process_affinity_label.setText(QCoreApplication.translate("CWTM_CPUAffinitySelectorDialog", u"Which processors are allowed to run for \"PROCESS_NAME\"?", None))
        self.ok_button.setText(QCoreApplication.translate("CWTM_CPUAffinitySelectorDialog", u"OK", None))
        self.cancel_button.setText(QCoreApplication.translate("CWTM_CPUAffinitySelectorDialog", u"Cancel", None))
    # retranslateUi

