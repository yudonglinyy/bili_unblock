# -*- coding: utf8 -*-
import json
import requests


def main_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # print("Received context: " + str(context))

    data = event.get("queryString", {})
    headers = event.get("headers", {})
    referer = headers.get("referer", "")
    del headers["host"]

    upstream_pc_url = 'https://api.bilibili.com/pgc/player/web/playurl'
    upstream_app_url = 'https://api.bilibili.com/pgc/player/api/playurl'
    timeout = 5

    if data and "platform" in data and "android" in data["platform"]:
        url = upstream_app_url
    else:
        url = upstream_pc_url

    try:
        resp = requests.get(url, data, headers=headers, timeout=timeout)
    except Exception as e:
        print(e)
        return {
            "isBase64Encoded": False,
            "statusCode": resp.status_code,
            "headers": {"Content-Type": "text/html"},
            "body": "error:%s" % e
        }

    try:
        respjson = resp.json()
    except Exception as e:
        print(e)
        return {
            "isBase64Encoded": False,
            "statusCode": resp.status_code,
            "headers": {"Content-Type": "text/html"},
            "body": "error:%s, resp:%s" % (e, resp.text)
        }

    respheaders = resp.headers
    del respheaders["Content-Encoding"]
    respheaders["access-control-allow-credentials"] = "true"
    respheaders["Access-Control-Allow-Origin"] = "/".join(referer.split("/", 3)[:-1])
    respheaders["access-control-allow-headers"] = "Origin,No-Cache,X-Requested-With,If-Modified-Since,Pragma,Last-Modified,Cache-Control,Expires,Content-Type,Access-Control-Allow-Credentials,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Cache-Webcdn"

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": dict(respheaders),
        "body": resp.text,
    }

