import allure
import pytest


@allure.feature("订单模块")
@allure.story("取消订单")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("已取消订单再次取消，被状态校验拦截")
def test_cancel_cancelled(api, cancelled_order_id):
    """已取消订单再取消，应被拦截"""
    with allure.step("调用取消订单接口"):
        data = api.order_cancel(cancelled_order_id)
    with allure.step("断言返回 725 状态校验拦截"):
        assert data["errno"] == 725, f"预期被拦截: {data}"


@allure.feature("订单模块")
@allure.story("取消订单")
@allure.severity(allure.severity_level.MINOR)
@allure.title("取消不存在的订单，返回参数值不对")
def test_cancel_not_exist(api):
    """取消不存在的订单，应返回 402"""
    data = api.order_cancel(999)
    assert data["errno"] == 402, f"预期402: {data}"


@allure.feature("订单模块")
@allure.story("确认收货")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("已取消订单直调确认收货，被状态校验拦截")
def test_confirm_cancelled(api, cancelled_order_id):
    """已取消订单直调确认收货，应被拦截"""
    data = api.order_confirm(cancelled_order_id)
    assert data["errno"] == 725, f"预期被拦截: {data}"


@allure.feature("订单模块")
@allure.story("支付")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("已取消订单调用支付接口，被状态校验拦截")
def test_prepay_cancelled(api, cancelled_order_id):
    """已取消订单调支付，应被拦截"""
    data = api.order_prepay(cancelled_order_id)
    assert data["errno"] == 725, f"预期被拦截: {data}"


@allure.feature("订单模块")
@allure.story("退款")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("退款接口错误提示文案缺陷（BUG-006）")
@pytest.mark.xfail(reason="BUG-006: 退款接口错误提示文案为'订单不能取消'")
def test_refund_wrong_message(api, cancelled_order_id):
    """BUG-006 复现：退款接口的提示文案不应出现'取消'"""
    data = api.order_refund(cancelled_order_id)
    assert data["errno"] == 725
    assert "取消" not in data["errmsg"], f"文案缺陷复现: {data}"
