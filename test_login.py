import allure
import requests
from config import BASE_URL, USERNAME, PASSWORD


@allure.feature("登录模块")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("正确账号密码登录，返回有效 token")
def test_login():
    """登录接口基础校验"""
    url = BASE_URL + "/wx/auth/login"
    r = requests.post(url, json={"username": USERNAME, "password": PASSWORD})
    data = r.json()
    assert data["errno"] == 0, f"登录失败: {data}"
    assert data["data"]["token"], "没有返回 token"
