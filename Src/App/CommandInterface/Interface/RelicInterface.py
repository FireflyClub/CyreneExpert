from Src.Import import *
from Src.Util import *


class Relic(ScrollArea):
    command_update = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)

        self.__initWidget()

    def __initWidget(self):
        # 遗器
        self.relic_search_line = SearchLineEdit(self)
        self.relic_search_line.setPlaceholderText(self.tr("搜索遗器"))
        self.relic_search_line.setFixedSize(258, 35)

        self.base_relic_button = TogglePushButton(self.tr("基础"), self)
        self.base_relic_button.setFixedSize(67, 35)
        self.custom_relic_button = TogglePushButton(self.tr("预设"), self)
        self.custom_relic_button.setFixedSize(67, 35)
        self.base_relic_button.setChecked(True)

        self.relic_type_button_group = QButtonGroup(self)
        self.relic_type_button_group.addButton(self.base_relic_button)
        self.relic_type_button_group.addButton(self.custom_relic_button)

        self.relic_table = TableWidget(self)
        self.relic_table.setColumnCount(4)
        self.relic_table.setFixedSize(405, 500)
        self.relic_table.setColumnWidth(0, 190)
        self.relic_table.setColumnWidth(1, 78)
        self.relic_table.setColumnWidth(2, 135)
        self.relic_table.setColumnWidth(3, 0)  # 隐藏command列

        self.relic_table.setBorderVisible(True)
        self.relic_table.setBorderRadius(8)
        self.relic_table.setWordWrap(False)
        self.relic_table.verticalHeader().hide()
        self.relic_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.relic_table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 词条
        self.entry_search_line = SearchLineEdit(self)
        self.entry_search_line.setPlaceholderText(self.tr("搜索词条"))
        self.entry_search_line.setFixedSize(160, 35)

        self.main_entry_button = TogglePushButton(self.tr("主词条"), self)
        self.side_entry_button = TogglePushButton(self.tr("副词条"), self)
        self.main_entry_button.setFixedSize(67, 35)
        self.side_entry_button.setFixedSize(67, 35)
        self.main_entry_button.setChecked(True)

        self.entry_type_button_group = QButtonGroup(self)
        self.entry_type_button_group.addButton(self.main_entry_button)
        self.entry_type_button_group.addButton(self.side_entry_button)

        self.entry_table = TableWidget(self)
        self.entry_table.setColumnCount(3)
        self.entry_table.setFixedSize(305, 500)
        self.entry_table.setColumnWidth(0, 148)
        self.entry_table.setColumnWidth(1, 80)
        self.entry_table.setColumnWidth(2, 75)

        self.entry_table.setBorderVisible(True)
        self.entry_table.setBorderRadius(8)
        self.entry_table.setWordWrap(False)
        self.entry_table.verticalHeader().hide()
        self.entry_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.entry_table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 当前信息
        self.main_now_label = SubtitleLabel(self.tr("当前主词条:"), self)
        self.main_now_edit = LineEdit(self)
        self.main_now_edit.setReadOnly(True)
        self.side_now_label = SubtitleLabel(self.tr("当前副词条:"), self)

        self.now_table = TableWidget(self)
        self.now_table.setColumnCount(2)
        self.now_table.setFixedSize(365, 160)

        self.now_table.setBorderVisible(True)
        self.now_table.setWordWrap(False)
        self.now_table.setBorderRadius(8)
        self.now_table.verticalHeader().hide()
        self.now_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.now_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.now_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.add_num_button = PrimaryToolButton(FluentIcon.ADD)
        self.add_num_button.setFixedSize(35, 35)
        self.minus_num_button = PrimaryToolButton(FluentIcon.REMOVE)
        self.minus_num_button.setFixedSize(35, 35)

        self.level_label = SubtitleLabel(self.tr("等级:"), self)
        self.level_edit = LineEdit(self)
        self.level_edit.setPlaceholderText(self.tr("请输入生成遗器的等级"))
        self.level_edit.setValidator(QIntValidator(1, 99, self))

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # 遗物
        self.relic_button_layout = QHBoxLayout()
        self.relic_button_layout.addWidget(self.relic_search_line)
        self.relic_button_layout.addWidget(self.base_relic_button)
        self.relic_button_layout.addWidget(self.custom_relic_button)

        self.relic_layout = QVBoxLayout()
        self.relic_layout.addLayout(self.relic_button_layout)
        self.relic_layout.addWidget(self.relic_table)

        # 词条
        self.entry_button_layout = QHBoxLayout()
        self.entry_button_layout.addWidget(self.entry_search_line)
        self.entry_button_layout.addWidget(self.main_entry_button)
        self.entry_button_layout.addWidget(self.side_entry_button)
        self.entry_layout = QVBoxLayout()
        self.entry_layout.addLayout(self.entry_button_layout)
        self.entry_layout.addWidget(self.entry_table)

        # 当前信息
        self.now_layout = QVBoxLayout()
        self.now_layout.addSpacing(15)
        self.now_layout.addWidget(self.main_now_label)
        self.now_layout.addSpacing(5)
        self.now_layout.addWidget(self.main_now_edit)
        self.now_layout.addSpacing(20)
        self.now_layout.addWidget(self.side_now_label)
        self.now_layout.addSpacing(5)
        self.now_layout.addWidget(self.now_table)
        self.now_layout.addSpacing(14)

        self.now_tool_layout = QHBoxLayout()
        self.now_tool_layout.addStretch(1)
        self.now_tool_layout.addWidget(self.add_num_button)
        self.now_tool_layout.addSpacing(5)
        self.now_tool_layout.addWidget(self.minus_num_button)
        self.now_tool_layout.addSpacing(12)

        self.now_layout.addLayout(self.now_tool_layout)
        self.now_layout.addSpacing(15)
        self.now_layout.addWidget(self.level_label)
        self.now_layout.addSpacing(5)
        self.now_layout.addWidget(self.level_edit)
        self.now_layout.addStretch(1)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.relic_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.entry_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.now_layout)
        self.setLayout(self.main_layout)

    def __initInfo(self):
        self.now_list = {}
        self.handleRelicTypeChanged()
        self.handleEntryLoad()
        self.handleNowLoad()

    def __connectSignalToSlot(self):
        self.relic_search_line.textChanged.connect(self.handleRelicSearch)
        self.base_relic_button.clicked.connect(self.handleRelicTypeChanged)
        self.custom_relic_button.clicked.connect(self.handleRelicTypeChanged)
        self.relic_table.cellClicked.connect(self.handleRelicTableClicked)

        self.entry_search_line.textChanged.connect(self.handleEntrySearch)
        self.main_entry_button.clicked.connect(self.handleEntryTypeChanged)
        self.side_entry_button.clicked.connect(self.handleEntryTypeChanged)
        self.entry_table.cellClicked.connect(self.handleEntryTableClicked)
        self.entry_table.cellDoubleClicked.connect(self.handleAddSideClicked)

        self.now_table.cellDoubleClicked.connect(lambda: self.handleEntryNumChanged('delete'))
        self.add_num_button.clicked.connect(lambda: self.handleEntryNumChanged('add'))
        self.minus_num_button.clicked.connect(lambda: self.handleEntryNumChanged('remove'))

        self.main_now_edit.textChanged.connect(self.handleRelicSignal)
        self.level_edit.textChanged.connect(self.handleRelicSignal)

    # 信号
    def handleRelicSignal(self):
        selected_items = self.relic_table.selectedItems()
        if selected_items:
            if self.base_relic_button.isChecked():
                relic_id = selected_items[2].text()
                relic_level = self.level_edit.text()
                main_entry_name = self.main_now_edit.text()
                now_list_nozero = {k: v for k, v in self.now_list.items() if v > 0}

                command = '/give ' + relic_id
                if relic_level != '':
                    command += ' lv' + relic_level

                if main_entry_name != '':
                    entry_index = 0
                    for i in range(self.entry_table.rowCount()):
                        if self.entry_table.item(i, 0).text() == main_entry_name and self.entry_table.item(i, 1).text() != self.tr(
                                '通用'):
                            entry_index = i
                            break
                    main_entry = self.entry_table.item(entry_index, 2).text()
                    command += ' s' + main_entry

                for entry_name, entry_num in now_list_nozero.items():
                    if entry_name != '':
                        entry_index = 0
                        for i in range(self.entry_table.rowCount()):
                            if self.entry_table.item(i, 0).text() == entry_name and self.entry_table.item(i, 1).text() == self.tr('通用'):
                                entry_index = i
                                break
                        side_entry = self.entry_table.item(entry_index, 2).text()
                        command += ' ' + side_entry + ':' + str(entry_num)

                self.command_update.emit(command)
            elif self.custom_relic_button.isChecked():
                command = selected_items[3].text()
                self.command_update.emit(command)

    # 条件更新时切换显示状态相关
    def handleRelicSearch(self):
        keyword = self.relic_search_line.text()
        for row in range(self.relic_table.rowCount()):
            item_1 = self.relic_table.item(row, 0)
            item_2 = self.relic_table.item(row, 1)
            item_3 = self.relic_table.item(row, 2)
            iskeyword_1 = item_1 and item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2 and item_2.text().lower().find(keyword.lower()) != -1
            iskeyword_3 = item_3 and item_3.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2 or iskeyword_3:
                self.relic_table.setRowHidden(row, False)
            else:
                self.relic_table.setRowHidden(row, True)

    def handleEntrySearch(self):
        keyword = self.entry_search_line.text()
        for row in range(self.entry_table.rowCount()):
            item = self.entry_table.item(row, 0)
            if item.text().lower().find(keyword.lower()) != -1:
                self.entry_table.setRowHidden(row, False)
            else:
                self.entry_table.setRowHidden(row, True)

    def handleRelicTypeChanged(self):
        self.relic_search_line.clear()
        self.relic_table.setRowCount(0)
        self.entry_table.setRowCount(0)
        self.now_table.setRowCount(0)

        selected_base_relic = self.base_relic_button.isChecked()
        if selected_base_relic:
            self.handleBaseRelicLoad()
            self.handleEntryLoad()
            self.handleNowLoad()
        else:
            self.entry_table.setRowCount(0)
            self.now_table.setRowCount(0)
            self.handleCustomRelicLoad()

        layouts = [self.entry_layout, self.entry_button_layout, self.now_layout, self.now_tool_layout]
        for layout in layouts:
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget is not None:
                    if selected_base_relic:
                        widget.setDisabled(False)
                    else:
                        widget.setDisabled(True)

    def handleEntryTypeChanged(self):
        self.entry_search_line.clear()
        selected_main_entry = self.main_entry_button.isChecked()
        for row in range(self.entry_table.rowCount()):
            entry_type = self.entry_table.item(row, 1).text()
            if selected_main_entry:
                if entry_type == self.tr('通用'):
                    self.entry_table.setRowHidden(row, True)
                else:
                    self.entry_table.setRowHidden(row, False)
                self.__handleRelatedEntryUpdate()
            else:
                if entry_type == self.tr('通用'):
                    self.entry_table.setRowHidden(row, False)
                else:
                    self.entry_table.setRowHidden(row, True)

    # 信息更新行为相关
    def handleRelicTableClicked(self):
        self.handleRelicSignal()
        self.__handleRelatedEntryUpdate()
        if self.base_relic_button.isChecked():
            self.main_now_edit.clear()

    def handleEntryTableClicked(self):
        selected_entry = self.entry_table.selectedItems()
        selected_entry_type = self.entry_table.item(self.entry_table.currentRow(), 1).text()
        if selected_entry and selected_entry_type != self.tr('通用'):
            self.main_now_edit.setText(selected_entry[0].text())
            self.side_entry_button.setChecked(True)
            self.handleEntryTypeChanged()

    def handleAddSideClicked(self):
        selected_side_entry = self.side_entry_button.isChecked()
        if selected_side_entry:
            selected_entry = self.entry_table.selectedItems()
            selected_entry_type = self.entry_table.item(self.entry_table.currentRow(), 1).text()
            entry_id = selected_entry[0].text()
            if selected_entry and selected_entry_type == self.tr('通用') and len(
                    self.now_list) < 4 and entry_id not in self.now_list:
                self.now_list[entry_id] = 1
                self.handleNowLoad()
            self.handleRelicSignal()

    def handleEntryNumChanged(self, types):
        selected_now = self.now_table.selectedItems()
        if selected_now:
            entry_name = selected_now[0].text()
            if types == 'add':
                if self.now_list[entry_name] < 6:
                    self.now_list[entry_name] += 1
            elif types == 'remove':
                if self.now_list[entry_name] > 0:
                    self.now_list[entry_name] -= 1
            elif types == 'delete':
                del self.now_list[entry_name]

            selected_row = self.now_table.currentRow()
            self.handleNowLoad()
            self.now_table.selectRow(selected_row)
            self.handleRelicSignal()

    # 读取和加载页面信息相关
    def handleBaseRelicLoad(self):
        with open(f'{CFG.ROOT}/Data/Cmd/{CFG.get(CFG.language).value.name()}/relic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            line = line.strip()
            parts = line.split(" : ")
            parts[0], parts[1], parts[2] = parts[1], parts[2], parts[0]
            relic[i] = ' : '.join(parts)
            self.relic_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels([self.tr('遗器名称'), self.tr('部位'), 'ID'])

    def handleCustomRelicLoad(self):
        with open(f'{CFG.ROOT}/Data/Cmd/{CFG.get(CFG.language).value.name()}/myrelic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.relic_table.setRowCount(len(relic))
        for i, line in enumerate(relic):
            line = line.strip()
            parts = line.split(' : ')
            self.relic_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.relic_table.setItem(i, j, QTableWidgetItem(part))
        self.relic_table.setHorizontalHeaderLabels(
            [self.tr('遗器名称'), self.tr('部位'), self.tr('适用角色'), 'command'])

    def handleEntryLoad(self):
        with open(f'{CFG.ROOT}/Data/Cmd/{CFG.get(CFG.language).value.name()}/entry.txt', 'r', encoding='utf-8') as file:
            entry = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
        self.entry_table.setRowCount(len(entry))
        for i, line in enumerate(entry):
            parts = line.split()
            self.entry_table.setRowHeight(i, 39)
            for j, part in enumerate(parts):
                self.entry_table.setItem(i, j, QTableWidgetItem(part))
        self.entry_table.setHorizontalHeaderLabels([self.tr('词条名称'), self.tr('部位'), 'ID'])

    def handleNowLoad(self):
        self.now_table.clearContents()
        self.now_table.setRowCount(len(self.now_list))
        for row, (key, value) in enumerate(self.now_list.items()):
            self.now_table.setRowHeight(row, 30)
            self.now_table.setItem(row, 0, QTableWidgetItem(key))
            self.now_table.setItem(row, 1, QTableWidgetItem(str(value)))
        self.now_table.setHorizontalHeaderLabels([self.tr('词条名称'), self.tr('数量')])

    # 遗器条件更新时，更新对应词条
    def __handleRelatedEntryUpdate(self):
        selected_relic = self.relic_table.selectedItems()
        if selected_relic and self.base_relic_button.isChecked():
            self.main_entry_button.setChecked(True)
            relic_type = selected_relic[1].text()
            for row in range(self.entry_table.rowCount()):
                if self.entry_table.item(row, 1).text() == relic_type:
                    self.entry_table.setRowHidden(row, False)
                else:
                    self.entry_table.setRowHidden(row, True)
            self.handleEntryLoad()
