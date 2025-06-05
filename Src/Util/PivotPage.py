from Src.Import import *
from Src.Util import *


class PivotPage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.__initWidget()
        self.__initLayout()

    def __initWidget(self):
        self.pivot = Pivot()
        self.widgetDict = {}

        self.contentArea = ScrollArea(self)
        self.contentArea.setWidgetResizable(True)
        self.contentArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __initLayout(self):
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentArea)
        self.setLayout(self.vBoxLayout)

    def addSubInterface(self, widget, objName, text, icon=None):
        widget.setObjectName(objName)
        widget.setParent(None) # 防止 setWidget 删除旧组件
        self.widgetDict[objName] = widget
        self.pivot.addItem(
            icon=icon,
            routeKey=objName,
            text=text,
            onClick=lambda: self.setCurrentPage(objName)
        )

    def setCurrentPage(self, widget):
        self.setCurrentPage(self.widget.objectName())

    def setCurrentPage(self, objName):
        self.contentArea.takeWidget()
        self.pivot.setCurrentItem(objName)
        self.contentArea.setWidget(self.widgetDict[objName])
