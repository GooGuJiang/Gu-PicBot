import feedparser
import sqlite3
import os
import sys
import yaml

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    sys.exit()

#初始化检测
if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/data") is False:
    os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}/data")

DB_PATH = f'{os.path.dirname(os.path.abspath(__file__))}/data/bot_data.db'

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
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Read existing article IDs from the database
    c.execute('SELECT link FROM rss_data')
    existing_articles = set(link for (link,) in c.fetchall())

    rss_list = []
    # Parse the RSS feed
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries:
        article_id = entry.link
        if article_id not in existing_articles:
            # Fetch the pixiv ID from the article link
            pid = get_pixiv_rlid(entry.link)
            # Add the new RSS data to the list
            data = (entry.title, pid, entry.link)
            rss_list.append(data)
            existing_articles.add(article_id)

    # Insert the new RSS data into the database
    c.executemany('INSERT OR IGNORE INTO rss_data (title, pid, link) VALUES (?, ?, ?)', rss_list)
    conn.commit()

    # Close the database connection
    conn.close()

    return rss_list

def pid_in_database(pid):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if the given pid is already in the database
    c.execute('SELECT COUNT(*) FROM rss_data WHERE pid = ?', (pid,))
    result = c.fetchone()

    # Close the database connection
    conn.close()

    # If result is not None and the count is > 0, then the pid is in the database
    return result is not None and result[0] > 0

if __name__ == "__main__":
    print(get_pixiv_rss())
