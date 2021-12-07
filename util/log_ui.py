# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_log(object):
    def setupUi(self, log):
        if not log.objectName():
            log.setObjectName(u"log")
        log.resize(509, 459)
        icon = QIcon()
        icon.addFile(u"static/ico.png", QSize(), QIcon.Normal, QIcon.Off)
        log.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(log)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(log)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"\u9ed1\u4f53")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.log_text = QPlainTextEdit(log)
        self.log_text.setObjectName(u"log_text")

        self.verticalLayout.addWidget(self.log_text)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.close_button = QPushButton(log)
        self.close_button.setObjectName(u"close_button")

        self.horizontalLayout.addWidget(self.close_button)

        self.clear_log = QPushButton(log)
        self.clear_log.setObjectName(u"clear_log")

        self.horizontalLayout.addWidget(self.clear_log)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(log)

        QMetaObject.connectSlotsByName(log)
    # setupUi

    def retranslateUi(self, log):
        log.setWindowTitle(QCoreApplication.translate("log", u"\u67e5\u770b\u65e5\u5fd7", None))
        self.label.setText(QCoreApplication.translate("log", u"\u65e5\u5fd7", None))
        self.log_text.setPlainText(QCoreApplication.translate("log", u"\u5f53\u524d\u6ca1\u6709\u65e5\u5fd7\uff01", None))
        self.close_button.setText(QCoreApplication.translate("log", u"\u6211\u77e5\u9053\u4e86", None))
        self.clear_log.setText(QCoreApplication.translate("log", u"\u6e05\u7a7a\u65e5\u5fd7", None))
    # retranslateUi

