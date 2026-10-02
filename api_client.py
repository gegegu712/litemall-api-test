import requests
from config import BASE_URL


class LitemallClient:
    """litemall 接口客户端：一个实例 = 一个登录用户"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def login(self):
        url = BASE_URL + "/wx/auth/login"
        r = requests.post(url, json={"username": self.username, "password": self.password})
        self.token = r.json()["data"]["token"]
        return self.token

    def _headers(self):
        return {"X-Litemall-Token": self.token}

    # ===== 订单接口 =====
    def order_list(self, **params):
        url = BASE_URL + "/wx/order/list"
        return requests.get(url, headers=self._headers(), params=params).json()

    def order_cancel(self, order_id):
        url = BASE_URL + "/wx/order/cancel"
        return requests.post(url, headers=self._headers(), json={"orderId": order_id}).json()

    def order_confirm(self, order_id):
        url = BASE_URL + "/wx/order/confirm"
        return requests.post(url, headers=self._headers(), json={"orderId": order_id}).json()

    def order_prepay(self, order_id):
        url = BASE_URL + "/wx/order/prepay"
        return requests.post(url, headers=self._headers(), json={"orderId": order_id}).json()

    def order_refund(self, order_id):
        url = BASE_URL + "/wx/order/refund"
        return requests.post(url, headers=self._headers(), json={"orderId": order_id}).json()
