import initialize
import traceback
import yaml
import os
import sys
import schedule
import threading
import time
from loguru import logger
from pixiv import download_img, make_tags
from rss import get_pixiv_rss
import telebot
import time
import twtter

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    initialize.init()

try:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)
    bot = telebot.TeleBot(config["BOT_TOKEN"], parse_mode="html")
    if config['PROXY_OPEN'] == True:
        from telebot import apihelper
        proxy = {
            "http": config['PROXY'],
            "https": config['PROXY']
        }
        apihelper.proxy = proxy
    else:
        proxy = None
    logger.success("配置文件加载成功 :)")
except Exception as e:
    logger.error(f"配置文件加载失败:(\n{e}")
    sys.exit()

def is_file_size_exceeds_limit(file_path: str, limit: int = 50 * 1024 * 1024) -> bool:
    file_size = os.path.getsize(file_path)
    return file_size > limit

def rss_push():
    try:
        rss_list = get_pixiv_rss()
        if rss_list is not None:
            count_push = 0
            for rss in rss_list:
                if rss is not None:
                    try:
                        img_path = download_img(rss["pid"])
                        #print(img_path)
                        if str(rss["pid"]) in os.listdir(f'{os.path.dirname(os.path.abspath(__file__))}/pixiv'):
                            return None
                        if img_path is not None:
                            push_text = f'''
<b>{img_path["title"]}</b>\n
作品 ID: <code>{img_path["id"]}</code>
作者: <a href="{img_path["anthor_url"]}">{img_path["author"]}</a>
链接: <a href="{img_path["page_url"]}">🔗链接地址</a>
标签: {make_tags(img_path["tags"])}
'''
                            with open(img_path["path_large"][0], 'rb') as img:
                                push_data = bot.send_photo(config["CHANNEL_ID"], img, caption=f"{push_text}")
                                logger.success(f"推送成功: {rss['title']}")
                            for push_photo in img_path["path_original"]:
                                if is_file_size_exceeds_limit(push_photo):
                                    continue
                                with open(push_photo, 'rb') as img:
                                    bot.send_document(config["CHANNEL_ID"], img, reply_to_message_id=push_data.message_id)
                        count_push += 1
                        if count_push >= 9:
                            time.sleep(20)
                            count_push=0
                        else:
                            time.sleep(1)                                
                        
                    except Exception as e:
                        logger.error(f"推送失败: {e}")
    except Exception as e:
        logger.error(f"获取RSS失败: {e}")
        return None

schedule.every(int(config["RSS_SECOND"])).seconds.do(rss_push)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

#调试用
#rss_push()
if config["RSS_OPEN"] == True:
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

@bot.message_handler(func=lambda m: True)
def push_link(message):
    if message.chat.type == "private":
        if message.from_user.id in config["BOT_ADMIN"]:
            if message.text.startswith("https://www.pixiv.net/artworks/"):
                try:
                    if str(message.text.split("/")[-1]) in os.listdir(f'{os.path.dirname(os.path.abspath(__file__))}/pixiv'):
                        bot.reply_to(message, "该图片已经推送过了")
                        return None
                    temp = bot.reply_to(message, "正在推送中...")
                    img_path = download_img(message.text.split("/")[-1])
                    if img_path is not None:
                        push_text = f'''
<b>{img_path["title"]}</b>
作品 ID: <code>{img_path["id"]}</code>
作者: <a href="{img_path["anthor_url"]}">{img_path["author"]}</a>
链接: <a href="{img_path["page_url"]}">🔗链接地址</a>
标签: {make_tags(img_path["tags"])}
                        ''' 
                        with open(img_path["path_large"][0], 'rb') as img:
                            push_data = bot.send_photo(config['CHANNEL_ID'], img, caption=f"{push_text}")
                            logger.success(f"推送成功: {message.text}")
                        for push_photo in img_path["path_original"]:
                            if is_file_size_exceeds_limit(push_photo):
                                continue
                            with open(push_photo, 'rb') as img:
                                bot.send_document(config['CHANNEL_ID'], img, reply_to_message_id=push_data.message_id)
                        bot.reply_to(message, "推送成功!")
                        bot.delete_message(message.chat.id, temp.message_id)
                        return None
                except Exception as e:
                    logger.error(f"推送失败: {e}")
                    bot.reply_to(message, "推送失败,请查看日志!")
                    return None
            get_tw_url = twtter.extract_tweet_id(message.text)
            if get_tw_url["status"] is True:
                dl_img = twtter.get_twtter_media(get_tw_url["id"])
                if dl_img["status"] is False:
                    bot.reply_to(message,"下载图片出错请重新尝试!")
                    return None
            try:
                get_tw_url = twtter.extract_tweet_id(message.text)
                if get_tw_url["status"] is True:
                    tmp = bot.reply_to(message, "正在推送中...")
                    dl_img = twtter.get_twtter_media(get_tw_url["id"])
                    if dl_img["status"] is False:
                        bot.reply_to(message,"下载图片出错请重新尝试!")
                        return None
                    if dl_img["tw_tag"] is not None:
                        taglink = f'\n标签: {twtter.make_tags(dl_img["tw_tag"])}'
                    push_text = f'''
<b>{twtter.remove_twitter_links_and_tags(dl_img["tw_text"])}</b>
推文作者: <a href="{dl_img["tw_user_url"]}">{dl_img["tw_user_name"]}</a>
推文链接: <a href="{dl_img["tw_user_url"]}/status/{dl_img["tw_id"]}">🔗链接地址</a>{taglink}
'''
                    with open(dl_img["media_path"][0], 'rb') as img:
                        push_data = bot.send_photo(config['CHANNEL_ID'], img, caption=f"{push_text}")
                        logger.success(f"推送成功: {message.text}")
                    for push_photo in dl_img["media_path"]:
                        if is_file_size_exceeds_limit(push_photo):
                            continue
                        with open(push_photo, 'rb') as img:
                            bot.send_document(config['CHANNEL_ID'], img, reply_to_message_id=push_data.message_id)
                    bot.reply_to(message, "推送成功!")
                    bot.delete_message(message.chat.id, tmp.message_id)
                    return None
            except Exception as e:
                logger.error(f"推送失败: {e}")
                bot.reply_to(message, "推送失败,请查看日志!")
                return None
    #print(message)
	#bot.reply_to(message, message.text)

if __name__ == '__main__':
    #import logging
    while True:
        try:
            #logger = telebot.logger
            #telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
            logger.success(f"启动成功!")
            bot.polling()

        except Exception:
            logger.error(f"遇到错误正在重启:")
            traceback.print_exc()
        time.sleep(1)