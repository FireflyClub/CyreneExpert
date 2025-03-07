from src.head import *
from src.util import *


class InitUI:
    def initPivot(self, text):
        self.setObjectName(text)

        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName('scrollWidget')
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)

        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        StyleSheet.SETTING_INTERFACE.apply(self)

    def initPivotLayout(self, default):
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.stackedWidget.setCurrentWidget(default)
        self.pivot.setCurrentItem(default.objectName())
        self.setViewportMargins(20, 0, 20, 20)
        self.vBoxLayout.setContentsMargins(0, 10, 10, 0)
        qrouter.setDefaultRouteKey(self.stackedWidget, default.objectName())
        self.stackedWidget.currentChanged.connect(lambda index: InitUI.onCurrentIndexChanged(self, index))

    def addSubInterface(self, widget: QLabel, objName, text, icon=None):
        widget.setObjectName(objName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            icon=icon,
            routeKey=objName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index, needUpdate=False):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())
