#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10 10 7 10 * jd_yqhy.py
new Env('邀好友赢大礼');
入口类型：https://prodev.m.jd.com/mall/active/dVF7gQUVKyUcuSsVhuya5d2XD4F/index.html?code=xxxxxxxx&invitePin=xxxxxx
变量：export jd_inv_authorCode="5f29b7dbcfad44548b685a4d8d151e59"
"""

import requests, random, time, asyncio, re, os, sys, json
from datetime import datetime
from sendNotify import *
from urllib.parse import quote_plus, unquote_plus
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from functools import partial
print = partial(print, flush=True)


activatyname = '邀请赢大礼'
activityId = 'dVF7gQUVKyUcuSsVhuya5d2XD4F'  # 活动类型

authorCode = os.environ.get("jd_inv_authorCode") if os.environ.get("jd_inv_authorCode") else ""

if not authorCode:
    print("⚠️未发现有效活动变量jd_inv_authorCode,退出程序!")
    sys.exit()

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
# 检测ck状态
async def check(ua, ck):
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

# 获取当前时间
def get_time():
    time_now = round(time.time() * 1000)
    return time_now

# 登录plogin
async def plogin(ua, cookie):
    now = get_time()
    url = f'https://plogin.m.jd.com/cgi-bin/ml/islogin?time={now}&callback=__jsonp{now - 2}&_={now + 2}'
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'plogin.m.jd.com',
        'Referer': 'https://prodev.m.jd.com/',
        'User-Agent': ua
    }
    response = requests.get(url=url, headers=header, timeout=None).text
    return response

# 邀请排名
async def memberBringRanking(ua, cookie):
    t = get_time()
    body = {
        "code": authorCode,
        "pageNum": 1,
        "pageSize": 10
    }
    url = f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={t}&functionId=memberBringRanking&body={json.dumps(body)}&code={authorCode}&pageNum=1&pageSize=10"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://prodev.m.jd.com',
        'referer': 'https://prodev.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers).text
    print(response)
    return json.loads(response)

# 活动接口 new
async def memberBringActPage(ua, cookie):
    t = get_time()
    body = {
        "code": authorCode,
        "invitePin": invitePin,
        "_t": t
    }
    url = f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={t}&functionId=memberBringActPage&body={json.dumps(body)}&code={authorCode}&invitePin={invitePin}&_t={t}"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://prodev.m.jd.com',
        'referer': 'https://prodev.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers).text
    # print(response)
    return json.loads(response)

# go开卡 new
async def memberBringJoinMember(ua, cookie):
    t = get_time()
    body = {
        "code": authorCode,
        "invitePin": invitePin
    }
    url = f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={t}&functionId=memberBringJoinMember&body={json.dumps(body)}&code={authorCode}&invitePin={invitePin}"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://prodev.m.jd.com',
        'referer': 'https://prodev.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers).text
    return json.loads(response)

async def check_ruhui(body, cookie, venderId, ua):
    url = f'https://api.m.jd.com/client.action?appid=jd_shop_member&functionId=getShopOpenCardInfo&body={json.dumps(body)}&client=H5&clientVersion=9.2.0&uuid=88888'
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'User-Agent': ua,
        'Accept-Language': 'zh-cn',
        'Referer': f'https://shopmember.m.jd.com/shopcard/?venderId={venderId}&channel=801&returnUrl={json.dumps(activityUrl)}',
        'Accept-Encoding': 'gzip, deflate'
    }
    response = requests.get(url=url, headers=headers, timeout=None).text
    return json.loads(response)

# 领取奖励 new
async def memberBringInviteReward(cookie, ua, number):
    t = get_time()
    body = {
        "code": authorCode,
        "stage": number
    }
    url = f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t={t}&functionId=memberBringInviteReward&body={body}&code={authorCode}&stage={number}"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://prodev.m.jd.com',
        'referer': 'https://prodev.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers).text
    return json.loads(response)

# 开启活动
async def memberBringFirstInvite(cookie, ua):
    body = {
        "code": authorCode,
    }
    url = f"https://api.m.jd.com/api?client=&clientVersion=&appid=jdchoujiang_h5&t=1664407539127&functionId=memberBringFirstInvite&body={json.dumps(body)}&code={authorCode}"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://prodev.m.jd.com',
        'referer': 'https://prodev.m.jd.com/',
        'user-agent': ua
    }
    response = requests.request("GET", url, headers=headers).text
    return json.loads(response)

async def get_ck(data):
    cklist = []
    if data['code'] != 200:
        return {'code': 0, 'data': data}
    else:
        env_data = data['data']
        for ck in env_data:
            if 'remarks' in ck and ck['name'] == 'JD_COOKIE':
                cklist.append(ck['value'])
            else:
                pass
    return cklist

# 检查pin
def checkpin(cks: list, pin):
    for ck in cks:
        if pin in ck:
            return ck
        else:
            None

# 主程序
async def main():
    try:
        cks = get_cookies()
        if not cks:
            return
    except:
        print("未获取到有效COOKIE,退出程序！")
        return
    success = 0  # 计算成功数
    global invitePin, activityUrl, MSG
    MSG = ''
    title = "🗣消息提醒：邀好友赢大礼"
    r = re.compile(r"pt_pin=(.*?);")
    invitePin_ = r.findall(cks[0])[0] # 获取COOKIES中第一个车头pin
    inveteck = checkpin(cks, invitePin_)  # 根据设定的pin返回对应ck
    try:
        invitePin = remote_redis(f"invite_{authorCode}", 1)
        if not invitePin:
            invitePin = invitePin_
    except:
        invitePin = invitePin_
    activityUrl = f'https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}&invitePin={invitePin}'  # 活动链接
    needinviteNum = []  # 需要助力次数
    needdel = []
    need = []
    if inveteck:
        print(f"====================共{len(cks)}个京东账号Cookie=========\n")
        print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")   
        print(f"📝若已加入活动店铺会员,则无法助力。\n【🛳活动入口】https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}\n")
        ua = userAgent()  # 获取ua
        result = await check(ua, inveteck)  # 检测ck
        if result['code'] == 200:
            await plogin(ua, inveteck)  # 获取登录状态
            await asyncio.sleep(2)
            result = await memberBringActPage(ua, inveteck)  # 获取活动信息
            await memberBringFirstInvite(inveteck, ua)  # 开启活动
            if result['success']:
                brandName = result['data']['brandName']  # 店铺名字
                venderId = result['data']['venderId']  # 店铺入会id
                rewardslist = []  # 奖品
                rewardNameList = []
                successCount = result['data']['successCount']  # 当前成功数
                success += successCount
                result_data = result['data']['rewards']  # 奖品数据
                print(f'🤖您好！账号[{invitePin_}]\n✅开启{brandName}邀请好友活动\n去开活动')
                MSG += f'✅账号[{invitePin_}]\n开启{brandName}邀请好友活动\n📝活动地址https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}\n'
                for i in result_data:
                    stage = i['stage']
                    inviteNum = i['inviteNum']  # 单次需要拉新人数
                    need.append(inviteNum)
                    rewardName = i['rewardName']  # 奖品名
                    rewardNameList.append(rewardName)
                    rewardNum = i['rewardStock']
                    if rewardNum != 0:
                        needinviteNum.append(inviteNum)
                        needdel.append(inviteNum)
                    rewardslist.append(f'级别{stage}:  需助力{inviteNum}人，奖品: {rewardName}，库存：{rewardNum}件\n')
                if len(rewardslist) != 0:
                    print('🎁当前活动奖品如下: \n' + str('\n'.join(rewardslist)) + f'\n当前已助力{successCount}次\n')
                    MSG += f"🎁当前活动奖品如下: \n{str(''.join(rewardslist))}\n"
                    for numbers in needdel:
                        if success >= numbers:
                            print("🎉您当前助力已经满足了，可以去领奖励了")
                            print(f'\n📝这就去领取奖励{need.index(numbers) + 1}')
                            result = await memberBringInviteReward(inveteck, ua, need.index(numbers) + 1)
                            try:
                                if result['success']:
                                    print(f"🎉成功领取 {rewardNameList[need.index(numbers)]}")
                                    MSG += f"🎉成功领取 {rewardNameList[need.index(numbers)]}\n"
                                else:
                                    print(f"⛈{rewardNameList[need.index(numbers)]} {result['errorMessage']}")
                                    MSG += f"⛈{rewardNameList[need.index(numbers)]} {result['errorMessage']}\n"
                            except:
                                print(result)
                                MSG += f"{result}\n"
                            needinviteNum.remove(numbers)
                            await asyncio.sleep(10)
                    needdel = needinviteNum
                    if needinviteNum == []:
                        print('🎉🎉🎉奖励已经全部获取啦，退出程序')
                        MSG += f"🎉🎉🎉奖励已经全部获取啦~\n"
                        MSG = f"⏰{str(datetime.now())[:19]}\n" + MSG
                        send(title, MSG)
                        return
                for n, ck in enumerate(cks, 1):
                    ua = userAgent()  # 获取ua
                    try:
                        pin = re.findall(r'(pt_pin=([^; ]+)(?=;))', str(ck))[0]
                        pin = (unquote_plus(pin[1]))
                    except IndexError:
                        pin = f'用户{n}'
                    print(f'******开始【京东账号{n}】{pin} *********\n')
                    for i, numbers in enumerate(needinviteNum, 1):
                        for numbers in needdel:
                            if success >= numbers:
                                print(numbers)
                                print("🎉您当前助力已经满足了，可以去领奖励了")
                                print(f'\n📝这就去领取奖励{need.index(numbers) + 1}')
                                result = await memberBringInviteReward(inveteck, ua, need.index(numbers) + 1)
                                try:
                                    if result['success']:
                                        print(f"🎉成功领取 {rewardNameList[need.index(numbers)]}")
                                        MSG += f"🎉成功领取 {rewardNameList[need.index(numbers)]}\n"
                                    else:
                                        print(f"⛈{rewardNameList[need.index(numbers)]} {result['errorMessage']}")
                                        MSG += f"⛈{rewardNameList[need.index(numbers)]} {result['errorMessage']}\n"
                                except:
                                    print(result)
                                    MSG += f"{result}\n"
                                needinviteNum.remove(numbers)
                                await asyncio.sleep(10)
                        needdel = needinviteNum
                        if needinviteNum == []:
                            print('🎉🎉🎉奖励已经全部获取啦，退出程序')
                            MSG += f"🎉🎉🎉奖励已经全部获取啦~\n"
                            MSG = f"⏰{str(datetime.now())[:19]}\n" + MSG
                            send(title, MSG)
                            return
                    await plogin(ua, ck)  # 获取登录状态
                    result = await check(ua, ck)  # 检测ck
                    if n != 1:
                        invitePin = invitePin_
                        activityUrl = f'https://prodev.m.jd.com/mall/active/{activityId}/index.html?code={authorCode}&invitePin={invitePin}'
                    if result['code'] == 200:
                        result = await memberBringActPage(ua, ck)  # 调用ck
                        if result['success']:
                            print(f'✅账户[{pin}]已开启{brandName}邀请好友活动\n')
                            await asyncio.sleep(3)
                            result = await check_ruhui({"venderId": str(venderId), "channel": "401"}, ck, venderId,
                                                       ua)  # 检查入会状态
                            try:
                                if result['result']['userInfo']['openCardStatus'] == 0:  # 0 未开卡
                                    await asyncio.sleep(2)
                                    print(f'😆您还不是会员哦，这就去去助力{invitePin}\n')
                                    result = await memberBringJoinMember(ua, ck)
                                    if result['success']:
                                        success += 1
                                        print(f'🎉助力成功! 当前成功助力{success}个\n')
                                    else:
                                        if '交易失败' in str(result):
                                            success += 1
                                            print(f'🎉助力成功! 当前成功助力{success}个\n')
                                        else:
                                            try:
                                                print(f"⛈{result['errorMessage']}")
                                            except:
                                                print(result)
                                    await asyncio.sleep(2)
                                else:
                                    print('⛈您已经是会员啦，不去请求入会了\n')
                                    continue
                            except TypeError as e:
                                print(e)
                                result = await memberBringJoinMember(ua, ck)
                                if result['success']:
                                    success += 1
                                    print(f'🎉助力成功! 当前成功助力{success}个\n')
                                else:
                                    if '交易失败' in result:
                                        success += 1
                                        print(f'🎉助力成功! 当前成功助力{success}个\n')
                                    else:
                                        print(f"⛈{result['errorMessage']}")
                                await asyncio.sleep(2)
                            if n == 1:
                                await memberBringFirstInvite(inveteck, ua)  # 开启邀请

                        else:  # 没有获取到活动信息
                            print('未获取到活动参数信息\n')
                            break
                    else:
                        print(result['data'])
                        continue
            else:
                print('未能获取到活动信息\n')
                return

        else:
            print(result['data'])
            return
    else:
        print(f'pin填写有误，请重试')


if __name__ == "__main__":
    asyncio.run(main())