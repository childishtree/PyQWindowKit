
from PySide6.QtWidgets import QFrame, QWidget, QMenuBar, QLabel, QAbstractButton, QHBoxLayout, QSizePolicy, QBoxLayout, QSpacerItem
from PySide6.QtCore import Qt, Signal, QEvent, QLocale, QSize
from PySide6.QtGui import QIcon

class WindowBarPrivate:
    def __init__(self, q):
        self.q = q
        self.w = None
        self.autoTitle = True
        self.autoIcon = False
        self.layout = None
        
        # Indices for layout (WindowBarItem enum)
        self.IconButton = 0
        self.MenuWidget = 1
        self.TitleLabel = 2
        self.PinButton = 3
        self.MinimizeButton = 4
        self.MaximizeButton = 5
        self.CloseButton = 6
        
    def init(self):
        self.layout = QHBoxLayout(self.q)
        if QLocale.system().textDirection() == Qt.LayoutDirection.RightToLeft:
            self.layout.setDirection(QBoxLayout.Direction.RightToLeft)
            
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        for i in range(self.IconButton, self.CloseButton + 1):
            self.insertDefaultSpace(i)
            
    def insertDefaultSpace(self, index):
        self.layout.insertSpacerItem(index, QSpacerItem(0, 0))
        
    def setWidgetAt(self, index, widget):
        item = self.layout.takeAt(index)
        if item:
            w = item.widget()
            if w:
                w.deleteLater()
            # C++: delete item; 
            # In Python, the item object is garbage collected, but we should ensure C++ side is fine.
            # QLayout::takeAt returns ownership to the caller.
        
        if not widget:
            self.insertDefaultSpace(index)
        else:
            self.layout.insertWidget(index, widget)
            
    def takeWidgetAt(self, index):
        item = self.layout.itemAt(index)
        if not item:
            return None
            
        orgWidget = item.widget()
        if orgWidget:
            self.layout.takeAt(index)
            self.insertDefaultSpace(index)
            return orgWidget
        return None
        
    def widgetAt(self, index):
        item = self.layout.itemAt(index)
        if item:
            return item.widget()
        return None

