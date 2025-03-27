from . import *
from Src.Import import *
from Src.Util import *


class Remote(ScrollArea):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        InitUI.initPivot(self, text)

        self.__initWidget()
        self.__initLayout()
        self.__initInfo()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.PRemoteInterface = SettingCardGroup(self.scrollWidget)
        self.usePRemoteCard = SwitchSettingCard(
            FluentIcon.CODE,
            self.tr('启用用户端远程执行'),
            self.tr('使用登陆用户接口执行远程命令'),
            configItem=CFG.usePRemote
        )
        self.setURLCard = SetUrl(
            self.tr('配置服务端地址'),
            self.tr('设置远程执行服务端地址')
        )
        self.setAPICard = SetApi(
            self.tr('配置服务端API'),
            self.tr('设置用于远程执行命令的地址, 适应不兼容服务端')
        )
        self.setUIDCard = SetUid(
            self.tr('配置UID'),
            self.tr('设置默认远程目标玩家的UID')
        )
        self.VerifyCard = Verify(
            self.tr('验证账号'),
            self.tr('通过验证码验证身份')
        )
        self.CRemoteInterface = SettingCardGroup(self.scrollWidget)
        self.useCRemoteCard = SwitchSettingCard(
            FluentIcon.CODE,
            self.tr('启用控制台远程执行'),
            self.tr('使用控制台接口执行远程命令'),
            configItem=CFG.useCRemote
        )
        self.setKeyCard = SetKey(
            self.tr('配置密码'),
            self.tr('设置控制台远程执行的密码')
        )

    def __initLayout(self):
        self.PRemoteInterface.addSettingCard(self.usePRemoteCard)
        self.PRemoteInterface.addSettingCard(self.setURLCard)
        self.PRemoteInterface.addSettingCard(self.setAPICard)
        self.PRemoteInterface.addSettingCard(self.setUIDCard)
        self.PRemoteInterface.addSettingCard(self.VerifyCard)
        self.CRemoteInterface.addSettingCard(self.useCRemoteCard)
        self.CRemoteInterface.addSettingCard(self.setKeyCard)

        InitUI.addSubInterface(self, self.PRemoteInterface, 'PRemoteInterface', self.tr('用户端'), icon=FluentIcon.CHAT)
        InitUI.addSubInterface(self, self.CRemoteInterface, 'CRemoteInterface', self.tr('控制台'), icon=FluentIcon.LINK)

        InitUI.initPivotLayout(self, self.PRemoteInterface, True)

    def __initInfo(self):
        if not CFG.get(CFG.usePRemote):
            self.setURLCard.setDisabled(True)
            self.setAPICard.setDisabled(True)
            self.setUIDCard.setDisabled(True)
            self.VerifyCard.setDisabled(True)
        if not CFG.get(CFG.useCRemote):
            self.setKeyCard.setDisabled(True)
        self.setURLCard.titleLabel.setText(self.tr('配置服务端地址 (当前: ') + CFG.get(CFG.serverUrl) + ')')
        self.setUIDCard.titleLabel.setText(self.tr('配置UID (当前: ') + CFG.get(CFG.uid) + ')')

    def __connectSignalToSlot(self):
        self.usePRemoteCard.checkedChanged.connect(self.handlePRemoteChanged)
        self.setURLCard.clicked_seturl.connect(lambda: self.handlePRemoteClicked('seturl'))
        self.setAPICard.clicked_setapi.connect(lambda: self.handlePRemoteClicked('setapi'))
        self.setUIDCard.clicked_setuid.connect(lambda: self.handlePRemoteClicked('setuid'))
        self.VerifyCard.clicked_apply.connect(lambda: self.handlePRemoteClicked('apply'))
        self.VerifyCard.clicked_verify.connect(lambda: self.handlePRemoteClicked('verify'))
        self.useCRemoteCard.checkedChanged.connect(self.handleCRemoteChanged)
        self.setKeyCard.clicked_setkey.connect(self.handleCRemoteClicked)

    def handlePRemoteChanged(self):
        if CFG.get(CFG.usePRemote):
            self.setURLCard.setDisabled(False)
            self.setAPICard.setDisabled(False)
            self.setUIDCard.setDisabled(False)
            self.VerifyCard.setDisabled(False)
        else:
            self.setURLCard.setDisabled(True)
            self.setAPICard.setDisabled(True)
            self.setUIDCard.setDisabled(True)
            self.VerifyCard.setDisabled(True)

    def handleCRemoteChanged(self):
        if CFG.get(CFG.useCRemote):
            self.setKeyCard.setDisabled(False)
        else:
            self.setKeyCard.setDisabled(True)

    def handlePRemoteClicked(self, command):
        if command == 'seturl':
            tmp_url = self.setURLCard.lineedit_seturl.text()
            if tmp_url != '':
                CFG.set(CFG.serverUrl, tmp_url)
                Info(self.parent, 'S', 1000, self.tr('服务端地址设置成功!'))
            else:
                Info(self.parent, 'E', 3000, self.tr('服务端地址为空!'))
        if command == 'setapi':
            Open(self, CFG.CONFIG)
        if command == 'setuid':
            tmp_uid = self.setUIDCard.lineedit_setuid.text()
            if tmp_uid != '':
                CFG.set(CFG.uid, tmp_uid)
                Info(self.parent, 'S', 1000, self.tr('UID设置成功!'))
            else:
                Info(self.parent, 'E', 3000, self.tr('UID为空!'))
        if command == 'apply':
            status, message = handleApply(CFG.get(CFG.uid))
            if status == "success":
                Info(self.parent, 'S', 1000, self.tr('验证码发送成功!'), self.tr("请在游戏内查收验证码!"))
            elif status == "error":
                Info(self.parent, 'E', 3000, self.tr('验证码发送失败!'), str(message))
        if command == 'verify':
            tmp_code = self.VerifyCard.lineedit_code.text()
            if tmp_code == '':
                Info(self.parent, 'E', 3000, self.tr('验证码为空!'))
                return

            status, message = handleVerify(CFG.get(CFG.uid), tmp_code)
            if status == "success":
                Info(self.parent, 'S', 1000, self.tr('账号验证成功, 密钥为: ') + message)
                CFG.set(CFG.pKey, message)
            elif status == "error":
                Info(self.parent, 'E', 3000, self.tr('验证码错误!'), str(message))

        self.__initInfo()

    def handleCRemoteClicked(self):
        console_key = self.setKeyCard.lineedit_setkey.text()
        if console_key != '':
            CFG.set(CFG.cKey, console_key)
            Info(self.parent, 'S', 1000, self.tr('控制台密码设置成功!'))
        else:
            Info(self.parent, 'E', 3000, self.tr('控制台密码为空!'))
