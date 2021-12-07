# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cookie.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_cookie_ui(object):
    def setupUi(self, cookie_ui):
        if not cookie_ui.objectName():
            cookie_ui.setObjectName(u"cookie_ui")
        cookie_ui.setWindowModality(Qt.WindowModal)
        cookie_ui.resize(1894, 1011)
        icon = QIcon()
        icon.addFile(u"static/ico.png", QSize(), QIcon.Normal, QIcon.Off)
        cookie_ui.setWindowIcon(icon)
        self.verticalLayout_6 = QVBoxLayout(cookie_ui)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.label_6 = QLabel(cookie_ui)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setPixmap(QPixmap(u"static/firefox_cookie_help.png"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.label_7 = QLabel(cookie_ui)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setPixmap(QPixmap(u"static/edge_cookie_help.png"))
        self.label_7.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_7)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_7)

        self.line_3 = QFrame(cookie_ui)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(cookie_ui)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.label = QLabel(cookie_ui)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(cookie_ui)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(cookie_ui)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_8 = QLabel(cookie_ui)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.line = QFrame(cookie_ui)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(cookie_ui)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.update_datetime_text = QLabel(cookie_ui)
        self.update_datetime_text.setObjectName(u"update_datetime_text")

        self.verticalLayout.addWidget(self.update_datetime_text)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_9 = QLabel(cookie_ui)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_3.addWidget(self.label_9)

        self.SESSDATA_INPUT = QLineEdit(cookie_ui)
        self.SESSDATA_INPUT.setObjectName(u"SESSDATA_INPUT")

        self.verticalLayout_3.addWidget(self.SESSDATA_INPUT)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.update_button = QPushButton(cookie_ui)
        self.update_button.setObjectName(u"update_button")

        self.verticalLayout_5.addWidget(self.update_button)

        self.cancel_button = QPushButton(cookie_ui)
        self.cancel_button.setObjectName(u"cancel_button")

        self.verticalLayout_5.addWidget(self.cancel_button)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.line_2 = QFrame(cookie_ui)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.verticalLayout_6.setStretch(2, 1)

        self.retranslateUi(cookie_ui)

        QMetaObject.connectSlotsByName(cookie_ui)
    # setupUi

    def retranslateUi(self, cookie_ui):
        cookie_ui.setWindowTitle(QCoreApplication.translate("cookie_ui", u"\u8bbe\u7f6eCookie-SESSDATA", None))
        self.label_6.setText("")
        self.label_7.setText("")
        self.label_4.setText(QCoreApplication.translate("cookie_ui", u"\u9700\u8981\u586b\u5165\u7684\u662fcookies\u4e2d\u7684sessdata\uff0c\u53ef\u53c2\u8003\u4ee5\u4e0b\u6b65\u9aa4\u6765\u83b7\u53d6", None))
        self.label.setText(QCoreApplication.translate("cookie_ui", u"1.\u5728\u6d4f\u89c8\u5668\u4e0a\u8bbf\u95ee\u54d4\u54e9\u54d4\u54e9\u9996\u9875(www.bilibili.com)", None))
        self.label_2.setText(QCoreApplication.translate("cookie_ui", u"2.\u767b\u5f55", None))
        self.label_3.setText(QCoreApplication.translate("cookie_ui", u"3.\u6309\u4e0bF12\uff0c\u6253\u5f00\u6d4f\u89c8\u5668\u7684\u5f00\u53d1\u8005\u6a21\u5f0f", None))
        self.label_8.setText(QCoreApplication.translate("cookie_ui", u"4.\u8bf7\u6839\u636e\u4e0a\u56fe(\u4ee5\u706b\u72d0\u6d4f\u89c8\u5668\u3001Edge\u6d4f\u89c8\u5668\u4e3a\u4f8b)\u7684\u6307\u5f15\u627e\u5230SESSDATA\uff0c\u590d\u5236\u5176\u503c\u5e76\u7c98\u8d34\u5728\u53f3\u8fb9\u7684\u8f93\u5165\u6846\u4e2d", None))
        self.label_5.setText(QCoreApplication.translate("cookie_ui", u"\u4e0a\u6b21\u66f4\u65b0\u65f6\u95f4:", None))
        self.update_datetime_text.setText(QCoreApplication.translate("cookie_ui", u"update_datetime", None))
        self.label_9.setText(QCoreApplication.translate("cookie_ui", u"\u8bf7\u5728\u4e0b\u65b9\u8f93\u5165SESSDATA\uff1a", None))
        self.SESSDATA_INPUT.setPlaceholderText(QCoreApplication.translate("cookie_ui", u"\u8bf7\u5728\u6b64\u5904\u8f93\u5165SESSDATA", None))
        self.update_button.setText(QCoreApplication.translate("cookie_ui", u"\u66f4\u65b0", None))
        self.cancel_button.setText(QCoreApplication.translate("cookie_ui", u"\u53d6\u6d88", None))
    # retranslateUi

