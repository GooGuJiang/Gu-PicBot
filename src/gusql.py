import sqlite3
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

DATA_DB =f'{os.path.abspath(os.path.join(current_dir, os.pardir))}/data/bot_data.db'

def oneload_sql_db():
    try:
        if not os.path.exists(f"{os.path.abspath(os.path.join(current_dir, os.pardir))}/data"):
            os.mkdir(f"{os.path.abspath(os.path.join(current_dir, os.pardir))}/data")

        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        # Create the table to store image data (if it doesn't exist)
        c.execute('''CREATE TABLE IF NOT EXISTS pixiv_images
                    (id INTEGER PRIMARY KEY,
                    pid INTEGER,
                    file_size INTEGER,
                    file_path TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS rss_data
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        pid TEXT,
                        link TEXT,
                        UNIQUE(link))''')
        c.execute('''CREATE TABLE IF NOT EXISTS pixiv_tg_id
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                pixiv_id INTEGER NOT NULL);''')
        conn.execute('''CREATE TABLE IF NOT EXISTS twtter_tg_id
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                twitter_id INTEGER NOT NULL);''')
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def pixiv_tg_id_add(tg_message_id,pixiv_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute('INSERT INTO pixiv_tg_id (telegram_id, pixiv_id) VALUES (?, ?)', (tg_message_id,pixiv_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_tg_pixiv_message_id(pixiv_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("SELECT telegram_id FROM pixiv_tg_id WHERE pixiv_id = ?", (pixiv_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return False
    except Exception as e:
        return False

def pixiv_tg_id_del(tg_message_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("DELETE FROM pixiv_tg_id WHERE telegram_id = ?", (tg_message_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False
    
def pixiv_tg_id_del_by_pixiv_id(pixiv_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("DELETE FROM pixiv_tg_id WHERE pixiv_id = ?", (pixiv_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def twtter_tg_id_add(tg_message_id,twtter_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute('INSERT INTO twtter_tg_id (telegram_id, twitter_id) VALUES (?, ?)', (tg_message_id,twtter_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_tg_message_id_by_twitter_id(twitter_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("SELECT telegram_id FROM twtter_tg_id WHERE twitter_id = ?", (twitter_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return False
    except Exception as e:
        return False

def twtter_tg_id_del(tg_message_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("DELETE FROM twtter_tg_id WHERE telegram_id = ?", (tg_message_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def twtter_tg_id_del_by_twitter_id(twitter_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("DELETE FROM twtter_tg_id WHERE twitter_id = ?", (twitter_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    print( get_tg_pixiv_message_id(105858621))
    print("Done")