class WindowBar(QFrame):
    pinRequested = Signal(bool)
    minimizeRequested = Signal()
    maximizeRequested = Signal(bool)
    closeRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.d = WindowBarPrivate(self)
        self.d.init()

    def menuBar(self) -> QMenuBar:
        return self.d.widgetAt(self.d.MenuWidget)

    def titleLabel(self) -> QLabel:
        return self.d.widgetAt(self.d.TitleLabel)

    def iconButton(self) -> QAbstractButton:
        return self.d.widgetAt(self.d.IconButton)

    def pinButton(self) -> QAbstractButton:
        return self.d.widgetAt(self.d.PinButton)

    def minButton(self) -> QAbstractButton:
        return self.d.widgetAt(self.d.MinimizeButton)

    def maxButton(self) -> QAbstractButton:
        return self.d.widgetAt(self.d.MaximizeButton)

    def closeButton(self) -> QAbstractButton:
        return self.d.widgetAt(self.d.CloseButton)

    def setMenuBar(self, menuBar: QMenuBar):
        org = self.takeMenuBar()
        if org:
            org.deleteLater()
        if not menuBar:
            return
        self.d.setWidgetAt(self.d.MenuWidget, menuBar)
        menuBar.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

    def setTitleLabel(self, label: QLabel):
        org = self.takeTitleLabel()
        if org:
            org.deleteLater()
        if not label:
            return
        self.d.setWidgetAt(self.d.TitleLabel, label)
        if self.d.autoTitle and self.d.w:
            label.setText(self.d.w.windowTitle())
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def setIconButton(self, btn: QAbstractButton):
        org = self.takeIconButton()
        if org:
            org.deleteLater()
        if not btn:
            return
        self.d.setWidgetAt(self.d.IconButton, btn)
        if self.d.autoIcon and self.d.w:
            btn.setIcon(self.d.w.windowIcon())
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

    def setPinButton(self, btn: QAbstractButton):
        org = self.takePinButton()
        if org:
            org.deleteLater()
        if not btn:
            return
        self.d.setWidgetAt(self.d.PinButton, btn)
        btn.clicked.connect(self.pinRequested)

    def setMinButton(self, btn: QAbstractButton):
        org = self.takeMinButton()
        if org:
            org.deleteLater()
        if not btn:
            return
        self.d.setWidgetAt(self.d.MinimizeButton, btn)
        btn.clicked.connect(self.minimizeRequested)

    def setMaxButton(self, btn: QAbstractButton):
        org = self.takeMaxButton()
        if org:
            org.deleteLater()
        if not btn:
            return
        self.d.setWidgetAt(self.d.MaximizeButton, btn)
        btn.clicked.connect(self.maximizeRequested)

    def setCloseButton(self, btn: QAbstractButton):
        org = self.takeCloseButton()
        if org:
            org.deleteLater()
        if not btn:
            return
        self.d.setWidgetAt(self.d.CloseButton, btn)
        btn.clicked.connect(self.closeRequested)

    def takeMenuBar(self) -> QMenuBar:
        return self.d.takeWidgetAt(self.d.MenuWidget)

    def takeTitleLabel(self) -> QLabel:
        return self.d.takeWidgetAt(self.d.TitleLabel)

    def takeIconButton(self) -> QAbstractButton:
        return self.d.takeWidgetAt(self.d.IconButton)

    def takePinButton(self) -> QAbstractButton:
        btn = self.d.takeWidgetAt(self.d.PinButton)
        if not btn:
            return None
        btn.clicked.disconnect(self.pinRequested)
        return btn

    def takeMinButton(self) -> QAbstractButton:
        btn = self.d.takeWidgetAt(self.d.MinimizeButton)
        if not btn:
            return None
        btn.clicked.disconnect(self.minimizeRequested)
        return btn

    def takeMaxButton(self) -> QAbstractButton:
        btn = self.d.takeWidgetAt(self.d.MaximizeButton)
        if not btn:
            return None
        btn.clicked.disconnect(self.maximizeRequested)
        return btn

    def takeCloseButton(self) -> QAbstractButton:
        btn = self.d.takeWidgetAt(self.d.CloseButton)
        if not btn:
            return None
        btn.clicked.disconnect(self.closeRequested)
        return btn

    def hostWidget(self) -> QWidget:
        return self.d.w

    def setHostWidget(self, w: QWidget):
        org = self.d.w
        if org:
            org.removeEventFilter(self)
        self.d.w = w
        if w:
            w.installEventFilter(self)

    def titleFollowWindow(self) -> bool:
        return self.d.autoTitle

    def setTitleFollowWindow(self, value: bool):
        self.d.autoTitle = value

    def iconFollowWindow(self) -> bool:
        return self.d.autoIcon

    def setIconFollowWindow(self, value: bool):
        self.d.autoIcon = value

    def eventFilter(self, obj, event):
        w = self.d.w
        if obj == w:
            iconBtn = self.iconButton()
            label = self.titleLabel()
            maxBtn = self.maxButton()
            
            if event.type() == QEvent.Type.WindowIconChange:
                if self.d.autoIcon and iconBtn:
                    iconBtn.setIcon(w.windowIcon())
                    self.iconChanged(w.windowIcon())
            elif event.type() == QEvent.Type.WindowTitleChange:
                if self.d.autoTitle and label:
                    label.setText(w.windowTitle())
                    self.titleChanged(w.windowTitle())
            elif event.type() == QEvent.Type.WindowStateChange:
                if maxBtn:
                    maxBtn.setChecked(w.isMaximized())
                    
        return super().eventFilter(obj, event)

    def titleChanged(self, text: str):
        pass

    def iconChanged(self, icon: QIcon):
        pass
