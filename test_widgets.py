
import sys
import os

# ================= Setup Start =================
# Add install dir to sys.path
install_dir = os.path.join(os.getcwd(), "out", "install", "x64-msvc-Release")
sys.path.append(install_dir)
# ================= Setup End =================

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PyQWindowKit import Widgets as QWKWidgets

class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        
        # 1. Create the Agent
        self.agent = QWKWidgets.WidgetWindowAgent(self)
        
        # 2. Setup the window
        self.agent.setup(self)
        
        # 3. Setup UI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title Bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(30)
        self.title_bar.setStyleSheet("background-color: #333; color: white;")
        title_layout = QVBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_label = QLabel("PyQWindowKit Widgets Demo")
        title_layout.addWidget(title_label)
        
        layout.addWidget(self.title_bar)
        
        # Content
        content = QLabel("Hello from QWidget + PyQWindowKit!")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content)
        
        # 4. Set Title Bar to Agent (enables dragging)
        self.agent.setTitleBar(self.title_bar)
        
        # 5. Add some system buttons behavior (optional/simulated for this demo)
        # Note: Real system buttons need more setup, but dragging is the key feature to test.

if __name__ == "__main__":
    QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
