import feedparser
import pickle
import os
import sys
import yaml

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    sys.exit()

#初始化检测
if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/rss_data") is False:
    os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}/rss_data")

RSS_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/rss_data/pixiv.rss"

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    sys.exit()
else:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)

# 订阅源的URL
RSS_URL = config["RSS_URL"]

def get_pixiv_rlid(url):
    return url.split("/")[-1]

def get_pixiv_rss():
    # 读取已经获取的文章
    try:
        with open(RSS_PATH, 'rb') as f:
            existing_articles = pickle.load(f)
    except (FileNotFoundError, EOFError):
        existing_articles = set()

    # 解析订阅源
    feed = feedparser.parse(RSS_URL)
    rss_list = []
    # 输出新闻标题和链接
    for entry in feed.entries:
        article_id = entry.link # 这里假设使用链接作为文章唯一标识符
        if article_id not in existing_articles:
            data={
                "title":entry.title,
                "pid":get_pixiv_rlid(entry.link),
                "link":entry.link
            }
            rss_list.append(data)
            existing_articles.add(article_id)

    # 保存获取的文章
    with open(RSS_PATH, 'wb') as f:
        pickle.dump(existing_articles, f)

    return rss_list

if __name__ == "__main__":
    print(get_pixiv_rss())
