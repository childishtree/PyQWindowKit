# =========================================================
#
# CMake configuration for PyQWindowKit
# This project is used to generate Python bindings for the QWindowKit library using Shiboken6.
# 前置条件: - 必需激活Python虚拟环境，并安装以下依赖：
#               pip install shiboken6_generator PySide6 shiboken6
#          - 必需使用release或其他非debug配置进行构建
#          - QWindowKit已构建并安装在项目的install目录中
# =========================================================

cmake_minimum_required(VERSION 3.20)

project(PyQWindowKit)

# =================== No DEBUG Model ===========================
string(TOUPPER "${CMAKE_BUILD_TYPE}" BUILD_TYPE_UPPER)
string(TOUPPER "${CMAKE_CONFIGURATION_TYPES}" CONFIG_TYPES_UPPER)

# Only prohibit Debug if it is explicitly selected as CMAKE_BUILD_TYPE
if(CMAKE_BUILD_TYPE AND BUILD_TYPE_UPPER STREQUAL "DEBUG")
    message(FATAL_ERROR "[ERROR] Debug build is prohibited! Please build with Release/RelWithDebInfo or other non-Debug configurations.")
endif()

# ========= 0. Setup Python Venv  ============
# Try to detect active virtual environment
if(NOT Python_EXECUTABLE AND DEFINED ENV{VIRTUAL_ENV})
    if(WIN32)
        set(Python_EXECUTABLE "$ENV{VIRTUAL_ENV}/Scripts/python.exe")
    else()
        set(Python_EXECUTABLE "$ENV{VIRTUAL_ENV}/bin/python")
    endif()
endif()

# ====================== 1. Find Qt6 ======================
find_package(Qt6 COMPONENTS Core Gui Widgets Quick REQUIRED)
set(QT_COMPONENTS Core Gui Widgets)     # 可选Quick

# ====================== 2. Find QWindowKit ======================
set(QWK_DIR "${CMAKE_CURRENT_SOURCE_DIR}/install" CACHE PATH "Path to QWindowKit installation directory")
list(APPEND CMAKE_PREFIX_PATH "${QWK_DIR}")
set(QWK_BUILD_QUICK TRUE)
set(QWK_COMPONENTS Core Widgets)

if(QWK_BUILD_QUICK)
    list(APPEND QWK_COMPONENTS Quick)
    list(APPEND QT_COMPONENTS Quick Network OpenGL Qml)
endif()

find_package(QWindowKit COMPONENTS Core Widgets REQUIRED)

