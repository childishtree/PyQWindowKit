
import sys
import os

# 1. 自动定位生成的 PyQWindowKit 包
# 假设脚本在项目根目录运行，我们添加 install 输出目录到 sys.path
install_dir = os.path.join(os.getcwd(), "out", "install", "x64-msvc-Release")

if os.path.exists(install_dir):
    print(f"Adding install dir to sys.path: {install_dir}")
    sys.path.append(install_dir)
else:
    print(f"Warning: Install dir not found: {install_dir}")
    # Fallback logic if needed...

try:
    # 2. 尝试导入模块
    # 由于我们在 __init__.py 中已经处理了 DLL 路径，这里应该可以直接导入
    import PyQWindowKit
    print("Successfully imported PyQWindowKit package!")
    print(f"Package file: {PyQWindowKit.__file__}")
    
    # 3. 检查子模块
    try:
        from PyQWindowKit import Core
        print("Successfully imported PyQWindowKit.Core!")
        print("Core contents:", dir(Core))
    except ImportError as e:
        print(f"Failed to import Core: {e}")
    try:
        from PyQWindowKit import Widgets
        print("Successfully imported PyQWindowKit.Widgets!")
        print("Widgets contents:", dir(Widgets))
    except ImportError as e:
        print(f"Failed to import Widgets: {e}")

    try:
        from PyQWindowKit import Quick
        print("Successfully imported PyQWindowKit.Quick!")
        print("Quick contents:", dir(Quick))
    except ImportError as e:
        print(f"Failed to import Quick: {e}")
    
except ImportError as e:
    print(f"ImportError: {e}")
    print("\nPossible reasons:")
    print("1. Dependency DLLs are missing.")
    print("2. The install directory is not in sys.path.")

