python -m venv .venv
./activate_venv.ps1
pip install --index-url=https://download.qt.io/official_releases/QtForPython/ --trusted-host download.qt.io shiboken6 pyside6 shiboken6_generator
# pip install --no-build-isolation --config-settings=editable.rebuild=true --config-settings=build-dir=build -v -e .