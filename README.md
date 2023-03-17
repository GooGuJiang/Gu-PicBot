<div align="center">
  <h1>✏ GooGu's Illustration Downloading BOT</h1>
  <p>✏ A Telegram bot that can download images from Pixiv and Twitter and upload them to Telegram channels.</p>

  ![](https://ggj.moe/wp-content/uploads/2023/03/botimg.webp)
</div>

## 😀 Features
- Subscribe to Pixiv favorites based on RssHub and push them
- Parse Pixiv links and push them
- Parse Twitter links and push them

## 🤔 Quick Start

### <img src="https://user-images.githubusercontent.com/511499/117447182-29758200-af0b-11eb-97bd-58723fee62ab.png" alt="Docker" height="28px" align="top"/> Docker

1. Pull Docker image

```bash
$ docker pull googujiang/gu-picbot
```

2. Create bot data folder
```bash
$ mkdir ~/gu-picbot
```

3. Create and run container

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

**Note:**
* Please refer to the following [❤️ Configuration](#%EF%B8%8F-configuration) for `<channel_id>`, `<bot_token>`, `<rss_url>`, `<refresh_token>`.

* Use `,` to separate multiple `BOT_ADMIN`.

### Normal Way

1. Make sure the `python` version is `>=3.6.*`.

2. Clone this repository:

```bash
$ git clone https://github.com/GooGuJiang/Gu-Random-Image.git
```

3. Install required libraries:

```bash
$ pip install -r requirements.txt
```

4. Run initialization:
```bash
$ python3 main.py
```

5 Fill in the configuration file.

6. Run:

```bash
$ python3 main.py
```

## 🤖 Command List

Currently, only Pixiv and Twitter links can be parsed, and more functions will be added later.

## ❤️ Configuration

Here is a detailed description of the configuration parameters:

| Parameter | Description |
| --- | --- |
| REFRESH\_TOKEN | The refresh token used to obtain a new access token |
| RSS\_URL | The URL of the RSS subscription |
| BOT\_TOKEN | The Telegram bot token |
| CHANNEL\_ID | The unique identifier of the channel or group to send messages |
| BOT\_ADMIN | A list of user IDs of the bot administrator |
| RSS\_SECOND | The time interval (in seconds) for RSS update check |
| PROXY | URL of the proxy server |
| PROXY\_OPEN | Whether to enable the proxy server |
| LOG\_OPEN | Whether to enable logging |
| FILE\_DELETE | Whether to delete the downloaded file after downloading |

Note:

* REFRESH\_TOKEN, BOT\_TOKEN, and CHANNEL\_ID are required parameters, and must be correctly configured to run the bot.
* The RSS\_URL and RSS\_OPEN parameters are used to enable and configure the RSS subscription function, and are optional.
* The PROXY and PROXY\_OPEN parameters are used to enable and configure the proxy server, and are optional.
* The BOT\_ADMIN parameter is used to configure bot administrators, who have special permissions to manage the bot.
* The value of the parameter must be enclosed in double quotes, and must be connected to the parameter name with an equal sign.

## ⁉️ Known Issues

<details> 
<summary> 
Encounter <code>Cloudflare version 2 Captcha</code> when starting up
</summary> 
Solution:

It has been solved by a hardcore method, but if it still doesn't work after 10 automatic retries, it may be an IP problem.
</details> 

## Acknowledgements

Some of the code for downloading Twitter images comes from [Twitter media downloader](https://github.com/mengzonefire/twitter-media-downloader).
