from Src.Import import *
from Src.Util import *


class Account(ExpandGroupSettingCard):
    command_update = Signal(str)

    def __init__(self):
        self.title = self.tr('管理账号')
        self.content = '/account {create | delete} [username]'
        self.icon = FluentIcon.TAG
        super().__init__(self.icon, self.title, self.content)

        self.account = LineEdit(self)
        self.name_label = BodyLabel(self.tr("名称"))
        self.name_label.setFixedWidth(135)
        self.add(self.name_label, self.account)

        self.uid = LineEdit(self)
        self.uid_label = BodyLabel(self.tr("UID"))
        self.uid_label.setFixedWidth(135)
        self.add(self.uid_label, self.uid)

        self.password = LineEdit(self)
        self.pwd_label = BodyLabel(self.tr("密码"))
        self.pwd_label.setFixedWidth(135)
        self.add(self.pwd_label, self.password)

        self.create = PrimaryPushButton(self.tr("创建"))
        self.delete = PrimaryPushButton(self.tr("删除"))
        self.card.hBoxLayout.insertWidget(5, self.create)
        self.card.hBoxLayout.insertSpacing(6, 12)
        self.card.hBoxLayout.insertWidget(7, self.delete)
        self.card.hBoxLayout.insertSpacing(8, 12)

        self.create.clicked.connect(lambda: self.onClicked('create'))
        self.delete.clicked.connect(lambda: self.onClicked('delete'))

    def add(self, label, widget):
        w = QWidget()
        w.setFixedHeight(60)

        layout = QHBoxLayout(w)
        layout.setContentsMargins(48, 12, 48, 12)

        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(widget)

        self.addGroupWidget(w)

    def onClicked(self, types):
        name = self.account.text()
        uid = self.uid.text()
        pwd = self.password.text()
        cmd = f'/account {types}'

        if types == 'create':
            if name != '': cmd += ' ' + name
            if uid != '': cmd += ' ' + uid
            if pwd != '': cmd += ' ' + pwd
        elif types == 'delete':
            if uid != '': cmd += ' ' + uid

        self.command_update.emit(cmd)