# -*- coding: utf8 -*-
import base64
import hashlib
import json
import random
import time
from urllib.parse import quote

import flask

server = flask.Flask(__name__)


# 食用方法
# 0. 容器内执行
# 1. pip3 install flask -i https://mirrors.ustc.edu.cn/pypi/web/simple
# 2. pm2 start signapi.py -x --interpreter python3
# 3. curl http://127.0.0.1:17840/sign ，确定sign正常运行，有结果输出
# 4. 添加变量 export M_API_SCAN_SIGN_URL="http://127.0.0.1:17840/sign"
# 5. 查看日志 pm2 log signapi


def bytes2bin(bytes):
    arr = []
    for v in [m for m in bytes]:
        arr.append(
            [(v & 128) >> 7, (v & 64) >> 6, (v & 32) >> 5, (v & 16) >> 4, (v & 8) >> 3, (v & 4) >> 2, (v & 2) >> 1,
             v & 1])
    print([i for j in arr for i in j])
    return [i for j in arr for i in j]


def bin2bytes(arr):
    length = len(arr) // 8
    arr1 = [0 for i in range(length)]
    for j in range(length):
        arr1[j] = arr[j * 8] << 7 | arr[j * 8 + 1] << 6 | arr[j * 8 + 2] << 5 | arr[j * 8 + 3] << 4 | arr[
            j * 8 + 4] << 3 | arr[j * 8 + 5] << 2 | arr[j * 8 + 6] << 1 | arr[j * 8 + 7]
    print(bytes(arr1))
    return bytes(arr1)


def sub_10EA4(input):
    table = [[0, 0], [1, 4], [2, 61], [3, 15], [4, 56], [5, 40], [6, 6], [7, 59], [8, 62], [9, 58], [10, 17], [11, 2],
             [12, 12], [13, 8], [14, 32], [15, 60], [16, 13], [17, 45], [18, 34], [19, 14], [20, 36], [21, 21],
             [22, 22], [23, 39], [24, 23], [25, 25], [26, 26], [27, 20], [28, 1], [29, 33], [30, 46], [31, 55],
             [32, 35], [33, 24], [34, 57], [35, 19], [36, 53], [37, 37], [38, 38], [39, 5], [40, 30], [41, 41],
             [42, 42], [43, 18], [44, 47], [45, 27], [46, 9], [47, 44], [48, 51], [49, 7], [50, 49], [51, 63], [52, 28],
             [53, 43], [54, 54], [55, 52], [56, 31], [57, 10], [58, 29], [59, 11], [60, 3], [61, 16], [62, 50],
             [63, 48]]
    arr = bytes2bin(input)
    arr1 = [0 for i in range(len(arr))]
    for i in range(len(table)):
        arr1[table[i][1]] = arr[table[i][0]]
    print(arr1)
    return bin2bytes(arr1)


def sub_4B7C(input):
    table = [[0, 6, 0, 1], [1, 4, 1, 0], [2, 5, 0, 1], [3, 0, 0, 1], [4, 2, 0, 1], [5, 3, 0, 1], [6, 1, 1, 0],
             [7, 7, 0, 1]]
    arr = bytes2bin(input)
    arr1 = [0 for i in range(8)]
    for i in range(8):
        if arr[i] == 0:
            arr1[table[i][1]] = table[i][2]
        else:
            arr1[table[i][1]] = table[i][3]
    print(arr1)
    return bin2bytes(arr1)


def sub_10D70(input):
    if len(input) == 1:
        return sub_4B7C(input)


