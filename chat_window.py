from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QMainWindow
from chat_tab import ChatTab
from component import MinTab

import os
os.environ['HTTP_PROXY'] = '192.168.43.224:7890'
os.environ['HTTPS_PROXY'] = '192.168.43.224:7890'

# 管理用户交互并促进应用程序内部的对话流程
# ChatWindow 类，主窗口
class ChatWindow(QtWidgets.QWidget):
    def __init__(self, configuration):
        super().__init__()
        self.tab_count = 0
        self.configuration = configuration
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("TransGPT")
        self.setGeometry(50, 50, 800, 600)

        # 用于独立窗口
        self.new_window = None
        self.chat_tab = None
        self.opened_windows = []  # 用于存储已经打开的窗口

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.tabCloseRequested.connect(self.check_tab_count)
        self.tab_widget.setUsesScrollButtons(True)
        self.tab_widget.setTabPosition(QtWidgets.QTabWidget.West)

        self.import_button = QtWidgets.QPushButton("Import Local Model", self)
        self.import_button.clicked.connect(self.import_model)
        #   self.import_button.clicked.connect(self.add_new_tab)

        self.new_tab_button = QtWidgets.QPushButton("New Chat Tab", self)
        self.new_tab_button.clicked.connect(self.add_new_tab)

        self.min_button = QtWidgets.QPushButton("Minimize", self)
        self.min_button.clicked.connect(self.min_tab)

        self.bottom_box = QtWidgets.QGroupBox()
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_box)
        self.copyright = QtWidgets.QLabel("© [2023] Oops Computing Team. All Rights Reserved.")

        self.bottom_layout.addWidget(self.copyright)
        self.bottom_layout.addWidget(self.import_button)
        self.bottom_layout.addWidget(self.new_tab_button)
        self.bottom_layout.addWidget(self.min_button)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.bottom_box)

        self.add_new_tab()
        self.deco_ui()


    def add_new_tab(self):
        self.tab_count += 1
        api_key = self.configuration.get_api_key()
        chat_tab = ChatTab(api_key)
        index = self.tab_widget.addTab(chat_tab, f"Chat {self.tab_count}")
        self.tab_widget.setCurrentIndex(index)

    def min_tab(self):
        self.new_window = QMainWindow()
        self.new_window.setWindowTitle(f"Widget")

        api_key = self.configuration.get_api_key()
        self.chat_tab = MinTab(api_key)
        self.new_window.setCentralWidget(self.chat_tab)
        self.new_window.setFixedHeight(300)
        self.new_window.setFixedWidth(400)
        self.new_window.setStyleSheet("background-color: white;")

        # 连接 self.new_window 的 destroyed 信号
        self.new_window.destroyed.connect(self.show_normal)

        # 在小窗口被关闭时，检查主窗口是否处于最小化状态
        self.new_window.installEventFilter(self)

        self.new_window.show()
        self.opened_windows.append(self.new_window)

        # 最小化原始页
        self.showMinimized()

    # 在主窗口关闭时关闭所有已打开的窗口
    def closeEvent(self, event):
        if self.opened_windows:
            for window in self.opened_windows:
                window.close()
            event.accept()

    def eventFilter(self, obj, event):
        if obj == self.new_window and event.type() == QtCore.QEvent.Close:
            self.show_normal()
        return super().eventFilter(obj, event)

    # 主窗口正常化
    def show_normal(self):
        self.setFocus()
        self.showNormal()

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def check_tab_count(self):
        if self.tab_widget.count() == 0:
            QtWidgets.QApplication.quit()

    @Slot()
    def import_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open .bin File", "", "BIN Files (*.bin)")
        from typing import cast
        current_tab = cast(ChatTab, self.tab_widget.currentWidget())
        current_tab.model_path=file_name

    
    def deco_ui(self):
        self.setStyleSheet("background-color: white;")
        self.copyright.setStyleSheet("background-color: white;")
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #e1f4ff;
                color: #4a4a4a;
                padding: 8px;
                width: 20px;
                height: 90px;
                border-top-left-radius: 6px;  
                border-bottom-left-radius: 6px;
                border-right: 2px solid #c8e0f0; 
            }
            QTabBar::tab:selected {
                background: #2e91f9;
                color: #ffffff;
                border-right: 2px solid #2e91f9; 
            }
            QTabBar QAbstractButton {
                background: #e1f4ff;
                border: none;
                padding: 10px;  
            }
            QTabBar QAbstractButton::up-arrow {
                width: 0;
                height: 0;
                border-left: 7px solid transparent;   
                border-right: 7px solid transparent;  
                border-bottom: 12px solid #2e91f9;   
            }
            QTabBar QAbstractButton::down-arrow {
                width: 0;
                height: 0;
                border-left: 7px solid transparent;  
                border-right: 7px solid transparent; 
                border-top: 12px solid #2e91f9;       
            }
        """)
        self.import_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #C5E1A5, stop: 1 #8BC34A);
                color: #2F4F4F;
                border: 2px solid #8BC34A;
                border-radius: 0;
                padding: 10px 25px;
                font-size: 16px;
                font-family: "Arial";
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #D7EED6, stop: 1 #AED581);
                border: 2px solid #006400;
            }
            QPushButton:pressed {
                background-color: #8BC34A;
                color: #FFFFFF;
            }
        """)

        self.new_tab_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #e6f7ff, stop: 1 #b3e0ff);
                color: #2F4F4F;
                border: 2px solid #6699cc;
                border-radius: 0; /* 移除圆角矩形 */
                padding: 10px 25px;
                font-size: 16px;
                font-family: "Arial";
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #cce6ff, stop: 1 #99c2ff);
                border: 2px solid #336699;
            }
            QPushButton:pressed {
                background-color: #6699cc;
                color: #FFFFFF;
            }
        """)

        self.min_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #D2B48C, stop: 1 #D2B48C);
                color: #2F4F4F;
                border: 2px solid #6699cc;
                border-radius: 0; /* 移除圆角矩形 */
                padding: 10px 25px;
                font-size: 16px;
                font-family: "Arial";
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #FFD700, stop: 1 #FFD700);
                border: 2px solid #336699;
            }
            QPushButton:pressed {
                background-color: #cd853f;
                color: #FFFFFF;
            }
        """)





