@echo off
cd ../

rd /s /q CyreneExpert\
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q data\__pycache__\

python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/

pyinstaller -w -i ./data/image/icon.ico ./CyreneExpert.py -n CyreneExpert
xcopy /s /e /y dist\CyreneExpert\ CyreneExpert\
xcopy /s /e /y data\cmd\ CyreneExpert\data\cmd\
xcopy /s /e /y data\image\ CyreneExpert\data\image\
xcopy /s /e /y data\font\ CyreneExpert\data\font\
xcopy /s /e /y src\translate\ CyreneExpert\src\translate\

rd /s /q dist\
rd /s /q build\
del /f /q 0.3.1
del /f /q CyreneExpert.spec
rd /s /q __pycache__\
rd /s /q app\__pycache__\
rd /s /q data\module\__pycache__\

start ./CyreneExpert/CyreneExpert.exe