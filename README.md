<div align="center">
<h1>✏咕谷の插画下载BOT</h1>

![]( https://ggj.moe/wp-content/uploads/2023/03/botimg.webp  )

<p>✏ 可以下载来自Pixiv和Twitter的图片，并将它们上传到Telegram频道。</p>
</div>

## 😀具有以下功能
- 基于RssHub订阅Pixiv收藏并推送
- 解析Pixiv链接并推送
- 解析Twtter链接并推送

## 🤔快速开始

### <img src="https://user-images.githubusercontent.com/511499/117447182-29758200-af0b-11eb-97bd-58723fee62ab.png" alt="Docker" height="28px" align="top"/>Docker

拉取 Docker 镜像

```bash
$ docker pull googujiang/gu-picbot
```

创建机器人数据文件夹
```bash
$ mkdir ~/gu-picbot
```

创建并运行容器

```bash
$ docker run --name gu-picbot \
    -v ~/gu-picbot:/data \
    -e CHANNEL_ID=<channel_id> \
    -e BOT_TOKEN=<bot_token> \
    -e RSS_URL=<rss_url> \
    -e REFRESH_TOKEN=<refresh_token> \
    -e BOT_ADMIN=<bot_admin> \
    -d googujiang/gu-picbot
```

注意：
* `<channel_id>` `<bot_token>` `<rss_url>` `<refresh_token>`请参考下面 `❤️配置说明` 填写

* `BOT_ADMIN` 多个管理员请使用 `,` 分割 

### 普通方式

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
$ python3 main.py
```

5.填写配置文件


6.运行

```bash
$ python3 main.py
```

## 🤖命令列表

目前只能解析Pixiv和Twtter链接，更多功能陆续添加。

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
| LOG\_OPEN | 是否启用日志记录功能 |
| FILE\_DELETE | 是否启用下载后删除文件 |

注意事项：

*   REFRESH\_TOKEN、BOT\_TOKEN和CHANNEL\_ID是必填参数，且必须正确配置才能正常运行机器人。
*   RSS\_URL和RSS\_OPEN参数用于启用和配置RSS订阅功能，可选。
*   PROXY和PROXY\_OPEN参数用于启用和配置代理服务器，可选。
*   BOT\_ADMIN参数用于配置机器人管理员，机器人管理员具有特殊权限，可对机器人进行管理操作。
*   参数的值必须使用双引号包含起来，且必须与参数名之间用等号连接。

## ⁉️已知问题

<details> 
<summary> 
启动时遇到<code>Cloudflare version 2 Captcha</code>
</summary> 
解决方案:

请尝试重新启动几次试试，撞Cloudflare验证了，还是不行就更换IP。
</details> 

## 鸣谢

Twtter图片下载的部分代码来自 [推特媒体文件下载工具](https://github.com/mengzonefire/twitter-media-downloader)
