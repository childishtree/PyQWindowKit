# PyQWindowKit 演示项目

此仓库包含一个演示，展示了如何使用 Shiboken6 为 QWindowKit 生成 Python 绑定，并包含一个基于 Python 的 Gallery 应用程序，用于展示该库的功能。

## 项目概述

该项目主要由两部分组成：
1.  **绑定生成**：使用 CMake 和 Shiboken6 为 QWindowKit C++ 库生成 Python 绑定。
2.  **Gallery 演示程序**：一个纯 Python 应用程序（位于 `gallery/` 目录下），利用生成的绑定创建一个现代化的、支持原生系统效果（如 Mica、Acrylic 等）的无边框窗口应用程序。

## 先决条件

*   **CMake**：3.20 或更高版本
*   **Qt**：6.x （需与您的 PySide6 版本匹配）
*   **Python**：3.8 或更高版本
*   **依赖包**：
    *   `shiboken6`
    *   `PySide6`
    *   `shiboken6_generator`（支持 `shiboken_generator_create_binding` 的 CMake 函数）

> 全程使用 Release（发布）版本进行构建与安装。

## 项目结构
*   `CMakeLists.txt`：主要的 CMake 构建配置文件。
*   `pyproject.toml`：用于定义 Python 包的构建系统要求。
*   `test_quick.py`：用于测试 QWK::Quick 绑定的简单脚本。
*   `test_widgets.py`：用于测试 QWK::Widgets 绑定的简单脚本。
*   `test_core.py`：用于测试 QWK::Core 绑定的简单脚本。
*   `verify_build.py`：验证 PyQWindowKit 是否构建成功。
*   `bindings/`：用于 Shiboken 的 XML 类型系统文件。
*   `scripts/`：用于绑定生成的辅助脚本。
*   `gallery/`：使用 PyQWindowKit 库的 Python 示例应用程序。

## 快速上手
> Windows 平台下使用 Visual Studio 2022开发。
> 确保Qt版本和已安装PySide6等的版本一致。

1. 在根目录下打开命令行工具，输入`.\setup_venv.ps1` 创建虚拟环境并安装所需的软件包。（输入`.\activate_venv.ps1` 激活虚拟环境。）
2. 修改 `CMakeSettings.json` 文件中的 Qt 安装路径 和 QWindowKit 安装路径 `DQWK_DIR` 和 Python 解释器 `PYTHON_EXECUTABLE` 的路径。
3. 使用Visual Studio 2022 打开根目录下的CMakeLists.txt 文件，选择 Release 版本进行构建和安装。
4. 运行 `test_quick.py`、`test_widgets.py`、`test_core.py` 脚本以测试绑定是否正确工作。 
5. 修改 `pyproject.toml` 中的 `cmake.args` 参数，与步骤二一致。
6. 在命令行中输入 `pip install .` 将PyQWindowKit 打包为 Python Wheel(安装到虚拟环境)。
7. 在命令行中运行 `python gallery/main.py` 以启动 Gallery 示例应用程序。

---

## 前期准备

### 创建 Python 虚拟环境并安装依赖包
使用命令 `python -m venv <venv_name>` 来创建一个新的虚拟环境。使用 `./<venv_name>/Scripts/activate`（在 Windows 上）或 `source <venv_name>/bin/activate`（在 macOS/Linux 上）激活后，安装依赖包。

您可以通过 pip 安装 Python 依赖包：
```bash
pip install shiboken6 PySide6 shiboken6_generator
```
或从 Qt 官网安装最新的 Python 依赖包：
```bash
pip install --index-url=https://download.qt.io/official_releases/QtForPython/ --trusted-host download.qt.io shiboken6 pyside6 shiboken6_generator
```

### QWindowKit 库的构建与安装
在生成绑定之前，您需要先构建并安装 QWindowKit 库。请参考 https://github.com/stdware/qwindowkit 。

