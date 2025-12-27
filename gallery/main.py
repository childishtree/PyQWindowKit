import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication, qVersion

from framelesswindow import FramelessWindow



def main():
    # 启用高DPI缩放，让界面元素根据屏幕缩放因子自动调整
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # 启用高DPI像素图，确保图标等图片资源在高分屏下清晰显示
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    # 对于较高版本的Qt（PySide6对应Qt6），设置高DPI缩放因子舍入策略
    # 获取当前Qt版本字符串，并转换为元组便于比较
    current_qt_version = tuple(map(int, qVersion().split('.')))
    if current_qt_version >= (6, 2, 0):
        # 设置缩放因子舍入策略为直接传递（PassThrough），避免系统缩放因子被舍入到整数
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    app = QApplication(sys.argv)

    w = FramelessWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
