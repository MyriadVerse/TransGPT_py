from PySide6 import QtWidgets

from chat_tab import ChatTab


# ChatWindow 类，主窗口
class ChatWindow(QtWidgets.QWidget):
    def __init__(self, configuration):
        super().__init__()
        self.tab_count = 0
        self.configuration = configuration
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("TransGPT")
        self.setGeometry(50, 50, 800, 600)

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.tabCloseRequested.connect(self.check_tab_count)
        self.tab_widget.setUsesScrollButtons(True)  
        self.tab_widget.setTabPosition(QtWidgets.QTabWidget.West)
        
        self.new_tab_button = QtWidgets.QPushButton("New Chat Tab", self)
        self.new_tab_button.clicked.connect(self.add_new_tab)
        
        self.bottom_box = QtWidgets.QGroupBox()
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_box)
        self.copyright = QtWidgets.QLabel("© [2023] Oops Computing Team. All Rights Reserved.")
        
        self.bottom_layout.addWidget(self.copyright)
        self.bottom_layout.addWidget(self.new_tab_button)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.bottom_box)

        self.add_new_tab()
        self.deco_ui()
      
        
        
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
        
        self.new_tab_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #e6f7ff, stop: 1 #b3e0ff);  /* Light blue gradient background */
                color: #2F4F4F;  /* Dark Slate Gray */
                border: 2px solid #6699cc;  /* Light blue border */
                border-radius: 15px;  /* Rounded corners */
                padding: 10px 25px;  /* Padding: vertical, horizontal */
                font-size: 16px;  /* Text size */
                font-family: "Arial";  /* Font family */

            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #cce6ff, stop: 1 #99c2ff);  /* Lighter blue gradient when hovered */
                border: 2px solid #336699;  /* Darker blue border when hovered */
            }
            QPushButton:pressed {
                background-color: #6699cc;  /* Solid light blue when pressed */
                color: #FFFFFF;  /* White text when pressed */
            }
        """)


    def add_new_tab(self):
        self.tab_count += 1
        api_key = self.configuration.get_api_key()
        chat_tab = ChatTab(api_key)
        index = self.tab_widget.addTab(chat_tab, f"Chat {self.tab_count}")
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
    
    def check_tab_count(self):
        if self.tab_widget.count() == 0:
            QtWidgets.QApplication.quit()



