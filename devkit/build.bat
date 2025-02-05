@echo off
cd ../

rd /s /q Firefly-Launcher\
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q src\component\__pycache__\
rd /s /q src\module\__pycache__\

python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/

pyinstaller -w -i ./src/image/icon.ico ./firefly-launcher.py -n Firefly-Launcher
xcopy /s /e /y dist\Firefly-Launcher\ Firefly-Launcher\
xcopy /s /e /y src\qss\ Firefly-Launcher\src\qss\
xcopy /s /e /y src\image\ Firefly-Launcher\src\image\
xcopy /s /e /y src\patch\ Firefly-Launcher\src\patch\
xcopy /s /e /y src\data\ Firefly-Launcher\src\data\
xcopy /s /e /y src\translate\ Firefly-Launcher\src\translate\

rd /s /q dist\
rd /s /q build\
del /f /q 0.3.1
del /f /q Firefly-Launcher.spec
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q src\component\__pycache__\
rd /s /q src\module\__pycache__\

start ./Firefly-Launcher/Firefly-Launcher.exe