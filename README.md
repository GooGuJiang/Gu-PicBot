<div align="center">
<h1>✏咕谷の动漫图片下载BOT</h1>

![]( https://ggj.moe/wp-content/uploads/2023/03/botimg.webp  )

<p>✏ 可以下载来自Pixiv和Twitter的图片，并将它们上传到Telegram频道。</p>
</div>

## 😀具有以下功能
- 基于RssHub订阅Pixiv收藏并推送
- 解析Pixiv链接并推送
- 解析Twtter链接并推送

## 🤔如何配置

1. 确保 `python` 的版本为 `>=3.6.*` 以上

2. 将本仓库 `clone` 到本地:

```bash
$ git clone https://github.com/GooGuJiang/Gu-Random-Image.git
```

3. 安装所需库

```bash
$ pip install -r requirements.txt
```

4. 初始化

```bash
$ pip install -r requirements.txt
```

5.填写配置文件


6.运行

```bash
$ python3 main.py
```

## ❤️配置说明

以下是配置参数的详细说明：

| 参数名 | 描述 |
| --- | --- |
| REFRESH\_TOKEN | 用于获取新的access\_token的刷新令牌 |
| RSS\_URL | RSS订阅的URL |
| BOT\_TOKEN | Telegram机器人Token |
| CHANNEL\_ID | 发送消息的频道或群组的唯一标识符 |
| BOT\_ADMIN | 机器人管理员的用户ID列表 |
| RSS\_SECOND | RSS更新检查的时间间隔（单位：秒） |
| PROXY | 代理服务器的URL |
| PROXY\_OPEN | 是否启用代理服务器 |
| RSS\_OPEN | 是否启用RSS订阅功能 |

注意事项：

*   REFRESH\_TOKEN、BOT\_TOKEN和CHANNEL\_ID是必填参数，且必须正确配置才能正常运行机器人。
*   RSS\_URL和RSS\_OPEN参数用于启用和配置RSS订阅功能，可选。
*   PROXY和PROXY\_OPEN参数用于启用和配置代理服务器，可选。
*   BOT\_ADMIN参数用于配置机器人管理员，机器人管理员具有特殊权限，可对机器人进行管理操作。
*   参数的值必须使用双引号包含起来，且必须与参数名之间用等号连接。

## 🤖命令列表

目前只能解析Pixiv和Twtter链接，更多功能陆续添加。

## 🆕更多部署方式

目前只有部署在Linux和Windows平台，Docker等部署方式后续添加。

## ⁉️已知问题

问题1:

启动时候遇到下面这个问题怎么解决？
```bash
pixivpy3.utils.PixivError: requests POST https://oauth.secure.pixiv.net/auth/token error: Detected a Cloudflare version 2 Captcha challenge, This feature is not available in the opensource (free) version.
```

解决方案:

请尝试重新启动几次试试，撞Cloudflare验证了，还是不行就更换IP。

## 鸣谢

Twtter图片下载的部分代码来自 [推特媒体文件下载工具](https://github.com/mengzonefire/twitter-media-downloader)
