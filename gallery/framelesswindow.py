
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QMenuBar, QMenu, QSizePolicy, QDialog, QVBoxLayout
from PySide6.QtGui import QAction, QActionGroup, QFont, QColor
from PySide6.QtCore import Qt, QTimer, QTime, QEvent, QSize

from framelesshelper import FramelessHelper, Theme
from framelessdialog import FramelessDialog

class ClockWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.startTimer(100)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def timerEvent(self, event):
        super().timerEvent(event)
        self.setText(QTime.currentTime().toString("hh:mm:ss"))


class FramelessWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.helper = FramelessHelper(self, Theme.Dark)
        
        # 2. Construct your title bar
        menuBar = self.createMenuBar()
        
        self.helper.setMenuBar(menuBar)
        self.setMenuWidget(self.helper.titleBar())
        
        # Central Widget
        clockWidget = ClockWidget()
        clockWidget.setObjectName("clock-widget")
        clockWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(clockWidget)
        
        self.setWindowTitle("PyQWindowKit Example Gallery")
        self.resize(800, 600)
        
    def createMenuBar(self):
        menuBar = QMenuBar(self)
        
        # File Menu
        fileMenu = QMenu("File(&F)", menuBar)
        fileMenu.addAction(QAction("New(&N)", menuBar))
        fileMenu.addAction(QAction("Open(&O)", menuBar))
        fileMenu.addSeparator()
        
        # Edit Menu
        editMenu = QMenu("Edit(&E)", menuBar)
        editMenu.addAction(QAction("Undo(&U)", menuBar))
        editMenu.addAction(QAction("Redo(&R)", menuBar))
        
        # Settings Menu
        settingsMenu = QMenu("Settings(&S)", menuBar)
        
        # Custom Dialog Action
        dlgAction = QAction("custom dialog", menuBar)
        dlgAction.triggered.connect(self.showCustomDialog)
        
        # Theme Action
        darkAction = QAction("Enable dark theme", menuBar)
        darkAction.setCheckable(True)
        darkAction.setChecked(True)
        darkAction.triggered.connect(lambda checked: self.helper.loadStyleSheet(Theme.Dark if checked else Theme.Light))
        
        self.helper.themeChanged.connect(lambda theme: darkAction.setChecked(theme == Theme.Dark))
        
        settingsMenu.addAction(darkAction)
        settingsMenu.addAction(dlgAction)
        settingsMenu.addSeparator()

        # Windows Specific Actions
        if sys.platform == "win32":
            noneAction = QAction("None", menuBar)
            noneAction.setData("none")
            noneAction.setCheckable(True)
            noneAction.setChecked(True)
            
            dwmBlurAction = QAction("Enable DWM blur", menuBar)
            dwmBlurAction.setData("dwm-blur")
            dwmBlurAction.setCheckable(True)
            
            acrylicAction = QAction("Enable acrylic material", menuBar)
            acrylicAction.setData("acrylic-material")
            acrylicAction.setCheckable(True)
            
            micaAction = QAction("Enable mica", menuBar)
            micaAction.setData("mica")
            micaAction.setCheckable(True)
            
            micaAltAction = QAction("Enable mica alt", menuBar)
            micaAltAction.setData("mica-alt")
            micaAltAction.setCheckable(True)
            
            winStyleGroup = QActionGroup(menuBar)
            winStyleGroup.addAction(noneAction)
            winStyleGroup.addAction(dwmBlurAction)
            winStyleGroup.addAction(acrylicAction)
            winStyleGroup.addAction(micaAction)
            winStyleGroup.addAction(micaAltAction)
            
            def onWinStyleTriggered(action):
                # Unset all
                for act in winStyleGroup.actions():
                    data = act.data()
                    if not data or data == "none":
                        continue
                    self.helper.setWindowAttribute(data, False)
                
                data = action.data()
                if data == "none":
                    self.setProperty("custom-style", False)
                elif data:
                    self.helper.setWindowAttribute(data, True)
                    self.setProperty("custom-style", True)
                
                self.style().polish(self)
                
            winStyleGroup.triggered.connect(onWinStyleTriggered)
            
            settingsMenu.addAction(noneAction)
            settingsMenu.addAction(dwmBlurAction)
            settingsMenu.addAction(acrylicAction)
            settingsMenu.addAction(micaAction)
            settingsMenu.addAction(micaAltAction)
            
        elif sys.platform == "darwin":
            # Mac specific actions...
            pass
            
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(settingsMenu)
        
        return menuBar
        
    def showCustomDialog(self):
        label = QLabel("Hello world")
        label.setObjectName("test")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        dialog = FramelessDialog(self, self.helper.getTheme())
        dialog.setWindowTitle("Help")
        dialog.setFixedSize(400, 240)
        dialog.setCentralWidget(label)
        dialog.exec()
        
    def event(self, event):
        if event.type() == QEvent.Type.WindowActivate:
            menu = self.menuWidget()
            if menu:
                menu.setProperty("bar-active", True)
                self.style().polish(menu)
        elif event.type() == QEvent.Type.WindowDeactivate:
            menu = self.menuWidget()
            if menu:
                menu.setProperty("bar-active", False)
                self.style().polish(menu)
                
        return super().event(event)