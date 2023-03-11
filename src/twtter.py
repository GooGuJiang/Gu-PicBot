import requests
import yaml
import sys
import os
from loguru import logger
import time
import re

current_dir = os.path.abspath(os.path.dirname(__file__))


TWTTER_PATH = f"{os.path.abspath(os.path.join(current_dir, os.pardir))}/data/twtter"

if os.path.exists(TWTTER_PATH) is False:
    os.mkdir(TWTTER_PATH)

if os.path.exists(f"{os.path.abspath(os.path.join(current_dir, os.pardir))}/data/config.yml") is False:
    sys.exit()
else:
    with open(f"{os.path.abspath(os.path.join(current_dir, os.pardir))}/data/config.yml","r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)



if config['PROXY_OPEN'] == True:
        proxy = {
            "http": config['PROXY'],
            "https": config['PROXY']
        }
else:
    proxy = None
# api auth token
authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
# api url
hostUrl = 'https://api.twitter.com/1.1/guest/activate.json'
singlePageApi = 'https://twitter.com/i/api/graphql/AkHczoaCocpQ_XO0hVM_-Q/TweetDetail'
userSearchApi = 'https://api.twitter.com/2/search/adaptive.json'
userInfoApi = 'https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults'
userLikesApi = 'https://api.twitter.com/graphql/aIE4yRZjJ_nNJlR7k9wQMw/Likes'
userFollowingApi = 'https://api.twitter.com/graphql/fzE3zNMTkr-CJufrDwjC4A/Following'
checkUpdateApi = 'https://api.github.com/repos/mengzonefire/twitter-media-downloader/releases/latest'

# api parameter
singlePageApiPar = '{{"focalTweetId":"{}","with_rux_injections":false,"includePromotedContent":false,"withCommunity":false,"withQuickPromoteEligibilityTweetFields":false,"withBirdwatchNotes":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true}}'
singlePageApiPar2 = '{"responsive_web_graphql_timeline_navigation_enabled":false,"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled":true,"dont_mention_me_view_api_enabled":true,"responsive_web_uc_gql_enabled":false,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":false,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}'
userSearchApiPar = '{{"include_profile_interstitial_type":1,"include_blocking":1,"include_blocked_by":1,"include_followed_by":1,"include_want_retweets":1,"include_mute_edge":1,"include_can_dm":1,"include_can_media_tag":1,"include_ext_has_nft_avatar":1,"include_ext_is_blue_verified":1,"include_ext_verified_type":1,"skip_status":1,"cards_platform":"Web-12","include_cards":1,"include_ext_alt_text":true,"include_ext_limited_action_results":false,"include_quote_count":true,"include_reply_count":1,"tweet_mode":"extended","include_ext_collab_control":true,"include_ext_views":true,"include_entities":true,"include_user_entities":true,"include_ext_media_color":true,"include_ext_media_availability":true,"include_ext_sensitive_media_warning":true,"include_ext_trusted_friends_metadata":true,"send_error_codes":true,"simple_quoted_tweet":true,"q":"{}","tweet_search_mode":"live","count":{},"query_source":"typed_query",{}"pc":1,"spelling_corrections":1,"include_ext_edit_control":true,"ext":"mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe"}}'
userInfoApiPar = '{{"screen_name":"{}","withHighlightedLabel":false}}'
userLikesApiPar = '{"userId":"{}","count":{},{},"includePromotedContent":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":true,"withV2Timeline":true}'
userFollowingApiPar = '{"userId":"{}","count":{},{}"includePromotedContent":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}'
commonApiPar = '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"responsive_web_graphql_exclude_directive_enabled":false,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}'

# re pattern
p_csrf_token = re.compile(r'ct0=(.+?)(?:;|$)')
pProxy = re.compile(r'.+?:\d+$')
pProxy2 = re.compile(r'(http|socks5)://(.+:.+@)?.+?:\d+$')
p_user_id = re.compile(r'"rest_id":"(\d+)"')
p_user_link = re.compile(
    r'https://twitter.com/([^/]+?)(?:/media|likes|following)?$')
p_twt_link = re.compile(r'https://twitter.com/(.+?)/status/(\d+)')


def extract_tweet_id(url):
    """
    从Twitter推文的URL中提取推文ID
    """
    # 从URL中提取最后一部分作为路径
    path = url.split('/')[-1]
    
    # 判断路径是否包含问号，如果包含则去掉问号及其后面的内容
    if '?' in path:
        path = path.split('?')[0]
    
    if path.isdigit():
        return {"status":True,"id":path}
    else:
        return {"status":False,"id":path}


def download_image(url, filepath,id):
    try:
        response = requests.get(url,proxies=proxy, timeout=60, verify=True)
        response.raise_for_status()  # 如果请求发生错误则抛出异常
        url_name = url.split('/')[-1].split('.')
        #print(f"{filepath}/{id}/{id}_{url_name[0]}.{url_name[1]}")
        with open(f"{filepath}/{id}/{id}_{url_name[0]}.{url_name[1]}", 'wb') as f:
            f.write(response.content)
        return {"status":True,"msg":f"{filepath}/{id}/{id}_{url_name[0]}.{url_name[1]}"}
    except Exception as e:
        logger.error(e)
        return {"status":False,"msg":e}

def getHeader():  # 获取游客token
    headers = {'authorization': authorization, 'Cookie': '', 'User-Agent': ''}
    if headers['Cookie']:  # 已配置cookie, 无需游客token
        return
    for i in range(1, 6):
        try:
            response = requests.post(hostUrl, proxies=proxy, headers=headers, timeout=5, verify=True).json()
            break
        except (requests.exceptions.Timeout, requests.exceptions.RequestException):
            #print(timeout_warning.format(i))
            time.sleep(1)
    if 'guest_token' in response:
        x_guest_token = response['guest_token']
        headers['x-guest-token'] = x_guest_token
        return headers
    else:
        return False

def getToken(cookie):
    csrf_token = p_csrf_token.findall(cookie)
    if len(csrf_token) != 0:
        return csrf_token[0]
    else:
        return None

def getTweet(pageContent, cursor=None, isfirst=False):
    if 'errors' in pageContent:
        message = pageContent['errors'][0]['message']
        print(f'推文已删除/不存在：{message}')
        return None, None
    elif 'globalObjects' in pageContent:  # 搜索接口
        entries = pageContent['globalObjects']['tweets'].values()
        if not entries and isfirst:
            print('\r请获取cookie')
        cursor = pageContent['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value'] \
            if len(entries) != 0 and pageContent['timeline']['instructions'][0]['addEntries']['entries'][-1]['entryId'] == 'sq-cursor-bottom' \
            else (pageContent['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']
                  if len(pageContent['timeline']['instructions']) != 1 and pageContent['timeline']['instructions'][-1]['replaceEntry']['entryIdToReplace'] == 'sq-cursor-bottom' else None)
    elif 'user' in pageContent['data']:
        result = pageContent['data']['user']['result']
        if result['__typename'] == 'UserUnavailable':
            #print(user_unavailable_warning)
            return None, None
        elif result['__typename'] == 'Age-restricted adult content':
           # print(age_restricted_warning)
            return None, None
        elif not result['timeline_v2']:
            #print(need_cookie_warning)
            return None, None
        instructions = result['timeline_v2']['timeline']['instructions']
        for instruction in instructions:
            if instruction['type'] == 'TimelineAddEntries':
                entries = instruction['entries']
                cursor = entries[-1]['content']['value'] if len(
                    entries) != 0 else None
                break
    elif 'threaded_conversation_with_injections_v2' in pageContent['data']:
        entries = pageContent['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']
    # 搜索接口返回的entries不包括cursor
    if len(entries) == 0 or len(entries) == 2 and 'entryId' in entries[-1] and 'cursor-bottom' in entries[-1]['entryId']:
        # 翻页完成, 无内容, 搜索/主页/媒体 接口的entries[-1]为cursor-bottom, [-2]为cursor-top
        return None, None
    tweets = []
    for tweet in entries:
        if 'entryId' in tweet and 'tweet-' in tweet['entryId']:
            tweets.append(tweet)
        elif 'entryId' not in tweet:
            tweets.append(tweet)
    return tweets, cursor

def get_twtter_media(tw_id:int):
    head = getHeader()
    #print('获取游客token成功')
    response = requests.get(singlePageApi, params={
                    'variables': singlePageApiPar.format(tw_id),
                    'features': singlePageApiPar2},
                    proxies=proxy,
                    headers=head,
                    timeout=10,
                    verify=True)
    get_date =getTweet(response.json(), cursor=None, isfirst=False)[0][0]
    media_path = []
    tw_tag = []
    get_media_json = get_date["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
    if len(get_media_json["entities"]["media"]) == 0:
        return {"status":False}
    dl_path = f"{TWTTER_PATH}/{tw_id}"
    if os.path.exists(dl_path) is False:
        os.mkdir(dl_path)
    for i in get_media_json["entities"]["media"]:
        if i["type"] == "photo":
            #print(i["media_url_https"])
            dl_st = download_image(i["media_url_https"],TWTTER_PATH,tw_id)
            if dl_st["status"] is True:
                media_path.append(dl_st["msg"])
    get_info = get_date["content"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"]["legacy"]
    for i in get_media_json["entities"]["hashtags"]:
        for k,v in i.items():
            if k == "text":
                tw_tag.append(f"#{v}")
    data={
        "tw_user_name":get_info["name"],
        "tw_user_url":f'https://twitter.com/{get_info["screen_name"]}',
        "tw_id":tw_id,
        "tw_text":get_media_json["full_text"],
        "tw_tag":tw_tag,
        "status":True,
        "media_path":media_path
    }
    return data

def make_tags(tags):
    tag = ""
    for i in tags:
        tag += f"{i} "
    return tag

import re

def remove_twitter_links_and_tags(text):
    """
    从字符串中删除所有的Twitter链接和话题标签
    """
    # 定义Twitter链接的正则表达式
    twitter_link_regex = r'https://t\.co/[^\s]+'
    
    # 定义话题标签的正则表达式
    hashtag_regex = r'#\S+\s*'
    
    # 使用正则表达式查找所有的Twitter链接和话题标签
    links_and_tags = re.findall(twitter_link_regex + '|' + hashtag_regex, text)
    
    # 逐个删除找到的链接和话题标签
    for link_or_tag in links_and_tags:
        text = text.replace(link_or_tag, '')
    
    return text


if __name__ == '__main__':
   print(get_twtter_media(1631683280507654146))
   