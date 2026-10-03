import allure


@allure.feature("订单模块")
@allure.story("订单详情")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("查询已取消订单详情成功")
def test_order_detail(api, cancelled_order_id):
    """复用 cancelled_order_id 夹具，不硬编码订单 id"""
    data = api.order_detail(cancelled_order_id)
    assert data["errno"] == 0, f"订单详情查询失败: {data}"


@allure.feature("订单模块")
@allure.story("订单详情")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("订单ID不存在时返回订单不存在")
def test_order_detail_not_exist(api):
    data = api.order_detail(999)
    assert data["errno"] == 720, f"预期返回 720 订单不存在，实际: {data}"
