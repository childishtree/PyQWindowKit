
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal, Qt, Property
from PySide6.QtGui import QIcon, QMouseEvent

class WindowButtonPrivate:
    def __init__(self, q):
        self.q = q
        self.iconNormal = QIcon()
        self.iconChecked = QIcon()
        self.iconDisabled = QIcon()

    def init(self):
        pass

    def reloadIcon(self):
        if not self.q.isEnabled() and not self.iconDisabled.isNull():
            self.q.setIcon(self.iconDisabled)
            return

        if self.q.isChecked() and not self.iconChecked.isNull():
            self.q.setIcon(self.iconChecked)
            return

        if not self.iconNormal.isNull():
            self.q.setIcon(self.iconNormal)

class WindowButton(QPushButton):
    doubleClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.d = WindowButtonPrivate(self)
        self.d.init()

    def getIconNormal(self) -> QIcon:
        return self.d.iconNormal

    def setIconNormal(self, icon: QIcon):
        self.d.iconNormal = icon
        self.d.reloadIcon()

    def getIconChecked(self) -> QIcon:
        return self.d.iconChecked

    def setIconChecked(self, icon: QIcon):
        self.d.iconChecked = icon
        self.d.reloadIcon()

    def getIconDisabled(self) -> QIcon:
        return self.d.iconDisabled

    def setIconDisabled(self, icon: QIcon):
        self.d.iconDisabled = icon
        self.d.reloadIcon()

    iconNormal = Property(QIcon, getIconNormal, setIconNormal)
    iconChecked = Property(QIcon, getIconChecked, setIconChecked)
    iconDisabled = Property(QIcon, getIconDisabled, setIconDisabled)

    def checkStateSet(self):
        super().checkStateSet()
        self.d.reloadIcon()
        
    def nextCheckState(self):
        # QPushButton doesn't expose checkStateSet directly in a way that is easily overridable 
        # to catch all state changes, but checkStateSet is called by nextCheckState 
        # and other internal methods.
        # In PySide6, checkStateSet is protected.
        super().nextCheckState()
        # self.d.reloadIcon() # nextCheckState calls checkStateSet internally

    def changeEvent(self, event):
        # Catch enabled/disabled state change
        if event.type() == event.Type.EnabledChange:
             self.d.reloadIcon()
        super().changeEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)
