# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

class Ui_bilibili_downloader(object):
    def setupUi(self, bilibili_downloader):
        if not bilibili_downloader.objectName():
            bilibili_downloader.setObjectName(u"bilibili_downloader")
        bilibili_downloader.resize(420, 316)
        icon = QIcon()
        icon.addFile(u"static/ico.png", QSize(), QIcon.Normal, QIcon.Off)
        bilibili_downloader.setWindowIcon(icon)
        self.quit = QAction(bilibili_downloader)
        self.quit.setObjectName(u"quit")
        self.help_text = QAction(bilibili_downloader)
        self.help_text.setObjectName(u"help_text")
        self.about_this = QAction(bilibili_downloader)
        self.about_this.setObjectName(u"about_this")
        self.open_base_dir = QAction(bilibili_downloader)
        self.open_base_dir.setObjectName(u"open_base_dir")
        self.action_5 = QAction(bilibili_downloader)
        self.action_5.setObjectName(u"action_5")
        self.read_log = QAction(bilibili_downloader)
        self.read_log.setObjectName(u"read_log")
        self.set_cookie_action = QAction(bilibili_downloader)
        self.set_cookie_action.setObjectName(u"set_cookie_action")
        self.check_for_update_action = QAction(bilibili_downloader)
        self.check_for_update_action.setObjectName(u"check_for_update_action")
        self.open_save_dir = QAction(bilibili_downloader)
        self.open_save_dir.setObjectName(u"open_save_dir")
        self.centralwidget = QWidget(bilibili_downloader)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_6 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer = QSpacerItem(2, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(13, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 80))
        self.label_4.setMaximumSize(QSize(83, 80))
        font = QFont()
        font.setPointSize(36)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_4)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(181, 91))
        self.label.setMaximumSize(QSize(181, 91))
        self.label.setAutoFillBackground(True)
        self.label.setPixmap(QPixmap(u"static/bilibili_logo.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 80))
        self.label_5.setMaximumSize(QSize(83, 80))
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setWordWrap(False)

        self.horizontalLayout.addWidget(self.label_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.url = QLineEdit(self.centralwidget)
        self.url.setObjectName(u"url")
        self.url.setDragEnabled(False)

        self.horizontalLayout_2.addWidget(self.url)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.change_save_path = QToolButton(self.centralwidget)
        self.change_save_path.setObjectName(u"change_save_path")

        self.horizontalLayout_5.addWidget(self.change_save_path)

        self.save_path = QLabel(self.centralwidget)
        self.save_path.setObjectName(u"save_path")
        self.save_path.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.save_path)

        self.open_save_dir_button = QToolButton(self.centralwidget)
        self.open_save_dir_button.setObjectName(u"open_save_dir_button")

        self.horizontalLayout_5.addWidget(self.open_save_dir_button)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.video_format = QComboBox(self.centralwidget)
        self.video_format.addItem("")
        self.video_format.setObjectName(u"video_format")

        self.horizontalLayout_3.addWidget(self.video_format)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_3)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_11)

        self.video_quality = QComboBox(self.centralwidget)
        self.video_quality.addItem("")
        self.video_quality.addItem("")
        self.video_quality.addItem("")
        self.video_quality.addItem("")
        self.video_quality.addItem("")
        self.video_quality.setObjectName(u"video_quality")

        self.horizontalLayout_3.addWidget(self.video_quality)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_4)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_12)

        self.async_tasks_max_num = QSpinBox(self.centralwidget)
        self.async_tasks_max_num.setObjectName(u"async_tasks_max_num")
        self.async_tasks_max_num.setMinimum(1)
        self.async_tasks_max_num.setMaximum(6)
        self.async_tasks_max_num.setValue(5)

        self.horizontalLayout_3.addWidget(self.async_tasks_max_num)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)

        self.all_progress_bar = QProgressBar(self.centralwidget)
        self.all_progress_bar.setObjectName(u"all_progress_bar")
        self.all_progress_bar.setMaximum(100)
        self.all_progress_bar.setValue(0)

        self.gridLayout.addWidget(self.all_progress_bar, 1, 1, 1, 1)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout.addWidget(self.progress_bar, 0, 1, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)


        self.horizontalLayout_4.addLayout(self.gridLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 0))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_10)

        self.speed = QLabel(self.centralwidget)
        self.speed.setObjectName(u"speed")
        self.speed.setScaledContents(False)
        self.speed.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.speed)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.download_button = QPushButton(self.centralwidget)
        self.download_button.setObjectName(u"download_button")
        self.download_button.setMinimumSize(QSize(71, 41))

        self.horizontalLayout_4.addWidget(self.download_button)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(13, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 3)
        self.horizontalLayout_6.setStretch(2, 1)
        bilibili_downloader.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(bilibili_downloader)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 420, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        bilibili_downloader.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(bilibili_downloader)
        self.statusbar.setObjectName(u"statusbar")
        bilibili_downloader.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.open_base_dir)
        self.menu.addAction(self.open_save_dir)
        self.menu.addSeparator()
        self.menu.addAction(self.quit)
        self.menu_2.addAction(self.help_text)
        self.menu_2.addAction(self.read_log)
        self.menu_2.addAction(self.check_for_update_action)
        self.menu_2.addAction(self.about_this)
        self.menu_3.addAction(self.set_cookie_action)

        self.retranslateUi(bilibili_downloader)

        QMetaObject.connectSlotsByName(bilibili_downloader)
    # setupUi

    def retranslateUi(self, bilibili_downloader):
        bilibili_downloader.setWindowTitle(QCoreApplication.translate("bilibili_downloader", u"B\u7ad9\u4e0b\u8f7d\u5c0f\u5de5\u5177 v1.0.0", None))
        self.quit.setText(QCoreApplication.translate("bilibili_downloader", u"\u9000\u51fa", None))
        self.help_text.setText(QCoreApplication.translate("bilibili_downloader", u"\u5e2e\u52a9\u6587\u6863", None))
        self.about_this.setText(QCoreApplication.translate("bilibili_downloader", u"\u5173\u4e8e", None))
        self.open_base_dir.setText(QCoreApplication.translate("bilibili_downloader", u"\u6253\u5f00\u7a0b\u5e8f\u5730\u5740", None))
        self.action_5.setText(QCoreApplication.translate("bilibili_downloader", u"\u6253\u8d4f", None))
        self.read_log.setText(QCoreApplication.translate("bilibili_downloader", u"\u67e5\u770b\u65e5\u5fd7", None))
        self.set_cookie_action.setText(QCoreApplication.translate("bilibili_downloader", u"\u8bbe\u7f6ecookie", None))
        self.check_for_update_action.setText(QCoreApplication.translate("bilibili_downloader", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.open_save_dir.setText(QCoreApplication.translate("bilibili_downloader", u"\u6253\u5f00\u50a8\u5b58\u5730\u5740", None))
        self.label_4.setText(QCoreApplication.translate("bilibili_downloader", u"\u23ec", None))
        self.label.setText("")
        self.label_5.setText(QCoreApplication.translate("bilibili_downloader", u"\u23ec", None))
        self.label_2.setText(QCoreApplication.translate("bilibili_downloader", u"\u89c6\u9891\u94fe\u63a5\uff1a", None))
        self.url.setPlaceholderText(QCoreApplication.translate("bilibili_downloader", u"\u8bf7\u5728\u6b64\u5904\u7c98\u8d34\u9700\u8981\u4e0b\u8f7d\u7684\u89c6\u9891\u94fe\u63a5", None))
        self.label_3.setText(QCoreApplication.translate("bilibili_downloader", u"\u4fdd\u5b58\u8def\u5f84\uff1a", None))
        self.change_save_path.setText(QCoreApplication.translate("bilibili_downloader", u"\u66f4\u6539", None))
        self.save_path.setText(QCoreApplication.translate("bilibili_downloader", u"-----", None))
        self.open_save_dir_button.setText(QCoreApplication.translate("bilibili_downloader", u"\u6253\u5f00", None))
        self.label_7.setText(QCoreApplication.translate("bilibili_downloader", u"\u6587\u4ef6\u683c\u5f0f\uff1a", None))
        self.video_format.setItemText(0, QCoreApplication.translate("bilibili_downloader", u".flv", None))

        self.label_11.setText(QCoreApplication.translate("bilibili_downloader", u"\u89c6\u9891\u753b\u8d28\uff1a", None))
        self.video_quality.setItemText(0, QCoreApplication.translate("bilibili_downloader", u"360P", None))
        self.video_quality.setItemText(1, QCoreApplication.translate("bilibili_downloader", u"480P", None))
        self.video_quality.setItemText(2, QCoreApplication.translate("bilibili_downloader", u"720P", None))
        self.video_quality.setItemText(3, QCoreApplication.translate("bilibili_downloader", u"1080P", None))
        self.video_quality.setItemText(4, QCoreApplication.translate("bilibili_downloader", u"1080P+", None))

        self.label_12.setText(QCoreApplication.translate("bilibili_downloader", u"\u5e76\u884c\u4efb\u52a1\u6570\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("bilibili_downloader", u"\u603b\u8fdb\u5ea6", None))
        self.label_8.setText(QCoreApplication.translate("bilibili_downloader", u"\u8fdb\u5ea6", None))
        self.label_10.setText(QCoreApplication.translate("bilibili_downloader", u"\u4e0b\u8f7d\u901f\u5ea6", None))
        self.speed.setText(QCoreApplication.translate("bilibili_downloader", u"----", None))
        self.download_button.setText(QCoreApplication.translate("bilibili_downloader", u"\u4e0b\u8f7d", None))
        self.menu.setTitle(QCoreApplication.translate("bilibili_downloader", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("bilibili_downloader", u"\u5e2e\u52a9", None))
        self.menu_3.setTitle(QCoreApplication.translate("bilibili_downloader", u"\u8bbe\u7f6e", None))
    # retranslateUi

