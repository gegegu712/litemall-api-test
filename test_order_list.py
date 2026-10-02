import allure
import pytest

# 每一行 = Excel 里一条用例：(标题, 请求参数, 预期errno)
CASES = [
    ("page=0 越界回落第一页", {"page": 0}, 0),
    ("page=999 越界回落最后一页", {"page": 999}, 0),
    ("limit=1 每页只返回一条", {"limit": 1}, 0),
    ("limit=10000 无上限钳制", {"limit": 10000}, 0),
    ("showType=abc 返回参数值不对", {"showType": "abc"}, 402),
]


@allure.feature("订单模块")
@allure.story("订单列表")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("{title}")
@pytest.mark.parametrize("title, params, expected_errno", CASES)
def test_order_list(api, title, params, expected_errno):
    """订单列表分页与异常参数校验"""
    data = api.order_list(**params)
    assert data["errno"] == expected_errno, f"{title} 失败: {data}"
