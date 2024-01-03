#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: jd_dpcj.py(店铺抽奖-JK)
Author: HarbourJ
Date: 2022/10/15 23:00
TG: https://t.me/HarbourToulu
TgChat: https://t.me/HarbourChat
cron: 1 1 1 1 1 1
new Env('店铺抽奖-JK');
ActivityEntry：https://shop.m.jd.com/shop/lottery?shopId=xxxxx&venderId=xxxxx
Description: 变量：export DPCJID="shopId1&shopId2" #变量为店铺🆔
"""

import requests, time, re, os, sys, json, random
from datetime import datetime
from sendNotify import *
from urllib.parse import quote_plus, unquote_plus
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from functools import partial
print = partial(print, flush=True)

def userAgent():
    global uuid, addressid, iosVer, iosV, clientVersion, iPhone, area, ADID, lng, lat
    uuid = ''.join(random.sample(
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'z'], 40))
    addressid = ''.join(random.sample('1234567898647', 10))
    iosVer = ''.join(random.sample(["15.1.1", "14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1"], 1))
    iosV = iosVer.replace('.', '_')
    clientVersion = ''.join(random.sample(["10.3.0", "10.2.7", "10.2.4"], 1))
    iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
    area = ''.join(random.sample('0123456789', 2)) + '_' + ''.join(random.sample('0123456789', 4)) + '_' + ''.join(
        random.sample('0123456789', 5)) + '_' + ''.join(random.sample('0123456789', 4))
    ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
        random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
        random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
    lng = '119.31991256596' + str(random.randint(100, 999))
    lat = '26.1187118976' + str(random.randint(100, 999))
    UserAgent = ''
    if not UserAgent:
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    else:
        return UserAgent

def get_cookies():
    CookieJDs = []
    if os.environ.get("JD_COOKIE"):
        print("已获取并使用Env环境 Cookie")
        if '&' in os.environ["JD_COOKIE"]:
            CookieJDs = os.environ["JD_COOKIE"].split('&')
        elif '\n' in os.environ["JD_COOKIE"]:
            CookieJDs = os.environ["JD_COOKIE"].split('\n')
        else:
            CookieJDs = [os.environ["JD_COOKIE"]]
        # return CookieJDs
    else:
        if os.path.exists("JD_COOKIE.txt"):
            with open("JD_COOKIE.txt", 'r') as f:
                JD_COOKIEs = f.read().strip()
                if JD_COOKIEs:
                    if '&' in JD_COOKIEs:
                        CookieJDs = JD_COOKIEs.split('&')
                    elif '\n' in JD_COOKIEs:
                        CookieJDs = JD_COOKIEs.split('\n')
                    else:
                        CookieJDs = [JD_COOKIEs]
                    CookieJDs = sorted(set(CookieJDs), key=CookieJDs.index)
                    # return CookieJDs
        else:
            print("未获取到正确✅格式的京东账号Cookie")
            return
    return CookieJDs

dpcj = os.environ.get("DPCJID") if os.environ.get("DPCJID") else ""

if not dpcj:
    print("⚠️未发现有效店铺签到活动变量DPCJID,退出程序!")
    sys.exit()

def check(ua, ck):
    try:
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
        header = {
            "Host": "me-api.jd.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Cookie": ck,
            "User-Agent": ua,
            "Accept-Language": "zh-cn",
            "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
            "Accept-Encoding": "gzip, deflate",
        }
        result = requests.get(url=url, headers=header, timeout=None).text
        codestate = json.loads(result)
        if codestate['retcode'] == '1001':
            msg = "⚠️当前ck已失效，请检查"
            return {'code': 1001, 'data': msg}
        elif codestate['retcode'] == '0' and 'userInfo' in codestate['data']:
            nickName = codestate['data']['userInfo']['baseInfo']['nickname']
            return {'code': 200, 'name': nickName, 'ck': ck}
    except Exception as e:
        return {'code': 0, 'data': e}

def get_time():
    time_now = round(time.time() * 1000)
    return time_now

def getSignInfo(ua, ck, shopId, venderId):
    url = f"https://api.m.jd.com/client.action?functionId=whx_getSignInfo&body=%7B%22shopId%22%3A%22{shopId}%22%2C%22venderId%22%3A%22{venderId}%22%2C%22source%22%3A%22m-shop%22%7D&t=1665848303470&appid=shop_view&clientVersion=11.0.0&client=wh5&area=1_88_2888_8&uuid=16587341419872043913507"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': ck,
        'origin': 'https://shop.m.jd.com',
        'referer': 'https://shop.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers)
    res = response.json()
    return res

def sign(ua, ck, shopId, venderId):
    url = f"https://api.m.jd.com/client.action?functionId=whx_sign&body=%7B%22shopId%22%3A%22{shopId}%22%2C%22venderId%22%3A%22{venderId}%22%2C%22source%22%3A%22m-shop%22%7D&t=1665847166130&appid=shop_view&clientVersion=11.0.0&client=wh5&area=1_88_2888_8&uuid=16587341419872043913507"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': ck,
        'origin': 'https://shop.m.jd.com',
        'referer': 'https://shop.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers)
    res = response.json()
    return res

def get_venderId(ua, ck, shopId):
    url = f'https://api.m.jd.com/client.action?functionId=whx_getMShopOutlineInfo&body=%7B%22shopId%22%3A%22{shopId}%22%2C%22source%22%3A%22m-shop%22%7D&appid=shop_view&clientVersion=11.0.0&client=wh5'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://shop.m.jd.com',
        'referer': 'https://shop.m.jd.com/',
        'user-agent': ua,
        'cookie': ck
    }
    response = requests.request("GET", url, headers=headers)
    res = response.json()
    try:
        if res['success']:
            venderId = res['data']['shopInfo']['venderId']
            return venderId
        else:
            return shopId
    except:
        return


if __name__ == "__main__":
    global msg
    msg = ''
    shopIds = dpcj.split('&')
    print(f"✅成功获取{len(shopIds)}个DPCJ🆔变量")
    try:
        cks = get_cookies()
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    num = 0
    for cookie in cks:
        num += 1
        if num % 9 == 0:
            print("⏰等待3s,休息一下")
            time.sleep(3)
        ua = userAgent()
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
            pt_pin = unquote_plus(pt_pin)
        except IndexError:
            pt_pin = f'用户{num}'
        print(f'\n******开始【京东账号{num}】{pt_pin} *********\n')
        print(datetime.now())

        result = check(ua, cookie)
        if result['code'] != 200:
            print(f"‼️{result['data']}")
            continue
        signRewards = []
        for shopId in shopIds:
            print(f"{shopId}")
            venderId = get_venderId(ua, cookie, shopId)
            time.sleep(0.2)
            if not venderId:
                continue
            signInfo = getSignInfo(ua, cookie, shopId, venderId)
            time.sleep(0.2)
            try:
                if signInfo['isSuccess']:
                    try:
                        signInfo_ = signInfo['result']['result']['signInfo']
                    except:
                        print(f"\t⛈店铺抽奖已过期")
                        continue
                    if signInfo_['isSign'] == 2:
                        print(f"\t⛈店铺已抽奖")
                    else:
                        toSign = sign(ua, cookie, shopId, venderId)
                        if toSign['isSuccess']:
                            if toSign['result']['result']['isWin']:
                                signReward = toSign['result']['result']['signReward']['name']
                                print(f"\t🎉{signReward}")
                                if "东券" in signReward or "购原价" in signReward:
                                    continue
                                signRewards.append(signReward)
                            else:
                                print("\t💨💨💨")
            except:
                continue
            # time.sleep(0.3)
        if signRewards:
            price = ','.join(signRewards)
            msg += f'【账号{num}】{pt_pin} 🎉{price}\n'

        time.sleep(0.5)

    title = "🗣消息提醒：店铺抽奖-JK"
    msg = f"⏰{str(datetime.now())[:19]}\n" + msg
    send(title, msg)