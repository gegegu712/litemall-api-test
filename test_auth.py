import allure
import pytest
import requests

from config import BASE_URL, USERNAME, PASSWORD

# 登录失败用例：(标题, 用户名, 密码, 预期errno)
LOGIN_FAIL_CASES = [
    ("密码错误返回账号密码不对", USERNAME, "wrong123", 700),
    ("用户名不存在返回账号不存在", "nobody999", PASSWORD, 700),
]

# 鉴权用例：(标题, 请求头)
AUTH_CASES = [
    ("不带 token 访问订单列表被拦截", {}),
    ("token 无效访问订单列表被拦截", {"X-Litemall-Token": "abc123"}),
]


@allure.feature("登录模块")
@allure.story("登录失败")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("{title}")
@pytest.mark.parametrize("title, username, password, expected_errno", LOGIN_FAIL_CASES)
def test_login_fail(title, username, password, expected_errno):
    """登录失败场景：密码错误、用户名不存在"""
    r = requests.post(BASE_URL + "/wx/auth/login",
                      json={"username": username, "password": password})
    data = r.json()
    assert data["errno"] == expected_errno, f"{title} 失败: {data}"


@allure.feature("鉴权")
@allure.story("登录态校验")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("{title}")
@pytest.mark.parametrize("title, headers", AUTH_CASES)
def test_auth_required(title, headers):
    """未登录或 token 无效时，订单接口应被拦截"""
    r = requests.get(BASE_URL + "/wx/order/list", headers=headers)
    data = r.json()
    assert data["errno"] == 501, f"{title} 失败: {data}"
