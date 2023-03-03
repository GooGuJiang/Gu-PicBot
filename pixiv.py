from pixivpy3 import *
import yaml
import sys
import os


#初始化目录
if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/pixiv") is False:
    os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}/pixiv")

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    sys.exit()
else:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)

#配置
PIXIV_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/pixiv"

REFRESH_TOKEN = config['REFRESH_TOKEN']

#初始化PixivPy
api = AppPixivAPI()
api.auth(refresh_token=REFRESH_TOKEN)



def get_file_name(url,size):
    data ={
        "file_name":f"{url.split('/')[-1].split('.')[0]}_{size}.{url.split('/')[-1].split('.')[1]}",
        "page":url.split('/')[-1].split('.')[0].split('_')[1],}
    return data
    #return f"{url.split('/')[-1].split('.')[0]}_{size}.{url.split('/')[-1].split('.')[1]}"

def download_img(pixiv_id):
    json_result = api.illust_detail(pixiv_id)
    illust = json_result.illust
    img_url = illust.meta_pages
    path_large =[]
    path_original =[]
    mkdir_gu = f"{PIXIV_PATH}/{illust.id}"
    #print(illust.meta_single_page)
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
        api.illust_bookmark_add(pixiv_id, restrict="public")
    except Exception as e:
        pass
    return file_data

def make_tags(tags):
    tag = ""
    for i in tags:
        tag += f"#{i['name']} "
    return tag

if __name__ == "__main__":
    print(download_img(105797544))
    #tag =  [{'name': 'オリジナル', 'translated_name': 'original'}, {'name': '女の子', 'translated_name': 'girl'}, {'name': '緑髪', 'translated_name': 'green hair'}, {'name': '天使', 'translated_name': 'angel'}, {'name': 'おっぱい', 'translated_name': 'breasts'}]
    #print(make_tags(tag))