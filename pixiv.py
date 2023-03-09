from pixivpy3 import *
import yaml
import sys
import os
import sqlite3
import time
from loguru import logger

#初始化目录
if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/pixiv") is False:
    os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}/pixiv")

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/data") is False:
    os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}/data")

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    sys.exit()
else:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)

PIXIV_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/pixiv"
# Connect to the SQLite database
PIXIV_DB = f'{os.path.dirname(os.path.abspath(__file__))}/data/bot_data.db'


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
    return total_size

def insert_image_data(pid,img_path):
    try:
        conn = sqlite3.connect(PIXIV_DB)
        c = conn.cursor()
        c.execute('INSERT INTO pixiv_images (pid, file_size,file_path) VALUES (?, ?, ?)', (pid, get_folder_size(img_path),img_path))
        conn.commit()
        conn.close()
        return True
    except:
        return False
    
def is_pid_exist(pid):
    """Check if a given PID exists in the database."""
    conn = sqlite3.connect(PIXIV_DB)
    c = conn.cursor()
    c.execute("SELECT pid FROM pixiv_images WHERE pid = ?", (pid,))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False

REFRESH_TOKEN = config['REFRESH_TOKEN']

#初始化PixivPy
#api = AppPixivAPI()
def pixiv_load():
    global api
    logger.info(f"初始化Pixiv API")
    while True:
        try:
            api = AppPixivAPI()
            api.auth(refresh_token=REFRESH_TOKEN)
            logger.info(f"初始化Pixiv API成功")
            return None
        except Exception as e:
            logger.error(f"遇到 Cloudflare version 2 Captcha ，将尝试重新初始化PIXIV API")
        time.sleep(1)    

pixiv_load()

def get_file_name(url,size):
    data ={
        "file_name":f"{url.split('/')[-1].split('.')[0]}_{size}.{url.split('/')[-1].split('.')[1]}",
        "page":url.split('/')[-1].split('.')[0].split('_')[1],}
    return data
    #return f"{url.split('/')[-1].split('.')[0]}_{size}.{url.split('/')[-1].split('.')[1]}"

def download_img(pixiv_id):
    #api.auth(refresh_token=REFRESH_TOKEN)
    try:
        json_result = api.illust_detail(pixiv_id)
        illust = json_result.illust
        img_url = illust.meta_pages
    except Exception as e:
        logger.error("遇到Pixiv API错误，尝试重新初始化API")
        pixiv_load()
        json_result = api.illust_detail(pixiv_id)
        illust = json_result.illust
        img_url = illust.meta_pages
    path_large =[]
    path_original =[]
    mkdir_gu = f"{PIXIV_PATH}/{illust.id}"
    #print(illust.meta_single_page)
    #print(illust)
    if os.path.exists(mkdir_gu) is False:
        os.mkdir(mkdir_gu)
    if len(illust.meta_single_page) == 0:
        for i in img_url:
            for j in i.image_urls:
                if j == "large":
                    input_path = f"{PIXIV_PATH}/{illust.id}/{get_file_name(i.image_urls[j],j)['page']}"
                    if os.path.exists(input_path) is False:
                        os.mkdir(input_path)
                    path_large.append(f"{input_path}/{get_file_name(i.image_urls[j],j)['file_name']}")
                    api.download(i.image_urls[j],path=input_path,name=get_file_name(i.image_urls[j],j)['file_name'])
                elif j == "original":
                    path_original.append(f"{input_path}/{get_file_name(i.image_urls[j],j)['file_name']}")
                    api.download(i.image_urls[j],path=input_path,name=get_file_name(i.image_urls[j],j)['file_name'])
    else:
        input_path = f"{PIXIV_PATH}/{illust.id}/{get_file_name(illust.meta_single_page['original_image_url'],illust.meta_single_page['original_image_url'])['page']}"
        if os.path.exists(input_path) is False:
            os.mkdir(input_path)
        api.download(illust.meta_single_page['original_image_url'],path=input_path,name=get_file_name(illust.meta_single_page['original_image_url'],'original')['file_name'])
        path_original.append(f"{input_path}/{get_file_name(illust.meta_single_page['original_image_url'],'original')['file_name']}")
        api.download(illust.image_urls['large'],path=input_path,name=get_file_name(illust.image_urls['large'],'large')['file_name'])
        path_large.append(f"{input_path}/{get_file_name(illust.image_urls['large'],'large')['file_name']}")
    file_data={
        "id":illust.id,
        "title":illust.title,
        "author":illust.user.name,
        "author_id":illust.user.id,
        "anthor_url":f"https://www.pixiv.net/users/{illust.user.id}",
        "tags":illust.tags,
        "create_date":illust.create_date,
        "page_url":f"https://www.pixiv.net/artworks/{illust.id}",
        "page_count":illust.page_count,
        "path_large":path_large,
        "path_original":path_original,
    }
    
    #print(file_data)
    #os.mkdir(f"{PIXIV_PATH}/{illust.id}")
    #for i in illust.image_urls:
    #    file_name_list = illust.image_urls[i].split("/")[-1].split(".")
    #    file_name = f"{file_name_list[0]}_{i}.{file_name_list[1]}"
    #    print(file_name)
    #api.download(illust.image_urls['large'],path=f"{PIXIV_PATH}/{illust.id}/",name=f"{illust.id}_large.jpg")
    
    try:
        insert_image_data(pixiv_id,f"{PIXIV_PATH}/{illust.id}")
        api.illust_bookmark_add(pixiv_id, restrict="public")
    except Exception as e:
        logger.error(e)
    return file_data

def make_tags(tags):
    tag = ""
    for i in tags:
        tag += f"#{i['name']} "
    return tag

if __name__ == "__main__":
    #print(download_img(105797544))
    #print(is_pid_exist("105797544"))
    #tag =  [{'name': 'オリジナル', 'translated_name': 'original'}, {'name': '女の子', 'translated_name': 'girl'}, {'name': '緑髪', 'translated_name': 'green hair'}, {'name': '天使', 'translated_name': 'angel'}, {'name': 'おっぱい', 'translated_name': 'breasts'}]
    #print(make_tags(tag))
    pass