def sub_v1(input):
    output = bytes()
    for i in range(len(input) // 8):
        output += sub_10EA4(input[i * 8:(i + 1) * 8])
    output += sub_10D70(input[-(len(input) % 8):])
    return output


def sub_v2(input):
    arr = [0x37, 0x92, 0x44, 0x68, 0xA5, 0x3D, 0xCC, 0x7F, 0xBB, 0xF, 0xD9, 0x88, 0xEE, 0x9A, 0xE9, 0x5A]
    key2 = b"80306f4370b39fd5630ad0529f77adb6"
    arr1 = [0 for _ in range(len(input))]
    for i in range(len(input)):
        r0 = int(input[i])
        r2 = arr[i & 0xf]
        r4 = int(key2[i & 7])
        r0 = r2 ^ r0
        r0 = r0 ^ r4
        r0 = r0 + r2
        r2 = r2 ^ r0
        r1 = int(key2[i & 7])
        r2 = r2 ^ r1
        arr1[i] = r2 & 0xff
    return bytes(arr1)


def sub_126AC(input, random1, random2):
    arr = [0, 1, 2]
    if random2 == 1:
        arr = [1, 2, 0]
    if random2 == 2:
        arr = [2, 0, 1]
    version = arr[random1]
    if version == 0:
        return sub_v1(input)
    if version == 2:
        return sub_v2(input)


def base64Encode(string):
    oldBin = ""
    tempStr = []
    result = ""
    base64_list = 'KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/'
    for ch in string:
        oldBin += "{:08}".format(int(str(bin(ord(ch))).replace("0b", "")))
    for i in range(0, len(oldBin), 6):
        tempStr.append("{:<06}".format(oldBin[i:i + 6]))
    for item in tempStr:
        result = result + base64_list[int(item, 2)]
    if len(result) % 4 == 2:
        result += "=="
    elif len(result) % 4 == 3:
        result += "="
    return result


def base64Decode(string):
    result = []
    string = string.strip("=")
    binstr = ""
    bin6list = []
    bin8list = []
    base64_list = "KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/"
    for ch in string:
        bin6list.append("{:>06}".format(str(bin(base64_list.index(ch)).replace("0b", ""))))
    binstr = "".join(bin6list)
    for i in range(0, len(binstr), 8):
        bin8list.append(binstr[i:i + 8])
    for item in range(len(bin8list) - 1):
        result.append(chr(int(bin8list[item], 2)))
    return "".join(result)


def get_sign(functionId, body, uuid, client, clientVersion):
    st = str(int(time.time()) * 1000)
    version = [[0, 2], [1, 1], [2, 0]]
    r1r2 = random.choice(version)
    r1 = r1r2[0]
    r2 = r1r2[1]
    sv = "1%s%s" % (r1, r2)
    input = "functionId=%s&body=%s&uuid=%s&client=%s&clientVersion=%s&st=%s&sv=%s" % (
        functionId, body, uuid, client, clientVersion, st, sv)
    ret_bytes = sub_126AC(str.encode(input), r1, r2)
    sign = hashlib.md5(base64.b64encode(ret_bytes)).hexdigest()
    return sv, st, sign


def task(func_id, body_json):
    body_str = (body_json).strip()
    client = "android"
    client_version = "10.4.0"
    uuid = ''.join(random.sample('0123456789abcdef0123456789abcdef0123456789abcdef', 40))
    d_model = random.choice(
        ["HUAWEI(NOH-AN00)", "Xiaomi(MI 9 Transparent Edition)", "Meizu(16T)", "HTC U-3w", "Redmi K20 Pro Premium Edition"])
    osVersion = random.choice(["10", "11", "12"])
    area = ''.join(random.sample('0123456789', 2)) + '_' + ''.join(random.sample('0123456789', 4)) + '_' + ''.join(
        random.sample('0123456789', 5)) + '_' + ''.join(random.sample('0123456789', 4))
    wifiBssid = "TP_LINK_".join(random.sample('0123456789ABCDEFG', 6))
    screen = random.choice(["640x1136", "750x1334", "1080x1920"])
    randomeid = ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 20))
    eid = f'eidAaf8081218as20a2GM${randomeid}7FnfQYOecyDYLcd0rfzm3Fy2ePY4UJJOeV0Ub840kG8C7lmIqt3DTlc11fB/s4qsAP8gtPTSoxu'
    ext = quote('{"prstate":"0","pvcStu":"1"}')

    sv, st, sign = get_sign(func_id, body_str, uuid, client, client_version)

    ep = json.dumps({
        "hdid": "JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=",
        "ts": st,
        "ridx": -1,
        "cipher": {"screen": base64Encode(screen), "wifiBssid": base64Encode(wifiBssid), "osVersion": base64Encode(osVersion),
                   "area": base64Encode(area), "openudid": base64Encode(uuid), "uuid": base64Encode(uuid)},
        "ciphertype": 5,
        "version": "1.0.3",
        "appname": "com.360buy.jdmobile",
    }).replace(" ", "")

    body_str = quote(body_str)
    ep = quote(ep)
    data_str = f"body={body_str}&build=168069&client={client}&clientVersion={client_version}&d_brand=android&d_model={d_model}&ef=1&eid={eid}&ep={ep}&ext={ext}&isBackground=N&joycious=124&lang=zh_CN&networkType=wifi&networklibtype=JDNetworkBaseAF&partner=android&rfs=0000&scope=11&st={st}&sv={sv}&sign={sign}"
    return {"fn": func_id, "body": data_str}


@server.route('/sign', methods=['post'])
def sign():
    try:
        data = flask.request.data
        data = json.loads(data.decode('utf-8'))
        data = task(data['fn'], json.dumps(data['body']))
        return data
    except Exception as e:
        print(e)
        return 'sign error'


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=17840)