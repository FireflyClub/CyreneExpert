import urllib.request
from src.head import *
from src.util import *


class SetUrl(SettingCard):
    clicked_seturl = Signal()

    def __init__(self, title, content, icon=FluentIcon.WIFI):
        super().__init__(icon, title, content)
        self.lineedit_seturl = LineEdit(self)
        self.lineedit_seturl.setPlaceholderText(self.tr("服务端地址"))
        self.lineedit_seturl.setFixedWidth(150)
        self.button_seturl = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_seturl)


class SetApi(SettingCard):
    clicked_setapi = Signal()

    def __init__(self, title, content, icon=FluentIcon.LABEL):
        super().__init__(icon, title, content)
        self.button_seturl = PrimaryPushButton(self.tr('打开文件'), self)
        self.hBoxLayout.addWidget(self.button_seturl, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_seturl.clicked.connect(self.clicked_setapi)


class SetUid(SettingCard):
    clicked_setuid = Signal()

    def __init__(self, title, content, icon=FluentIcon.QUICK_NOTE):
        super().__init__(icon, title, content)
        self.lineedit_setuid = LineEdit(self)
        self.lineedit_setuid.setPlaceholderText("UID")
        self.lineedit_setuid.setFixedWidth(150)
        self.lineedit_setuid.setValidator(QIntValidator(self))
        self.button_setuid = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_setuid, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_setuid.clicked.connect(self.clicked_setuid)


class Verify(SettingCard):
    clicked_apply = Signal()
    clicked_verify = Signal()

    def __init__(self, title, content, icon=FluentIcon.FINGERPRINT):
        super().__init__(icon, title, content)
        self.button_apply = PrimaryPushButton(self.tr('发送'), self)
        self.lineedit_code = LineEdit(self)
        self.lineedit_code.setPlaceholderText(self.tr("验证码"))
        self.lineedit_code.setFixedWidth(100)
        self.lineedit_code.setValidator(QIntValidator(self))
        self.button_verify = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.button_apply, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addWidget(self.lineedit_code, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_verify, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_apply.clicked.connect(self.clicked_apply)
        self.button_verify.clicked.connect(self.clicked_verify)


class SetKey(SettingCard):
    clicked_setkey = Signal()

    def __init__(self, title, content, icon=FluentIcon.QUICK_NOTE):
        super().__init__(icon, title, content)
        self.lineedit_setkey = PasswordLineEdit(self)
        self.lineedit_setkey.setPlaceholderText(self.tr("控制台密码"))
        self.lineedit_setkey.setFixedWidth(150)
        self.button_setkey = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_setkey, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_setkey, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_setkey.clicked.connect(self.clicked_setkey)


class SetTarget(SettingCard):
    clicked_settarget = Signal()

    def __init__(self, title, content, icon=FluentIcon.QUICK_NOTE):
        super().__init__(icon, title, content)
        self.lineedit_settarget = LineEdit(self)
        self.lineedit_settarget.setPlaceholderText("UID")
        self.lineedit_settarget.setFixedWidth(150)
        self.button_settarget = PrimaryPushButton(self.tr('设置'), self)
        self.hBoxLayout.addWidget(self.lineedit_settarget, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.button_settarget, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button_settarget.clicked.connect(self.clicked_settarget)


def handleApply(uid):
    base_url = 'http://' + cfg.get(cfg.serverUrl) + cfg.ROUTE_PAPPLY
    data = json.dumps({'uid': int(uid)}).encode('utf-8')

    req = urllib.request.Request(base_url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err


def handleVerify(uid, code):
    base_url = 'http://' + cfg.get(cfg.serverUrl) + cfg.ROUTE_PVERIFY
    data = json.dumps(
        {
            'uid': int(uid),
            'code': int(code)
        }
    ).encode('utf-8')
    
    req = urllib.request.Request(base_url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err


def handleCommandSend(uid, key, command):
    base_url = 'http://' + cfg.get(cfg.serverUrl) + cfg.ROUTE_PREMOTE
    data = json.dumps(
        {
            'uid': int(uid),
            'key': key,
            'cmd': command
        }
    ).encode('utf-8')

    req = urllib.request.Request(base_url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err

def handleCosoleSend(key, command):
    base_url = 'http://' + cfg.get(cfg.serverUrl) + cfg.ROUTE_CREMOTE
    data = json.dumps(
        {
            'key': key,
            'cmd': command
        }
    ).encode('utf-8')

    req = urllib.request.Request(base_url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
            if response_json['retcode'] == 200:
                return 'success', response_json['message']
            else:
                return 'error', response_json['message']

    except urllib.error.HTTPError as http_err:
        print(f'网络请求失败, {http_err}')
        return 'error', http_err

    except urllib.error.URLError as req_err:
        print(f'请求格式错误, {req_err}')
        return 'error', req_err

    except Exception as err:
        print(f'未知错误, {err}')
        return 'error', err
