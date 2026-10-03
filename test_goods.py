import allure
import pytest

# 商品列表参数化用例：(标题, 请求参数, 预期errno)
LIST_CASES = [
    ("默认参数返回商品列表", {}, 0),
    ("page=9999 越界回落最后一页", {"page": 9999}, 0),
    ("sort=abc 非法排序字段返回参数值不对", {"sort": "abc"}, 402),
]


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("{title}")
@pytest.mark.parametrize("title, params, expected_errno", LIST_CASES)
def test_goods_list(api, title, params, expected_errno):
    """商品列表分页与参数校验"""
    data = api.goods_list(**params)
    assert data["errno"] == expected_errno, f"{title} 失败: {data}"


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("limit=1 时只返回一条商品")
def test_goods_list_limit_one(api):
    data = api.goods_list(limit=1)
    assert data["errno"] == 0, f"请求失败: {data}"
    assert len(data["data"]["list"]) == 1, f"应只返回1条，实际返回: {data}"


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.MINOR)
@allure.title("关键字无匹配时返回空列表")
def test_goods_list_keyword_no_match(api):
    data = api.goods_list(keyword="zzzz不存在")
    assert data["errno"] == 0, f"请求失败: {data}"
    assert len(data["data"]["list"]) == 0, f"应返回空列表，实际返回: {data}"


@allure.feature("商品模块")
@allure.story("商品详情")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("商品详情查询成功，返回商品信息")
def test_goods_detail(api, goods_id):
    data = api.goods_detail(goods_id)
    assert data["errno"] == 0, f"商品详情查询失败: {data}"


@allure.feature("商品模块")
@allure.story("商品详情")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("商品ID不存在时不应返回系统内部错误")
@pytest.mark.xfail(reason="BUG-007: 商品不存在时返回502系统内部错误，应返回业务错误码")
def test_goods_detail_not_exist(api):
    data = api.goods_detail(99999999)
    assert data["errno"] != 502, f"商品不存在时返回了系统内部错误: {data}"
