import pytest
from api_client import LitemallClient
from config import USERNAME, PASSWORD


@pytest.fixture(scope="session")
def api():
    client = LitemallClient(USERNAME, PASSWORD)
    client.login()
    return client


@pytest.fixture(scope="session")
def token(api):
    return api.token


@pytest.fixture(scope="session")
def cancelled_order_id(api):
    """自动找一条已取消订单作为测试数据，找不到则跳过用例"""
    data = api.order_list(limit=100)
    for order in data["data"]["list"]:
        if "已取消" in order["orderStatusText"]:
            return order["id"]
    pytest.skip("测试数据不足：当前账号没有已取消订单")
