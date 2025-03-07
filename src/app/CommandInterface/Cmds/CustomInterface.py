from src.head import *
from src.util import *


class Custom(QWidget):
    command_update = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        self.parent = parent

        self.__initWidget()

    def __initWidget(self):
        self.mycommand_search_line = SearchLineEdit(self)
        self.mycommand_search_line.setPlaceholderText(self.tr("搜索自定义命令"))
        self.mycommand_search_line.setFixedHeight(35)

        self.default_button = PrimaryPushButton(self.tr('恢复默认'), self)
        self.default_button.setFixedSize(100, 35)

        self.mycommand_table = TableWidget(self)
        self.mycommand_table.setFixedSize(1140, 500)
        self.mycommand_table.setColumnCount(2)

        self.mycommand_table.setBorderVisible(True)
        self.mycommand_table.setBorderRadius(8)
        self.mycommand_table.setWordWrap(False)
        self.mycommand_table.verticalHeader().hide()
        self.mycommand_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mycommand_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.mycommand_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.line_layout = QHBoxLayout()
        self.line_layout.addWidget(self.mycommand_search_line)
        self.line_layout.addSpacing(5)
        self.line_layout.addWidget(self.default_button)

        self.mycommand_layout = QVBoxLayout()
        self.mycommand_layout.addLayout(self.line_layout)
        self.mycommand_layout.addWidget(self.mycommand_table)
        self.setLayout(self.mycommand_layout)

    def __initInfo(self):
        self.handleMycommandLoad()

    def __connectSignalToSlot(self):
        self.mycommand_search_line.textChanged.connect(self.handleMycommandSearch)
        self.default_button.clicked.connect(self.handleDefaultClicked)

        self.mycommand_table.cellClicked.connect(lambda: self.handleMycommandClicked('single'))
        self.mycommand_table.doubleClicked.connect(lambda: self.handleMycommandClicked('double'))
        self.mycommand_table.itemChanged.connect(self.handleNameChanged)

    def handleMycommandSearch(self):
        keyword = self.mycommand_search_line.text()
        for row in range(self.mycommand_table.rowCount()):
            item_1 = self.mycommand_table.item(row, 0)
            item_2 = self.mycommand_table.item(row, 1)
            iskeyword_1 = item_1.text().lower().find(keyword.lower()) != -1
            iskeyword_2 = item_2.text().lower().find(keyword.lower()) != -1
            if iskeyword_1 or iskeyword_2:
                self.mycommand_table.setRowHidden(row, False)
            else:
                self.mycommand_table.setRowHidden(row, True)

    def handleDefaultClicked(self):
        shutil.copy(cfg.DEFAULT_MYCOMMAND, cfg.MYCOMMAND)
        Info(self.parent, 'S', 1000, self.tr('恢复默认成功！'))
        self.handleMycommandLoad()

    def handleMycommandClicked(self, types):
        row = self.mycommand_table.currentRow()
        column = self.mycommand_table.currentColumn()
        if types == 'single':
            if column == 0:
                self.mycommand_table.editItem(self.mycommand_table.item(row, 0))
            elif column == 1:
                command = self.mycommand_table.item(row, 1).text()
                self.command_update.emit(command)
        elif types == 'double':
            self.mycommand_table.removeRow(row)
            with open(cfg.MYCOMMAND, 'r', encoding='utf-8') as file:
                mycommand = file.readlines()
            with open(cfg.MYCOMMAND, 'w', encoding='utf-8') as file:
                for i, line in enumerate(mycommand):
                    if i != row:
                        file.write(line)

    def handleNameChanged(self):
        selected_item = self.mycommand_table.selectedItems()
        if selected_item:
            rows = self.mycommand_table.rowCount()
            column = self.mycommand_table.currentColumn()
            if column == 0 and selected_item[0].text().strip() == '':
                selected_item[0].setText(self.tr('自定义命令'))
            data = []
            # 临时解决NoneType问题
            try:
                for row in range(rows):
                    first_col = self.mycommand_table.item(row, 0).text()
                    second_col = self.mycommand_table.item(row, 1).text()
                    data_row = f"{first_col} : {second_col}\n"
                    data.append(data_row)
                with open(cfg.MYCOMMAND, 'w', encoding='utf-8') as file:
                    file.writelines(data)
            except:
                pass

    def handleMycommandLoad(self):
        self.mycommand_table.clearFocus()
        if not os.path.exists(cfg.MYCOMMAND):
            shutil.copy(cfg.DEFAULT_MYCOMMAND, cfg.MYCOMMAND)

        with open(cfg.MYCOMMAND, 'r', encoding='utf-8') as file:
            mycommand = file.readlines()
        self.mycommand_table.setRowCount(len(mycommand))
        for i, line in enumerate(mycommand):
            line = line.strip()
            parts = line.split(' : ')
            for j, part in enumerate(parts):
                self.mycommand_table.setItem(i, j, QTableWidgetItem(part))
        self.mycommand_table.setHorizontalHeaderLabels([self.tr('名称'), self.tr('命令')])