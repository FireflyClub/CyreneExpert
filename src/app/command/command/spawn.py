from src.head import *
from src.util import *


class Spawn(QWidget):
    monster_id_signal = Signal(str, str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.monster_num_label = SubtitleLabel(self.tr("数量:"), self)
        self.monster_num_edit = LineEdit(self)
        self.monster_num_edit.setPlaceholderText(self.tr("请输入怪物数量"))
        self.monster_num_edit.setValidator(QIntValidator(1, 99, self))

        self.monster_level_label = SubtitleLabel(self.tr("等级:"), self)
        self.monster_level_edit = LineEdit(self)
        self.monster_level_edit.setPlaceholderText(self.tr("请输入怪物等级"))
        self.monster_level_edit.setValidator(QIntValidator(1, 99, self))

        self.monster_round_label = SubtitleLabel(self.tr("半径:"), self)
        self.monster_round_edit = LineEdit(self)
        self.monster_round_edit.setPlaceholderText(self.tr("请输入仇恨半径"))
        self.monster_round_edit.setValidator(QIntValidator(1, 99, self))

        self.monster_search_line = SearchLineEdit(self)
        self.monster_search_line.setPlaceholderText(self.tr("搜索显示怪物"))
        self.monster_search_line.setFixedSize(455, 35)

        self.monster_table = TableWidget(self)
        self.monster_table.setFixedSize(455, 420)
        self.monster_table.setColumnCount(2)

        self.monster_table.setBorderVisible(True)
        self.monster_table.setBorderRadius(8)
        self.monster_table.setWordWrap(False)
        self.monster_table.verticalHeader().hide()
        self.monster_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.monster_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.monster_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.stage_search_line = SearchLineEdit(self)
        self.stage_search_line.setPlaceholderText(self.tr("搜索局内怪物"))
        self.stage_search_line.setFixedSize(455, 35)

        self.stage_table = TableWidget(self)
        self.stage_table.setFixedSize(455, 420)
        self.stage_table.setColumnCount(2)

        self.stage_table.setBorderVisible(True)
        self.stage_table.setBorderRadius(8)
        self.stage_table.setWordWrap(False)
        self.stage_table.verticalHeader().hide()
        self.stage_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stage_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.stage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.monster_layout = QVBoxLayout()
        self.monster_layout.addWidget(self.monster_search_line)
        self.monster_layout.addWidget(self.monster_table)
        self.stage_layout = QVBoxLayout()
        self.stage_layout.addWidget(self.stage_search_line)
        self.stage_layout.addWidget(self.stage_table)

        self.set_layout = QVBoxLayout()
        self.set_layout.addSpacing(70)
        self.set_layout.addWidget(self.monster_num_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_num_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.monster_level_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_level_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.monster_round_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.monster_round_edit)
        self.set_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.monster_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.stage_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.set_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.handleMonsterLoad()
        self.handleStageLoad()

    def __connectSignalToSlot(self):
        self.monster_search_line.textChanged.connect(self.handleMonsterSearch)
        self.monster_table.cellClicked.connect(self.handleSpawnSignal)
        self.stage_search_line.textChanged.connect(self.handleStageSearch)
        self.stage_table.cellClicked.connect(self.handleSpawnSignal)

        self.monster_num_edit.textChanged.connect(self.handleSpawnSignal)
        self.monster_level_edit.textChanged.connect(self.handleSpawnSignal)
        self.monster_round_edit.textChanged.connect(self.handleSpawnSignal)

    def handleSpawnSignal(self):
        selected_monster = self.monster_table.selectedItems()
        selected_stage = self.stage_table.selectedItems()
        if selected_monster and selected_stage:
            monster_id = selected_monster[1].text()
            stage_id = selected_stage[1].text()
            self.monster_id_signal.emit(monster_id, stage_id)

    def handleMonsterSearch(self):
        keyword = self.monster_search_line.text()
        for row in range(self.monster_table.rowCount()):
            item_1 = self.monster_table.item(row, 0)
            item_2 = self.monster_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.monster_table.setRowHidden(row, False)
            else:
                self.monster_table.setRowHidden(row, True)

    def handleStageSearch(self):
        keyword = self.stage_search_line.text()
        for row in range(self.stage_table.rowCount()):
            item_1 = self.stage_table.item(row, 0)
            item_2 = self.stage_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.stage_table.setRowHidden(row, False)
            else:
                self.stage_table.setRowHidden(row, True)

    def handleMonsterLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/monster.txt', 'r', encoding='utf-8') as file:
            monster = [line for line in file.readlines() if
                       not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.monster_table.setRowCount(len(monster))
        for i, line in enumerate(monster):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            monster[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.monster_table.setItem(i, j, QTableWidgetItem(part))
        self.monster_table.setHorizontalHeaderLabels([self.tr('显示怪物名称'), 'ID'])

    def handleStageLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/stage.txt', 'r', encoding='utf-8') as file:
            stage = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.stage_table.setRowCount(len(stage))
        for i, line in enumerate(stage):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            stage[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.stage_table.setItem(i, j, QTableWidgetItem(part))
        self.stage_table.setHorizontalHeaderLabels([self.tr('局内怪物名称'), 'ID'])
