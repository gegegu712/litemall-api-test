# -*- coding: utf-8 -*-
"""CI 用的 mock 服务。

GitHub Actions 的云端环境里没有 litemall 真实后端，用这个脚本模拟用户端接口，
让自动化用例在没有真实后端的环境下也能完整跑通（验证用例链路与框架可用性）。
响应内容与真实后端保持一致，包括退款接口的文案缺陷（BUG-006），供 xfail 用例持续监控。
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# 一条"已取消"订单，供 cancelled_order_id 夹具与各用例使用
CANCELLED_ORDER = {
    "id": 1,
    "orderStatusText": "已取消(系统)",
    "handleOption": {
        "cancel": False, "delete": True, "pay": False, "comment": False,
        "confirm": False, "refund": False, "rebuy": False, "aftersale": False,
    },
}

# 不存在的订单 id（真实后端返回 402 参数值不对）
NOT_EXIST_ORDER_ID = 999


class MockHandler(BaseHTTPRequestHandler):
    def _reply(self, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json;charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/wx/order/list":
            # 与真实后端一致：showType 传非数字时报 402
            show_type = query.get("showType", [None])[0]
            if show_type is not None and not show_type.isdigit():
                return self._reply({"errno": 402, "errmsg": "参数值不对"})
            return self._reply({
                "errno": 0, "errmsg": "成功",
                "data": {"total": 1, "pages": 1, "limit": 100, "page": 1,
                         "list": [CANCELLED_ORDER]},
            })

        self._reply({"errno": 404, "errmsg": "mock 未实现的接口: " + parsed.path})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            body = json.loads(raw)
        except ValueError:
            body = {}

        path = urlparse(self.path).path
        order_id = body.get("orderId")

        if path == "/wx/auth/login":
            return self._reply({
                "errno": 0, "errmsg": "成功",
                "data": {"token": "mock-token-for-ci", "userInfo": {"nickName": "mock"}},
            })

        if path == "/wx/order/cancel":
            if order_id == NOT_EXIST_ORDER_ID:
                return self._reply({"errno": 402, "errmsg": "参数值不对"})
            return self._reply({"errno": 725, "errmsg": "订单不能取消"})

        if path == "/wx/order/confirm":
            return self._reply({"errno": 725, "errmsg": "订单不能确认收货"})

        if path == "/wx/order/prepay":
            return self._reply({"errno": 725, "errmsg": "订单不能支付"})

        if path == "/wx/order/refund":
            # 保留真实后端的文案缺陷（BUG-006），xfail 用例据此监控
            return self._reply({"errno": 725, "errmsg": "订单不能取消"})

        self._reply({"errno": 404, "errmsg": "mock 未实现的接口: " + path})

    def log_message(self, fmt, *args):
        print("[mock] " + fmt % args)


if __name__ == "__main__":
    port = int(os.environ.get("MOCK_PORT", "8080"))
    print("mock 服务启动: http://localhost:%d" % port)
    HTTPServer(("127.0.0.1", port), MockHandler).serve_forever()
