
import sys
import os

# ================= Setup Start =================
# Add install dir to sys.path
install_dir = os.path.join(os.getcwd(), "out", "install", "x64-msvc-Release")
sys.path.append(install_dir)
# ================= Setup End =================

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PyQWindowKit import Quick

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    # Register QWindowKit types for QML
    # Note: In the C++ example, it's QWK::registerTypes(&engine). 
    # In Python binding, it should be exposed as Quick.registerTypes(engine)
    Quick.registerTypes(engine)
    
    # Load QML
    qml_content = b"""
    import QtQuick
    import QtQuick.Controls
    import QtQuick.Window
    import QWindowKit 1.0

    Window {
        id: window
        width: 800
        height: 600
        visible: false // Hide first to prevent flickering
        title: "PyQWindowKit Quick Demo"
        
        Component.onCompleted: {
            windowAgent.setup(window)
            window.visible = true
        }

        WindowAgent {
            id: windowAgent
        }

        Rectangle {
            anchors.fill: parent
            color: "#2b2b2b"
            
            Rectangle {
                id: titleBar
                height: 32
                width: parent.width
                color: "#3c3c3c"
                anchors.top: parent.top
                
                Text {
                    text: window.title
                    color: "white"
                    anchors.centerIn: parent
                }
                
                // Use WindowAgent's helper to make this area draggable
                TapHandler {
                    onTapped: if (eventPoint.device.pointerType === PointerDevice.Mouse) window.startSystemMove()
                }
                
                // Note: Real dragging usually requires WindowItemDelegate or setting title bar to agent
                // In pure QML usage of QWindowKit, we set the title bar like this:
                Component.onCompleted: windowAgent.setTitleBar(titleBar)
            }
            
            Text {
                text: "Hello from QML + PyQWindowKit!"
                color: "white"
                anchors.centerIn: parent
                font.pixelSize: 24
            }
            
            Button {
                text: "Close"
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottomMargin: 20
                onClicked: Qt.quit()
            }
        }
    }
    """
    
    qml_file = os.path.join(os.getcwd(), "temp_demo.qml")
    with open(qml_file, "wb") as f:
        f.write(qml_content)
        
    engine.load(QUrl.fromLocalFile(qml_file))
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    ret = app.exec()
    
    if os.path.exists(qml_file):
        os.remove(qml_file)
        
    sys.exit(ret)

