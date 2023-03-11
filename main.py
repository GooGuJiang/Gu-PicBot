import src.initialize as initialize
import traceback
import os
import sys
import threading
import time
from loguru import logger
from src.pixiv import download_img, make_tags
from src.rss import get_pixiv_rss
import telebot
import time
import src.twtter as twtter
from src.gusql import pixiv_tg_id_add,twtter_tg_id_add,get_tg_pixiv_message_id,get_tg_message_id_by_twitter_id
import shutil


try:
    config = initialize.check_config()
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
    logger.info("开始执行RSS定时任务")
    try:
        rss_list = get_pixiv_rss()
        if rss_list is not None:
            count_push = 0
            for rss in rss_list:
                if rss is not None:
                    try:
                        if get_tg_pixiv_message_id(rss[1]):
                            continue
                        img_path = download_img(rss[1])
                        #print(img_path)
                        if img_path is not None:
                            push_text = f'''
<b>{img_path["title"]}</b>
作品 ID: <code>{img_path["id"]}</code>
作者: <a href="{img_path["anthor_url"]}">{img_path["author"]}</a>
链接: <a href="{img_path["page_url"]}">🔗链接地址</a>
标签: {make_tags(img_path["tags"])}
'''
                            with open(img_path["path_large"][0], 'rb') as img:
                                push_data = bot.send_photo(config["CHANNEL_ID"], img, caption=f"{push_text}")
                                logger.success(f"推送成功: {rss[1]}")
                                pixiv_tg_id_add(push_data.message_id,img_path["id"])
                            for push_photo in img_path["path_original"]:
                                if is_file_size_exceeds_limit(push_photo):
                                    continue
                                with open(push_photo, 'rb') as img:
                                    bot.send_document(config["CHANNEL_ID"], img, reply_to_message_id=push_data.message_id)
                        count_push += 1
                        if count_push >= 9:
                            time.sleep(60)
                            count_push=0
                        else:
                            time.sleep(1)                                
                        if config["FILE_DELETE"] == True:
                            if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/data/pixiv/{img_path["id"]}'):
                                shutil.rmtree(f'{os.path.dirname(os.path.abspath(__file__))}/data/pixiv/{img_path["id"]}')
                    except Exception as e:
                        logger.error(f"推送失败: {e}")
    except Exception as e:
        logger.error(f"获取RSS失败: {e}")
        return None

#schedule.every().seconds.do(rss_push)

def run_schedule():
    while True:
        #schedule.run_pending()
        rss_push()
        time.sleep(int(config["RSS_SECOND"]))

#schedule.run_pending()
#rss_push()
if config["RSS_OPEN"] == True:
    logger.info("RSS推送已开启")
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

@bot.message_handler(func=lambda m: True)
def push_link(message):
    if message.chat.type == "private":
        if message.from_user.id in config["BOT_ADMIN"]:
            if message.text.startswith("https://www.pixiv.net/artworks/"):
                try:
                    sql_get_gu = get_tg_pixiv_message_id(message.text.split("/")[-1])
                    if sql_get_gu:
                        message_tmmmpp = bot.forward_message(chat_id=message.chat.id,message_id=sql_get_gu,from_chat_id=config['CHANNEL_ID'])
                        bot.send_message(message.chat.id, "已经推送过了!", reply_to_message_id=message_tmmmpp.message_id)
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
                            pixiv_tg_id_add(push_data.message_id,img_path["id"])
                        for push_photo in img_path["path_original"]:
                            if is_file_size_exceeds_limit(push_photo):
                                continue
                            with open(push_photo, 'rb') as img:
                                bot.send_document(config['CHANNEL_ID'], img, reply_to_message_id=push_data.message_id)
                        bot.reply_to(message, "推送成功!")
                        bot.delete_message(message.chat.id, temp.message_id)
                        if config["FILE_DELETE"] == True:
                            if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/data/pixiv/{img_path["id"]}'):
                                shutil.rmtree(f'{os.path.dirname(os.path.abspath(__file__))}/data/pixiv/{img_path["id"]}')
                        return None
                except Exception as e:
                    logger.error(f"推送失败: {e}")
                    bot.reply_to(message, "推送失败,请查看日志!")
                    return None
            try:
                get_tw_url = twtter.extract_tweet_id(message.text)
                sql_get_gu = get_tg_message_id_by_twitter_id(message.text.split("/")[-1])
                if sql_get_gu:
                    message_tmmmpp = bot.forward_message(chat_id=message.chat.id,message_id=sql_get_gu,from_chat_id=config['CHANNEL_ID'])
                    bot.send_message(message.chat.id, "已经推送过了!", reply_to_message_id=message_tmmmpp.message_id)
                    return None
                if get_tw_url["status"] is True:
                    tmp = bot.reply_to(message, "正在推送中...")
                    dl_img = twtter.get_twtter_media(get_tw_url["id"])
                    if dl_img["status"] is False:
                        bot.reply_to(message,"下载图片出错请重新尝试!")
                        return None
                    if len(dl_img["tw_tag"]) >0:
                        taglink = f'\n标签: {twtter.make_tags(dl_img["tw_tag"])}'
                    else:
                        taglink = ""
                    push_text = f'''
<b>{twtter.remove_twitter_links_and_tags(dl_img["tw_text"])}</b>
推文作者: <a href="{dl_img["tw_user_url"]}">{dl_img["tw_user_name"]}</a>
推文链接: <a href="{dl_img["tw_user_url"]}/status/{dl_img["tw_id"]}">🔗链接地址</a>{taglink}
'''
                    with open(dl_img["media_path"][0], 'rb') as img:
                        push_data = bot.send_photo(config['CHANNEL_ID'], img, caption=f"{push_text}")
                        logger.success(f"推送成功: {message.text}")
                        twtter_tg_id_add(push_data.message_id,get_tw_url["id"])
                    for push_photo in dl_img["media_path"]:
                        if is_file_size_exceeds_limit(push_photo):
                            continue
                        with open(push_photo, 'rb') as img:
                            bot.send_document(config['CHANNEL_ID'], img, reply_to_message_id=push_data.message_id)
                    bot.reply_to(message, "推送成功!")
                    bot.delete_message(message.chat.id, tmp.message_id)
                    if config["FILE_DELETE"] == True:
                        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/data/twitter/{get_tw_url["id"]}'):
                            shutil.rmtree(f'{os.path.dirname(os.path.abspath(__file__))}/data/twitter/{get_tw_url["id"]}')
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

        except Exception as e:
            logger.error(f"遇到错误正在重启:{e}")
            traceback.print_exc()
        time.sleep(1)

        
