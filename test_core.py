
import sys
import os

# ================= Setup Start =================
# Add install dir to sys.path
install_dir = os.path.join(os.getcwd(), "out", "install", "x64-msvc-Release")
sys.path.append(install_dir)
# ================= Setup End =================

from PySide6.QtCore import QCoreApplication, QTimer
import PyQWindowKit

def test_core_features():
    print("-" * 20)
    print("Testing Core Features...")
    
    # 1. Test Core Module Import
    try:
        from PyQWindowKit import Core
        print("[PASS] Core module imported.")
    except ImportError as e:
        print(f"[FAIL] Core module import failed: {e}")
        return

    # 2. Test StyleAgent and SystemTheme
    if hasattr(Core, "StyleAgent"):
        print("[PASS] StyleAgent found in Core.")
        if hasattr(Core.StyleAgent, "SystemTheme"):
            print("[PASS] StyleAgent.SystemTheme found.")
            try:
                # Access an enum value to verify
                print(f"       SystemTheme.Dark = {Core.StyleAgent.SystemTheme.Dark}")
            except AttributeError:
                print("       [WARN] SystemTheme.Dark not found (check enum values).")
        else:
            print("[FAIL] StyleAgent.SystemTheme NOT found.")
    else:
        print("[FAIL] StyleAgent NOT found in Core.")

    # 3. Test WindowAgentBase and SystemButton
    if hasattr(Core, "WindowAgentBase"):
        print("[PASS] WindowAgentBase found in Core.")
        if hasattr(Core.WindowAgentBase, "SystemButton"):
            print("[PASS] WindowAgentBase.SystemButton found.")
            try:
                print(f"       SystemButton.Close = {Core.WindowAgentBase.SystemButton.Close}")
            except AttributeError:
                 print("       [WARN] SystemButton.Close not found.")
        else:
            print("[FAIL] WindowAgentBase.SystemButton NOT found.")
    else:
        print("[FAIL] WindowAgentBase NOT found in Core.")
        
    print("-" * 20)

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    
    print(f"PyQWindowKit Package File: {PyQWindowKit.__file__}")
    
    test_core_features()
    
    print("PyQWindowKit Core Test - Finished")
    
    QTimer.singleShot(0, app.quit)
    sys.exit(app.exec())
