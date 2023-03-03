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

try:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)
    proxy_open = config['PROXY_OPEN']
    bot = telebot.TeleBot(config["BOT_TOKEN"], parse_mode="html")
    if proxy_open == True:
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
                        if img_path is not None:
                            push_text = f'''
作品名称: <b>{img_path["title"]}</b>
作品 ID: <b>{img_path["id"]}</b>
作者: <a href="{img_path["anthor_url"]}">{img_path["author"]}</a>
链接: <a href="{img_path["page_url"]}">🔗链接地址</a>
标签: {make_tags(img_path["tags"])}\n\n
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
    print(message)
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
