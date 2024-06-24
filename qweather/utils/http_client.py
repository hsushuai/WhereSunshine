# -*- coding:utf-8 -*-
import json

import requests
from requests.exceptions import HTTPError

headers = {"Accept-Encoding": "gzip"}


def get(api_url, **params):
    resp = requests.get(_build_url(api_url, **params), headers=headers)
    resp_dict = json.loads(resp.text)
    status_code = int(resp_dict["code"])
    if requests.codes.ok != status_code:
        http_error_msg = ""
        if status_code == 204:
            http_error_msg = "204 Client Error: 请求成功，但你查询的地区暂时没有你需要的数据。"
        elif status_code == 400:
            http_error_msg = "400 Client Error: 请求错误，可能包含错误的请求参数或缺少必选的请求参数。"
        elif status_code == 401:
            http_error_msg = "401 Client Error: 认证失败，可能使用了错误的KEY、数字签名错误、KEY的类型错误（如使用SDK的KEY去访问Web API）。"
        elif status_code == 402:
            http_error_msg = "402 Client Error: 超过访问次数或余额不足以支持继续访问服务，你可以充值、升级访问量或等待访问量重置。）。"
        elif status_code == 403:
            http_error_msg = "403 Client Error: 无访问权限，可能是绑定的PackageName、BundleID、域名IP地址不一致，或者是需要额外付费的数据。"
        elif status_code == 404:
            http_error_msg = "404 Client Error: 查询的数据或地区不存在。"
        elif status_code == 429:
            http_error_msg = "429 Client Error: 超过限定的QPM（每分钟访问次数），请参考QPM说明：https://dev.qweather.com/docs/resource/glossary/#qpm"
        elif status_code == 500:
            http_error_msg = "500 Sever Error: 无响应或超时，接口服务异常请联系我们：https://www.qweather.com/contact"
        raise HTTPError(http_error_msg, response=resp)
    return resp_dict


def _build_url(api_url, **params):
    query_params = "?"
    for key, value in params.items():
        if value is None:
            continue
        query_params += f"&{key}={value}"
    return api_url + query_params
