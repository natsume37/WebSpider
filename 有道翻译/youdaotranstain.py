import json
import time

import execjs
import requests

headers = {
    "host": "dict.youdao.com",
    "origin": "https://fanyi.youdao.com",
    "pragma": "no-cache",
    "referer": "https://fanyi.youdao.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
# e = "asdjnjfenknafdfsdfsd"
# t = int(round(time.time() * 1000))


def obj_js():
    with open('test.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        ctx = execjs.compile(js_code)
        return ctx


def get_jiemi_txt(e, key, iv):
    ctx = obj_js()
    res = ctx.call('data', e, key, iv)
    return res


def get_sign(e, t):
    ctx = obj_js()
    sign = ctx.call('k', e, t)
    # print("sign：", sign)
    return sign


def get_time_now():
    return int(round(time.time() * 1000))


def getKey():
    e = "asdjnjfenknafdfsdfsd"
    t = get_time_now()
    sign = get_sign(e, t)
    try:
        response = requests.get(
            f"https://dict.youdao.com/webtranslate/key?keyid=webfanyi-key-getter&sign={sign}&client=fanyideskweb&product=webfanyi&appVersion=1.0.0&vendor=web&pointParam=client,mysticTime,product&mysticTime={t}&keyfrom=fanyi.web&mid=1&screen=1&model=1&network=wifi&abtest=0&yduuid=abcdefg",
            headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        secretKey = data['data']['secretKey']
        aesKey = data['data']['aesKey']
        aesIv = data['data']['aesIv']
        return secretKey, aesKey, aesIv
    except requests.exceptions.RequestException as err:
        print(f"获取密钥失败: {err}")
        return None
    except (json.JSONDecodeError, KeyError) as err:
        print(f"解析密钥响应失败: {err}")
        return None


def getMitext():
    key_info = getKey()
    if key_info is None:
        raise "key_ingo 为空"# 或者抛出异常
    e, aeskey, aesiv = key_info
    t = get_time_now()
    sign = get_sign(e, t)
    txt = input(">>> ")

    data = {
        'i': f'{txt}',
        'from': 'auto',
        'to': '',
        'useTerm': 'false',
        'domain': '0',
        'dictResult': 'true',
        'keyid': 'webfanyi',
        'sign': f'{sign}',
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': f'{t}',
        'keyfrom': 'fanyi.web',
        'mid': '1',
        'screen': '1',
        'model': '1',
        'network': 'wifi',
        'abtest': '0',
        'yduuid': 'abcdefg',
    }
    url = "https://dict.youdao.com/webtranslate"
    try:
        aestxt_response = requests.post(url, headers=headers, data=data)
        aestxt_response.raise_for_status()
        return aestxt_response, aeskey, aesiv
    except requests.exceptions.RequestException as err:
        print(f"获取翻译结果失败: {err}")
        return None, None, None


def out_txt():
    result = getMitext()
    if result is None or any(item is None for item in result):
        print("获取加密文本或密钥信息失败，无法进行解密。")
        return None

    aestxt_response, aeskey, aesiv = result
    print("加密文本响应:", aestxt_response)
    aestxt = aestxt_response.text
    res = get_jiemi_txt(aestxt, aeskey, aesiv)
    if res:
        try:
            res_json = json.loads(res)
            print("解密结果:", res_json)
            return res_json
        except json.JSONDecodeError as e:
            print(f"JSON解码错误: {e}")
            print(f"原始解密文本: {res}")
            return None
    else:
        print("解密文本为空")
        return None


if __name__ == '__main__':
    while True:
        out_txt()