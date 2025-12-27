
import os
import sys

from PySide6.QtCore import Qt, QTimer, QEvent, QPoint, QSize, QRect, Signal, QObject, QFile, QIODevice
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QMenuBar, QFrame
from PySide6.QtGui import QIcon, QWindow, QAction, QActionGroup, QCursor, QGuiApplication

import PyQWindowKit
from PyQWindowKit import Widgets

from widgetframe.windowbar import WindowBar
from widgetframe.windowbutton import WindowButton
import resources_rc

class Theme:
    Dark = 0
    Light = 1

class FramelessHelper(QObject):
    themeChanged = Signal(int) # Theme enum

    def __init__(self, parent: QWidget, theme=Theme.Dark):
        super().__init__(parent)
        self.m_target = parent
        self.m_currentTheme = theme
        
        self.m_target.setAttribute(Qt.WidgetAttribute.WA_DontCreateNativeAncestors)
        self.m_target.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        
        self.installWindowAgent()
        self.loadStyleSheet(theme)
        
    def installWindowAgent(self):
        self.m_windowAgent = Widgets.WidgetWindowAgent(self.m_target)
        self.m_windowAgent.setup(self.m_target)
        
        self.m_windowBar = WindowBar(self.m_target)
        
        titleLabel = QLabel()
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setObjectName("win-title-label")
        self.m_windowBar.setTitleLabel(titleLabel)
        
        # Setup system buttons
        # In Python we can just use the ones created by WindowBar, but we need to tell Agent about them
        
        iconButton = WindowButton()
        iconButton.setObjectName("icon-button")
        iconButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.m_windowBar.setIconButton(iconButton)
        self.m_windowAgent.setSystemButton(Widgets.WindowAgentBase.SystemButton.WindowIcon, iconButton)
        
        minButton = WindowButton()
        minButton.setObjectName("min-button")
        minButton.setProperty("system-button", True)
        minButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.m_windowBar.setMinButton(minButton)
        self.m_windowAgent.setSystemButton(Widgets.WindowAgentBase.SystemButton.Minimize, minButton)
        
        maxButton = WindowButton()
        maxButton.setCheckable(True)
        maxButton.setObjectName("max-button")
        maxButton.setProperty("system-button", True)
        maxButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.m_windowBar.setMaxButton(maxButton)
        self.m_windowAgent.setSystemButton(Widgets.WindowAgentBase.SystemButton.Maximize, maxButton)
        
        closeButton = WindowButton()
        closeButton.setObjectName("close-button")
        closeButton.setProperty("system-button", True)
        closeButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.m_windowBar.setCloseButton(closeButton)
        self.m_windowAgent.setSystemButton(Widgets.WindowAgentBase.SystemButton.Close, closeButton)
        
        self.m_windowBar.setHostWidget(self.m_target)
        self.m_windowAgent.setTitleBar(self.m_windowBar)
        
        # Connections
        self.m_windowBar.minimizeRequested.connect(self.m_target.showMinimized)
        self.m_windowBar.maximizeRequested.connect(self._onMaximizeRequested)
        self.m_windowBar.closeRequested.connect(self.m_target.close)
        
    def _onMaximizeRequested(self, max):
        if max:
            self.m_target.showMaximized()
        else:
            self.m_target.showNormal()
            
    def loadStyleSheet(self, theme):
        self.m_currentTheme = theme
        
        qss_path = ":/qss/dark-style.qss" if theme == Theme.Dark else ":/qss/light-style.qss"
        
        qss = QFile(qss_path)
        if qss.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            # Read as bytes then decode
            style = str(qss.readAll(), encoding='utf-8')
            self.m_target.setStyleSheet(style)
            self.themeChanged.emit(self.m_currentTheme)
        else:
            print(f"Warning: QSS file not found: {qss_path}")
            
    def setMenuBar(self, menuBar):
        menuBar.setObjectName("win-menu-bar")
        self.m_windowBar.setMenuBar(menuBar)
        self.m_windowAgent.setHitTestVisible(menuBar, True)
        
    def titleBar(self):
        return self.m_windowBar
        
    def setWindowAttribute(self, key, value):
        self.m_windowAgent.setWindowAttribute(key, value)
        
    def getTheme(self):
        return self.m_currentTheme
