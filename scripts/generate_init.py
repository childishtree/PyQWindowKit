
import os
import sys
import logging

# Try to import dependencies for pyi generation
try:
    import PySide6
    import shiboken6
    from shibokensupport.signature.lib import pyi_generator
except ImportError as e:
    print(f"Warning: Could not import stub generator dependencies: {e}")
    pyi_generator = None

def create_init(package_dir, submodules):
    init_path = os.path.join(package_dir, "__init__.py")
    with open(init_path, "w") as f:
        f.write(f"# PyQWindowKit package\n")
        f.write("import os\n")
        f.write("import sys\n\n")
        
        f.write("__version__ = \"1.4.1\"\n")
        f.write("__version_info__ = (1, 4, 1, '', '')\n\n")

        # Add DLL directory for Windows
        f.write("if os.name == 'nt':\n")
        f.write("    package_dir = os.path.dirname(os.path.abspath(__file__))\n")
        f.write("    os.add_dll_directory(package_dir)\n\n")
        
        f.write("# Libraries required to import PyQWindowKit\n")  # DLL load failed while importing Quick: 找不到指定的模块。
        f.write("from PySide6.QtCore import QObject\n")    # QWKCore
        f.write("from PySide6.QtWidgets import QWidget\n")    # QWKWidgets
        f.write("from PySide6.QtQuick import QQuickItem, QQuickWindow\n")   # QWKQuick
        
        for mod in submodules:
            f.write(f"from . import {mod}\n")
            
    print(f"Generated {init_path}")

def generate_pyi(package_dir, module_name):
    if pyi_generator is None:
        print("Skipping pyi generation (dependencies missing)")
        return

    print(f"Generating stub for {module_name} in {package_dir}...")
    
    # Setup paths for DLL loading
    if os.name == 'nt':
        # Add package_dir to PATH
        os.environ["PATH"] = package_dir + os.pathsep + os.environ["PATH"]
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(package_dir)
            except OSError:
                pass
        
        # Also try to add shiboken6 directory to DLL path, as the module might depend on it
        if shiboken6 and hasattr(shiboken6, '__file__'):
            shiboken_dir = os.path.dirname(shiboken6.__file__)
            os.environ["PATH"] = shiboken_dir + os.pathsep + os.environ["PATH"]
            if hasattr(os, "add_dll_directory"):
                try:
                    os.add_dll_directory(shiboken_dir)
                except OSError:
                    pass
        
        # Also try to add PySide6 directory to DLL path
        if PySide6 and hasattr(PySide6, '__file__'):
            pyside6_dir = os.path.dirname(PySide6.__file__)
            os.environ["PATH"] = pyside6_dir + os.pathsep + os.environ["PATH"]
            if hasattr(os, "add_dll_directory"):
                try:
                    os.add_dll_directory(pyside6_dir)
                except OSError:
                    pass
    
    # Ensure we can import the module
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)

    # Mock options object expected by pyi_generator
    class Options:
        quiet = False
        verbose = 0
        feature = []
        sys_path = [package_dir]
        logger = logging.getLogger("stubgen")
        _pyside_call = True  # Mimic pyside6-genpyi behavior

    options = Options()
    
    try:
        # Call the internal generator function
        pyi_generator.generate_pyi(
            module_name,
            package_dir,
            options=options
        )
        print(f"Successfully generated stub for {module_name}")
    except Exception as e:
        print(f"Failed to generate stub for {module_name}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Usage: generate_init.py <install_root> <package_name> [modules...]
    if len(sys.argv) < 3:
        print("Usage: generate_init.py <install_root> <package_name> [modules...]")
        sys.exit(1)
        
    install_root = sys.argv[1]
    package_name = sys.argv[2]
    modules = sys.argv[3:]
    
    package_dir = os.path.join(install_root, package_name)
    if not os.path.exists(package_dir):
        print(f"Package directory does not exist: {package_dir}")
        os.makedirs(package_dir, exist_ok=True)
        
    create_init(package_dir, modules)
    
    for mod in modules:
        generate_pyi(package_dir, mod)
