# -*- coding: utf-8 -*-
"""接口探测脚本：把候选场景的真实响应一次性打出来，供用例设计使用。
文件名不带 test_ 前缀，pytest 不会收集它。
"""
import requests
from config import BASE_URL, USERNAME, PASSWORD

# ===== 1. 登录拿 token =====
login = requests.post(BASE_URL + "/wx/auth/login",
                      json={"username": USERNAME, "password": PASSWORD}).json()
token = login["data"]["token"]
H = {"X-Litemall-Token": token}


def show(label, resp):
    """打印一条探测结果：标签 + errno + errmsg"""
    try:
        d = resp.json()
    except ValueError:
        print("%-26s [非JSON] HTTP %s" % (label, resp.status_code))
        return
    print("%-26s errno=%-6s errmsg=%s" % (label, d.get("errno"), d.get("errmsg")))


# ===== 2. 商品模块 =====
r = requests.get(BASE_URL + "/wx/goods/list", headers=H)
show("商品列表-默认", r)
first_id = r.json()["data"]["list"][0]["id"]
print("（下面用的商品 id = %s）" % first_id)
print("-" * 62)

show("商品列表-limit=1", requests.get(
    BASE_URL + "/wx/goods/list", headers=H, params={"limit": 1}))
show("商品列表-page=9999", requests.get(
    BASE_URL + "/wx/goods/list", headers=H, params={"page": 9999}))
show("商品列表-sort=abc", requests.get(
    BASE_URL + "/wx/goods/list", headers=H, params={"sort": "abc"}))
show("商品列表-关键字无结果", requests.get(
    BASE_URL + "/wx/goods/list", headers=H, params={"keyword": "zzzz不存在"}))
show("商品详情-正常", requests.get(
    BASE_URL + "/wx/goods/detail", headers=H, params={"id": first_id}))
show("商品详情-id不存在", requests.get(
    BASE_URL + "/wx/goods/detail", headers=H, params={"id": 99999999}))
show("商品详情-不传id", requests.get(
    BASE_URL + "/wx/goods/detail", headers=H))

# ===== 3. 订单模块 =====
print("-" * 62)
show("订单详情-正常", requests.get(
    BASE_URL + "/wx/order/detail", headers=H, params={"orderId": 1}))
show("订单详情-id不存在", requests.get(
    BASE_URL + "/wx/order/detail", headers=H, params={"orderId": 999}))

# ===== 4. 鉴权 =====
print("-" * 62)
show("订单列表-不带token", requests.get(
    BASE_URL + "/wx/order/list", headers={}))
show("订单列表-乱码token", requests.get(
    BASE_URL + "/wx/order/list", headers={"X-Litemall-Token": "abc123"}))

# ===== 5. 登录异常 =====
print("-" * 62)
show("登录-密码错", requests.post(
    BASE_URL + "/wx/auth/login", json={"username": USERNAME, "password": "wrong123"}))
show("登录-用户名不存在", requests.post(
    BASE_URL + "/wx/auth/login", json={"username": "nobody999", "password": PASSWORD}))
