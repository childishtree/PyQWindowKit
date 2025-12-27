
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QDialogButtonBox, QSizePolicy
from PySide6.QtCore import Qt, Signal, QEvent

from framelesshelper import FramelessHelper, Theme

class FramelessDialog(QDialog):
    themeChanged = Signal(int) # Theme

    def __init__(self, parent=None, theme=Theme.Dark, buttons=None):
        # Handle overloaded constructor logic
        # If buttons are not passed, default to Ok | Cancel
        if buttons is None:
            buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            
        super().__init__(parent, Qt.WindowType.Dialog)
        
        self.helper_ = FramelessHelper(self, theme)
        self.content_ = QVBoxLayout()
        self.central_ = QWidget(self)
        
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        
        box = QDialogButtonBox(buttons, self)
        
        self.content_.setContentsMargins(9, 9, 9, 9)
        self.content_.addWidget(self.central_, 1)
        self.content_.addWidget(box)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.helper_.titleBar(), 0)
        layout.addLayout(self.content_, 1)
        
        box.accepted.connect(self.onAccepted)
        box.rejected.connect(self.onRejected)
        self.helper_.themeChanged.connect(self.themeChanged)

    def setCentralWidget(self, widget: QWidget):
        if self.central_:
            self.content_.replaceWidget(self.central_, widget)
            self.central_.deleteLater()
        self.central_ = widget
        self.central_.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
    def centralWidget(self) -> QWidget:
        return self.central_
        
    def onAccepted(self):
        self.accept()
        
    def onRejected(self):
        self.reject()
        
    def event(self, event):
        if event.type() == QEvent.Type.WindowActivate:
            menu = self.helper_.titleBar()
            if menu:
                menu.setProperty("bar-active", True)
                self.style().polish(menu)
        elif event.type() == QEvent.Type.WindowDeactivate:
            menu = self.helper_.titleBar()
            if menu:
                menu.setProperty("bar-active", False)
                self.style().polish(menu)
                
        return super().event(event)
