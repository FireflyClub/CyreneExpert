from src.head import *
from src.util import *


class Give(QWidget):
    item_id_signal = Signal(str, int)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        self.give_search_line = SearchLineEdit(self)
        self.give_search_line.setPlaceholderText(self.tr("搜索物品"))
        self.give_search_line.setFixedSize(804, 35)
        self.give_combobox = ComboBox(self)
        self.give_combobox.setFixedSize(100, 35)
        self.give_combobox.addItems(
            [self.tr("角色"), self.tr("光锥"), self.tr("物品"), self.tr("食物"), self.tr("头像")])

        self.give_table = TableWidget(self)
        self.give_table.setFixedSize(915, 420)
        self.give_table.setColumnCount(2)
        self.give_table.setColumnWidth(0, 613)
        self.give_table.setColumnWidth(1, 300)

        self.give_table.setBorderVisible(True)
        self.give_table.setBorderRadius(8)
        self.give_table.setWordWrap(False)
        self.give_table.verticalHeader().hide()
        self.give_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.give_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.give_num_label = SubtitleLabel(self.tr("数量:"), self)
        self.give_num_edit = LineEdit(self)
        self.give_num_edit.setPlaceholderText(self.tr("请输入物品数量"))
        self.give_num_edit.setValidator(QIntValidator(self))

        self.give_level_label = SubtitleLabel(self.tr("等级:"), self)
        self.give_level_edit = LineEdit(self)
        self.give_level_edit.setPlaceholderText(self.tr("请输入等级"))
        self.give_level_edit.setValidator(QIntValidator(1, 99, self))

        self.give_eidolon_label = SubtitleLabel(self.tr("星魂/叠影:"), self)
        self.give_eidolon_edit = LineEdit(self)
        self.give_eidolon_edit.setPlaceholderText(self.tr("请输入星魂/叠影"))
        self.give_eidolon_edit.setValidator(QIntValidator(1, 9, self))

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.give_line_layout = QHBoxLayout()
        self.give_line_layout.addWidget(self.give_search_line)
        self.give_line_layout.addSpacing(5)
        self.give_line_layout.addWidget(self.give_combobox)
        self.give_layout = QVBoxLayout()
        self.give_layout.addLayout(self.give_line_layout)
        self.give_layout.addWidget(self.give_table)

        self.set_layout = QVBoxLayout()
        self.set_layout.addSpacing(70)
        self.set_layout.addWidget(self.give_num_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.give_num_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.give_level_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.give_level_edit)
        self.set_layout.addSpacing(20)
        self.set_layout.addWidget(self.give_eidolon_label)
        self.set_layout.addSpacing(5)
        self.set_layout.addWidget(self.give_eidolon_edit)
        self.set_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.give_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.set_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.handleAvatarLoad()

    def __connectSignalToSlot(self):
        self.give_search_line.textChanged.connect(self.handleGiveSearch)
        self.give_table.cellClicked.connect(self.handleGiveSignal)
        self.give_combobox.currentIndexChanged.connect(lambda index: self.handleGiveTypeChanged(index))

        self.give_num_edit.textChanged.connect(self.handleGiveSignal)
        self.give_level_edit.textChanged.connect(self.handleGiveSignal)
        self.give_eidolon_edit.textChanged.connect(self.handleGiveSignal)

    def handleGiveSignal(self):
        selected_items = self.give_table.selectedItems()
        index = self.give_combobox.currentIndex()
        if selected_items:
            item_id = selected_items[1].text()
            self.item_id_signal.emit(item_id, index)

    def handleGiveSearch(self):
        keyword = self.give_search_line.text()
        for row in range(self.give_table.rowCount()):
            item_1 = self.give_table.item(row, 0)
            item_2 = self.give_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.give_table.setRowHidden(row, False)
            else:
                self.give_table.setRowHidden(row, True)

    def handleGiveTypeChanged(self, index):
        interface = [
            self.handleAvatarLoad, self.handleLightconeLoad,
            self.handleItemLoad, self.handleFoodLoad, self.handleHeadLoad
        ]
        interface[index]()

    def handleAvatarLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/avatar.txt', 'r', encoding='utf-8') as file:
            avatar = [line for line in file.readlines() if
                      not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(avatar))
        for i, line in enumerate(avatar):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            avatar[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('角色名称'), 'ID'])

    def handleLightconeLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/lightcone.txt', 'r', encoding='utf-8') as file:
            lightcone = [line for line in file.readlines() if
                         not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(lightcone))
        for i, line in enumerate(lightcone):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            lightcone[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('光锥名称'), 'ID'])

    def handleItemLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/item.txt', 'r', encoding='utf-8') as file:
            item = [line for line in file.readlines() if
                    not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(item))
        for i, line in enumerate(item):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            item[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('物品名称'), 'ID'])

    def handleFoodLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/food.txt', 'r', encoding='utf-8') as file:
            food = [line for line in file.readlines() if
                    not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(food))
        for i, line in enumerate(food):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            food[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('食物名称'), 'ID'])

    def handleHeadLoad(self):
        with open(f'{cfg.ROOT}/data/cmd/{cfg.get(cfg.language).value.name()}/head.txt', 'r', encoding='utf-8') as file:
            head = [line for line in file.readlines() if
                    not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.give_table.setRowCount(len(head))
        for i, line in enumerate(head):
            line = line.strip()
            parts = line.split(' : ')
            parts[0], parts[1] = parts[1], parts[0]
            head[i] = ' : '.join(parts)
            for j, part in enumerate(parts):
                self.give_table.setItem(i, j, QTableWidgetItem(part))
        self.give_table.setHorizontalHeaderLabels([self.tr('头像名称'), 'ID'])