执行以下命令以构建和安装 QWindowKit：
```bash
git clone --recursive https://github.com/stdware/qwindowkit
cd qwindowkit
cmake -B build -S . -DCMAKE_PREFIX_PATH="<QT_INSTALL_DIR>" \
                    -DQWINDOWKIT_BUILD_QUICK=TRUE \           # 可选
                    -DCMAKE_INSTALL_PREFIX="<QWINDOWKIT_INSTALL_DIR>" \
                    -G "Ninja Multi-Config"
cmake --build build --target install --config Release
```
- 使用 `-DCMAKE_PREFIX_PATH` 指定您的 Qt 安装路径。
- 使用 `-DQWINDOWKIT_BUILD_QUICK=TRUE` 启用 QWindowKit 的 Quick 模块构建。
- 使用 `-DCMAKE_INSTALL_PREFIX` 指定 QWindowKit 的安装路径。

> **注意**：请安装 Release 版本的 QWindowKit，以确保与绑定生成过程兼容（PySide6 及 Shiboken6 包都是使用的 Release 版本）。

## PyQWindowKit 库的配置、构建与安装

执行以下命令以构建 PyQWindowKit 绑定：
```bash
# 配置
cmake -S . -B build -G "Ninja" -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_PREFIX_PATH="<QT_INSTALL_DIR>" \
         -DQWK_DIR="<QWINDOWKIT_INSTALL_DIR>" \
         -DPython_EXECUTABLE="<PATH_TO_YOUR_PYTHON_EXECUTABLE>"
# 构建
cmake --build build --config Release
```
> *注意：请确保 `cmake` 能够找到您的 Python 环境、Qt 和 QWindowKit 的安装路径。*

如果在虚拟环境下执行 `cmake`，就无需指定 `-DPython_EXECUTABLE` 参数。如果没有在虚拟环境下，也没有指定 Python 解释器路径，会默认使用系统下的 Python 解释器。
QWindowKit 默认安装在 `./install` 路径下。如果 QWindowKit 安装在其他位置，请使用 `-DQWK_DIR` 参数指定其安装位置。

执行以下命令安装 PyQWindowKit 库：
```bash
# 安装
cmake --install build --prefix <OUT_INSTALL_DIR> --config Release
```

## 测试
`test_quick.py`、`test_widgets.py`、`test_core.py` 是分别用于测试 QWK::Quick、QWK::Widgets 和 QWK::Core 绑定的简单脚本。您可以运行这些脚本以验证绑定是否正确工作。例如：
```bash
python test_quick.py
```
> 请注意：`install_dir` 应替换为您在安装 PyQWindowKit 时指定的路径 `<OUT_INSTALL_DIR>`。

## 将 PyQWindowKit 打包为 Python Wheel
使用以下命令将 PyQWindowKit 打包为 Python Wheel：
```bash
pip install .
```

## 运行 Python Gallery

`gallery/` 目录包含一个 QWindowKit Gallery 示例的 Python 移植版本。它演示了以下功能：
*   无边框窗口的实现。
*   带有系统按钮的自定义标题栏。
*   在 Windows 上使用原生窗口效果（Mica、Acrylic、DWM 模糊）。
*   主题切换（深色/浅色）。

### 如何运行

1.  确保您已成功构建绑定。
2.  设置 `PYTHONPATH` 环境变量，使其包含生成 `PyQWindowKit` 模块的目录（通常在您的构建输出目录中，例如 `build/`）。
3.  运行主脚本：

```bash
# 示例（请根据实际情况调整路径）
# 在 Windows (PowerShell) 上
$env:PYTHONPATH = "path\to\build\output;$env:PYTHONPATH"
python gallery\main.py

# 在 macOS/Linux 上
export PYTHONPATH="path/to/build/output:$PYTHONPATH"
python gallery/main.py
```

![gallery](./doc/gallery.png)

## 功能特性

*   **跨平台支持**：设计可在 Windows、macOS 和 Linux 上运行（尽管某些效果是 Windows 特有的）。
*   **原生集成**：使用 QWindowKit 与原生窗口系统 API 进行交互。
*   **高度可定制**：通过 Python 完全控制标题栏和窗口行为。

## 感谢
感谢以下开源项目的帮助：
- https://github.com/Darcy-C/Shiboken6Demo
- https://github.com/ozguronsoy/SimpleMapView/tree/main
- https://github.com/refeyn/QuickGraphLib/tree/master
