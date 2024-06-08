# Firefly Launcher-Beta
![Firefly-Launcher-Beta](https://socialify.git.ci/letheriver2007/Firefly-Launcher/image?description=1&forks=1&issues=1&language=1&name=1&pulls=1&stargazers=1&theme=Light)

## 功能简介

### 一键启动
- 快速启动 Fiddler.exe + Star Rail.exe

### 配置说明
- 功能配置

主题配置: ```导航 > 主题```, 切换明暗主题.

主题色配置: ```导航 > 设置 > 主题色```, 自定义主题色(默认流萤主题色你居然要改???).

DPI缩放配置: ```导航 > 设置 > DPI```, 调整游戏窗口大小, 建议跟随系统设置.

语言配置: ```导航 > 设置 > 语言```, 切换语言, 支持简体中文 / 繁體中文 / English.

- 多游戏版本配置

游戏版本配置: ```导航 > 启动器 > 配置 > 选择游戏版本```

单独游戏启动: ```导航 > 启动器 > 启动游戏```

- 代理配置

代理配置: ```导航 > 代理 > 配置 > 选取Fiddler```

单独代理启动: ```导航 > 代理 > 原版打开 / 导航 > 代理 > 脚本打开 > LunarCore / LunarCore(SSL) ```

代理脚本备份: ```导航 > 代理 > 备份```, 文件会以 CustomRules_```TIME```.js 保存在启动器根目录下.

系统代理重置: ```导航 > 代理 > 重置代理```, 将会清空系统代理配置并关闭.

- config.json 配置(不推荐)
```
{
  "UID": "10001", // 用户远程模式登陆账号
  "KEY": "lethe", // 用户远程模式账号密码
  "SERVER_URL": "127.0.0.1:22501", // 服务器地址
  "ROUTE_PAPPLY": "/api/papply", // 申请验证码接口
  "ROUTE_PVERIFY": "/api/pverify", // 验证并设置密码接口
  "ROUTE_PREMOTE": "/api/premote", // 用户远程模式执行接口
  "ROUTE_CREMOTE": "/api/cremote" // 控制台远程模式执行接口
}
```

### LunarCore 命令

- 功能配置

命令自动复制: ```导航 > LunarCore > 命令自动复制```, 使用命令后自动复制到剪贴板.

手动自定义配置(不推荐): ```导航 > LunarCore > 自定义命令设置 / 遗器命令设置```, 手动配置命令.

远程配置:

```导航 > LunarCore > 远程 > 启用远程执行```

```导航 > LunarCore > 远程 > 配置服务端地址```, 配置服务端公用地址 + DISPATCH / HTTP 端口

```导航 > LunarCore > 远程 > 配置服务端API```, 配置不兼容服务端API地址(使用JokerSR无需更改).

```导航 > LunarCore > 远程 > 配置UID```, 配置用户远程模式登陆账号.

```导航 > LunarCore > 远程 > 配置密码 > 发送```, 登陆游戏账号并接受验证码.

```导航 > LunarCore > 远程 > 配置密码 > 验证码 + 密码```, 输入验证码并设置密码.
