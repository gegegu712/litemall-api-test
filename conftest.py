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
@pytest.fixture(scope="session")
def goods_id(api):
    """取一个真实存在的商品 id 作为测试数据"""
    data = api.goods_list(limit=1)
    return data["data"]["list"][0]["id"]
