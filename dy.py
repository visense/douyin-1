# coding: utf-8
from __future__ import print_function
import re
import requests
import w3lib
from parsel import Selector
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
try:
    from urllib.parse import urljoin
except ImportError:
    from six.moves.urllib.parse import urljoin


def download(url, proxy=None, rain_num=2):
    print("dowing", url)
    heads = {
        'Accept': 'text/*, application/xml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Mobile Safari/537.36',
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.douyin.com",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        html = requests.get(url, headers=heads).text
    except Exception as e:
        print("Downing error", e.reason)
        html = None
        if rain_num > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, rain_num - 1)
    return html


def spider(uid):
    url = "https://www.douyin.com/share/user/%s" % uid
    body = download(url)
    xbody = Selector(text=body)
    item = dict()

    nick_name = xbody.xpath("//p[@class='nickname']/text()").extract_first()
    print(nick_name)

    works = xbody.xpath("//div[@class='user-tab active tab get-list']/span").extract_first()
    works = re.findall('>([\s\S]+?)<', works)
    works = jiexi(works).strip()

    like_num = xbody.xpath("//div[@class='like-tab tab get-list']/span").extract_first()
    like_num = re.findall('>([\s\S]+?)<', like_num)
    like_num = jiexi(like_num).strip()

    douyin_id = xbody.xpath("//p[@class='shortid']").extract_first()
    douyin_id = re.findall('>([\s\S]+?)<', douyin_id)
    douyin_id = jiexi(douyin_id).replace(u"抖音ID：", '').strip()
    try:
        info = xbody.xpath("//span[@class='info']/text()").extract_first().strip()
    except Exception as e:
        info = ''
    guanzhu = xbody.xpath("//span[contains(@class,'focus block')]/span[@class='num']").extract_first()
    guanzhu = re.findall('>([\s\S]+?)<', guanzhu)
    guanzhu = jiexi(guanzhu)

    fans = xbody.xpath("//span[contains(@class,'follower block')]/span[@class='num']").extract_first()
    fans = re.findall('>([\s\S]+?)<', fans)
    fans = jiexi(fans)

    zan = xbody.xpath("//span[contains(@class,'liked-num block')]/span[@class='num']").extract_first()
    zan = re.findall('>([\s\S]+?)<', zan)
    zan = jiexi(zan)

    item['douyin_id'] = douyin_id
    item['nick_name'] = nick_name
    item["fans"] = fans
    item["zan"] = zan
    item["guanzhu"] = guanzhu
    item['works'] = works
    item['like_num'] = like_num
    item['info'] = info
    print(item)


def jiexi(lists):
    pat = {
        u"\ue60d": 0,
        u"\ue603": 0,
        u"\ue616": 0,
        u"\ue60e": 1,
        u"\ue618": 1,
        u"\ue602": 1,
        u"\ue605": 2,
        u"\ue610": 2,
        u"\ue617": 2,
        u"\ue611": 3,
        u"\ue604": 3,
        u"\ue61a": 3,
        u"\ue606": 4,
        u"\ue619": 4,
        u"\ue60c": 4,
        u"\ue60f": 5,
        u"\ue607": 5,
        u"\ue61b": 5,
        u"\ue61f": 6,
        u"\ue612": 6,
        u"\ue608": 6,
        u"\ue61c": 7,
        u"\ue60a": 7,
        u"\ue613": 7,
        u"\ue60b": 8,
        u"\ue61d": 8,
        u"\ue614": 8,
        u"\ue615": 9,
        u"\ue61e": 9,
        u"\ue609": 9,
        "w": "w",
        ".": "."
    }
    _li = list()
    for i in lists:
        if str(i).strip():
            i = i.replace(u'<i class="icon iconfont follow-num">', "").strip()
            i = i.replace(u'<i class="icon iconfont ">', "").strip()
            i = i.replace(u'<i class="icon iconfont tab-num">', "").strip()
            i = pat.get(i, i)
            _li.append(str(i))
    return "".join(_li)


if __name__ == '__main__':
    uids = [
        "57720812347", "93046013277", "72096309936", "60637177764", "69914084602", "72722865756", "58486060366", "95433824498",
        "77267568314", "52616983119", "61141281259", "58900737309"
    ]
    for uid in uids:
        spider(uid)