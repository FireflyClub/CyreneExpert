from src.head import *
from src.util import *


class Scene(QWidget):
    scene_id_signal = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.scene_search_line = SearchLineEdit(self)
        self.scene_search_line.setPlaceholderText(self.tr("搜索场景"))
        self.scene_search_line.setFixedHeight(35)

        self.scene_table = TableWidget(self)
        self.scene_table.setFixedSize(1140, 420)
        self.scene_table.setColumnCount(2)

        self.scene_table.setBorderVisible(True)
        self.scene_table.setBorderRadius(8)
        self.scene_table.setWordWrap(False)
        self.scene_table.verticalHeader().hide()
        self.scene_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.scene_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.scene_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.scene_layout = QVBoxLayout()
        self.scene_layout.addWidget(self.scene_search_line)
        self.scene_layout.addWidget(self.scene_table)
        self.setLayout(self.scene_layout)

    def __initInfo(self):
        self.handleSceneLoad()

    def __connectSignalToSlot(self):
        self.scene_search_line.textChanged.connect(self.handleSceneSearch)
        self.scene_table.cellClicked.connect(self.handleSceneSignal)

    def handleSceneSignal(self, row):
        item = self.scene_table.item(row, 1)
        scene_id = item.text()
        self.scene_id_signal.emit(scene_id)

    def handleSceneSearch(self):
        keyword = self.scene_search_line.text()
        for row in range(self.scene_table.rowCount()):
            item_1 = self.scene_table.item(row, 0)
            item_2 = self.scene_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.scene_table.setRowHidden(row, False)
            else:
                self.scene_table.setRowHidden(row, True)

    def handleSceneLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/scene.txt', 'r', encoding='utf-8') as file:
            scene = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.scene_table.setRowCount(len(scene))
        for i, line in enumerate(scene):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            scene[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.scene_table.setItem(i, j, QTableWidgetItem(part))
        self.scene_table.setHorizontalHeaderLabels([self.tr('场景描述'), 'ID'])