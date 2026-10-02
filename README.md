# litemall 商城（用户端）接口自动化测试

基于开源电商项目 [litemall](https://github.com/linlinjava/litemall) 用户端的接口测试项目：从接口盘点、用例设计到自动化落地与缺陷定位的完整实践。

## 技术栈

`Python` `pytest` `requests` `Allure` `Postman` `MySQL` `Docker` `Git`

## 项目结构

```
├── config.py            # 配置层：测试环境地址、测试账号
├── api_client.py        # 接口层：LitemallClient 封装登录与订单接口
├── conftest.py          # 夹具层：登录态 token、测试数据自动获取
├── pytest.ini           # pytest 配置
├── test_login.py        # 登录模块用例
├── test_order_list.py   # 订单列表用例（参数化）
└── test_order_ops.py    # 订单操作用例（状态校验拦截）
```

分层设计：用例层只描述"发什么请求、断言什么"，接口细节收敛在 api_client.py，环境配置收敛在 config.py，更换测试环境只需修改一个文件。

## 用例覆盖情况

| 模块 | 用例数 | 覆盖内容 |
| --- | --- | --- |
| 登录 | 1 | 正确账号密码登录，返回有效 token |
| 订单列表 | 5 | 分页边界值（page / limit 越界回落）、非法参数 |
| 订单操作 | 5 | 订单状态机校验拦截、越权与不存在订单、已知缺陷监控 |
| **合计** | **11** | 其余模块持续补充中 |

## 运行方式

```bash
pip install -r requirements.txt
python -m pytest --alluredir=allure-results --clean-alluredir
allure serve allure-results
```

## 测试报告

![Allure 报告](docs/allure-report.png)

## 缺陷发现

测试过程中累计发现 6 个真实缺陷，其中订单退款接口存在错误提示文案缺陷（退款被拒时提示"订单不能取消"，应为退款相关文案），已通过 `@pytest.mark.xfail` 标记为已知缺陷持续监控——缺陷修复后该用例将自动转为通过状态。

## 被测系统

litemall（Spring Boot + MyBatis + MySQL + Vue），通过 Docker 部署测试环境。
