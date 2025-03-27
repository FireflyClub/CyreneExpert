import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTranslator
from qfluentwidgets import FluentTranslator
from Src.App.MainInterface import Main
from Src.Util.Config import CFG

if CFG.get(CFG.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(CFG.get(CFG.dpiScale))

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

locale = CFG.get(CFG.language).value
translator = FluentTranslator(locale)
localTranslator = QTranslator()
localTranslator.load(f"data\\translate\\{locale.name()}.qm")

app.installTranslator(translator)
app.installTranslator(localTranslator)

window = Main()
window.show()
sys.exit(app.exec())
