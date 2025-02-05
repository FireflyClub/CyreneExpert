from app.importer import *


class MessageBoxBase(MaskDialogBase):
    accepted = Signal()
    rejected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttonGroup = QFrame(self.widget)
        self.yesButton = PrimaryPushButton(self.tr('登录'), self.buttonGroup)
        self.cancelButton = PrimaryPushButton(self.tr('退出'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(self.widget)
        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)

        self.yesButton.setFocus()
        self.buttonGroup.setFixedHeight(81)

        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.viewLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def __onCancelButtonClicked(self):
        self.reject()
        self.rejected.emit()

    def __onYesButtonClicked(self):
        # self.accept()
        self.accepted.emit()

    def __setQss(self):
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')
        FluentStyleSheet.DIALOG.apply(self)

    def hideYesButton(self):
        self.yesButton.hide()
        self.buttonLayout.insertStretch(0, 1)

    def hideCancelButton(self):
        self.cancelButton.hide()
        self.buttonLayout.insertStretch(0, 1)


class MessageLogin(MessageBoxBase):
    passwordEntered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel(self.tr('登陆验证'))
        self.passwordLabel = PasswordLineEdit(self)
        self.passwordLabel.setFixedWidth(300)
        self.passwordLabel.setPlaceholderText(self.tr('请输入密码'))
        self.yesButton.clicked.connect(self.emitPassword)
        self.cancelButton.clicked.connect(lambda: sys.exit())

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.passwordLabel)

    def emitPassword(self):
        password = self.passwordLabel.text()
        self.passwordEntered.emit(password)
