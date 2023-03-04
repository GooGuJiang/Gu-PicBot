import os
import sys
import yaml
from loguru import logger

if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml") is False:
    try:
        data={
            "REFRESH_TOKEN":"",
            "RSS_URL":"",
            "BOT_TOKEN":"",
            "CHANNEL_ID":"",
            "BOT_ADMIN":[""],
            "RSS_SECOND":60,
            "PROXY":"socks5://127.0.0.1:8089",
            "PROXY_OPEN":False,
            "RSS_OPEN":True
        }
        #print(yaml.dump(data=data))
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","w+") as c:
            c.write(yaml.dump(data=data,Dumper=yaml.CDumper))
        #logger.success("Config file created successfully, please fill in the configuration information and restart the program.")
        logger.success("配置文件创建成功，请填写配置信息后重启程序。")
        sys.exit()
    except Exception as e:
        #logger.error("Failed to create config file, please check the permissions.")
        logger.error(f"创建配置文件失败，请检查权限。\n{e}")
        sys.exit()

def check_config():
    #检查配置文件填写是否正确
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)
    if config['REFRESH_TOKEN'] == "":
        #logger.error("REFRESH_TOKEN is not configured, please fill in the configuration information and restart the program.")
        logger.error("REFRESH_TOKEN未配置,请填写配置信息后重启程序。")
        sys.exit()
    elif config['BOT_TOKEN'] == "":
        #logger.error("BOT_TOKEN is not configured, please fill in the configuration information and restart the program.")
        logger.error("BOT_TOKEN未配置,请填写配置信息后重启程序。")
        sys.exit()
    elif config['CHANNEL_ID'] == "":
        #logger.error("BOT_CHANNEL is not configured, please fill in the configuration information and restart the program.")
        logger.error("BOT_CHANNEL未配置,请填写配置信息后重启程序。")
        sys.exit()
    elif config['BOT_ADMIN'] == [""]:
        #logger.error("BOT_ADMIN is not configured, please fill in the configuration information and restart the program.")
        logger.error("BOT_ADMIN未配置,请填写配置信息后重启程序。")
        sys.exit()
    elif config['PROXY_OPEN'] == "":
        #logger.error("PROXY_OPEN is not configured, please fill in the configuration information and restart the program.")
        logger.error("PROXY_OPEN未配置,请填写配置信息后重启程序。")
        sys.exit()
    elif config['PROXY_OPEN'] == True:
        if config['PROXY'] == "":
            #logger.error("PROXY is not configured, please fill in the configuration information and restart the program.")
            logger.error("PROXY未配置,请填写配置信息后重启程序。")
            sys.exit()
    elif config['RSS_OPEN'] == True:
        if config['RSS_URL'] == "":
            #logger.error("RSS_URL is not configured, please fill in the configuration information and restart the program.")
            logger.error("RSS_URL未配置,请填写配置信息后重启程序。")
            sys.exit()
        elif config['RSS_SECOND'] == "":
            #logger.error("RSS_SECOND is not configured, please fill in the configuration information and restart the program.")
            logger.error("RSS_SECOND未配置,请填写配置信息后重启程序。")
            sys.exit()
    
    logger.success("配置检测通过!")

if __name__ == "__main__":
    check_config()