# ====================== 3. Python/Shiboken6 ======================
find_package(Python COMPONENTS Interpreter Development REQUIRED)
execute_process(
    COMMAND ${Python_EXECUTABLE} -c 
    # "import site; print(next(p for p in site.getsitepackages() if 'site-packages' in p))"
    # OUTPUT_VARIABLE Python_SITELIB
    "import os, shiboken6_generator; print(os.path.dirname(shiboken6_generator.__file__), end='')"
    OUTPUT_VARIABLE SHIBOKEN6_GENERATOR_DIR
    RESULT_VARIABLE SHIBOKEN6_GENERATOR_FOUND
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(NOT "${SHIBOKEN6_GENERATOR_FOUND}" EQUAL "0")
    message(FATAL_ERROR "Could not find 'shiboken6_generator'. Run: pip install shiboken6_generator")
endif()

execute_process(
    COMMAND "${Python_EXECUTABLE}" -c 
    "import os, PySide6; print(os.path.dirname(PySide6.__file__), end='')"
    OUTPUT_VARIABLE PYSIDE6_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

file(TO_CMAKE_PATH "${SHIBOKEN6_GENERATOR_DIR}" SHIBOKEN6_GENERATOR_DIR)
file(TO_CMAKE_PATH "${PYSIDE6_DIR}" PYSIDE6_DIR)
list(APPEND CMAKE_PREFIX_PATH "${SHIBOKEN6_GENERATOR_DIR}" "${PYSIDE6_DIR}")
find_package(Shiboken6Tools REQUIRED)

# list(APPEND CMAKE_PREFIX_PATH "${Python_SITELIB}/shiboken6_generator/lib/cmake")
# find_package(Shiboken6Tools REQUIRED)


# ====================== 4. Create Bindings ======================
include(scripts/CreateBinding.cmake)

# Bindings Configuration
set(packahe_name "PyQWindowKit")

set(SHIBOKEN_EXTRA_OPTIONS "")
get_target_property(QWK_CORE_INCLUDE_DIRS QWindowKit::Core INTERFACE_INCLUDE_DIRECTORIES)
foreach(dir ${QWK_CORE_INCLUDE_DIRS})
    list(APPEND SHIBOKEN_EXTRA_OPTIONS "-I${dir}")
endforeach()


## QWindowKit Core Binding
set(typesystem_file_core ${CMAKE_SOURCE_DIR}/bindings/bindings_core.xml)

# Dynamically generate source list from XML
execute_process(
    COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/get_generated_sources.py"
            "${typesystem_file_core}"
            "${CMAKE_CURRENT_BINARY_DIR}/Core"
    OUTPUT_VARIABLE generated_sources_core
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Generate Bindings
create_qwk_binding(
        TARGET "Core"
        ORIGIN_LIB "QWindowKit::Core"
        HEADER "${CMAKE_SOURCE_DIR}/bindings/bindings_core.h"
        TYPESYSTEM "${typesystem_file_core}"
        SOURCES ${generated_sources_core}
        QT_MODULES ${QT_COMPONENTS}
        INSTALL_DIR "${packahe_name}"
        EXTRA_INCLUDES ${SHIBOKEN_EXTRA_OPTIONS}
    )

## QWindowKit Widgets Binding
set(typesystem_file_widgets ${CMAKE_SOURCE_DIR}/bindings/bindings_widgets.xml)

# Dynamically generate source list from XML
execute_process(
    COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/get_generated_sources.py"
            "${typesystem_file_widgets}"
            "${CMAKE_CURRENT_BINARY_DIR}/Widgets"
    OUTPUT_VARIABLE generated_sources_widgets
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Generate Bindings
create_qwk_binding(
        TARGET "Widgets"
        ORIGIN_LIB "QWindowKit::Widgets"
        HEADER "${CMAKE_SOURCE_DIR}/bindings/bindings_widgets.h"
        TYPESYSTEM "${typesystem_file_widgets}"
        SOURCES ${generated_sources_widgets}
        QT_MODULES ${QT_COMPONENTS}
        INSTALL_DIR "${packahe_name}"
        EXTRA_INCLUDES ${SHIBOKEN_EXTRA_OPTIONS}
    )

if(QWK_BUILD_QUICK)
    set(typesystem_file_quick ${CMAKE_SOURCE_DIR}/bindings/bindings_quick.xml)
    
    # Dynamically generate source list from XML
    execute_process(
        COMMAND "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/get_generated_sources.py"
                "${typesystem_file_quick}"
                "${CMAKE_CURRENT_BINARY_DIR}/Quick"
        OUTPUT_VARIABLE generated_sources_quick
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    
    create_qwk_binding(
        TARGET "Quick"
        ORIGIN_LIB "QWindowKit::Quick"
        HEADER "${CMAKE_SOURCE_DIR}/bindings/bindings_quick.h"
        TYPESYSTEM "${typesystem_file_quick}"
        SOURCES ${generated_sources_quick}
        QT_MODULES ${QT_COMPONENTS}
        INSTALL_DIR "${packahe_name}"
        EXTRA_INCLUDES ${SHIBOKEN_EXTRA_OPTIONS}
    )
endif()


# ====================== 5. Install ======================
# 1. Install PyQWindowKit package files(.pyd) by cmake `create_qwk_binding` function
# 2. Install QWindowKit dependency DLLs (Release versions only)
foreach(component ${QWK_COMPONENTS})
    set(target_name "QWindowKit::${component}")
    get_target_property(dll_path ${target_name} IMPORTED_LOCATION_RELEASE)
    
    if(dll_path)
        install(FILES "${dll_path}" DESTINATION ${packahe_name})
    else()
        message(WARNING "Could not find Release DLL for ${target_name}")
    endif()
endforeach()


# 执行python脚本，生成xxx.pyi和__init__.py文件
set(MODULE_ARGS "\"Core\"")
set(MODULE_ARGS "${MODULE_ARGS} \"Widgets\"")
if(QWK_BUILD_QUICK)
    set(MODULE_ARGS "${MODULE_ARGS} \"Quick\"")
endif()

install(CODE "
    execute_process(
        COMMAND \"${Python_EXECUTABLE}\" \"${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_init.py\"
        \"\${CMAKE_INSTALL_PREFIX}\" \"${packahe_name}\" ${MODULE_ARGS}
    )
")

