import json
import os

import urllib3


def handler(event, context):
    print(json.dumps(event))

    url = os.environ["PROXY_URL"]
    proxy_username = os.environ["PROXY_USERNAME"]
    proxy_password = os.environ["PROXY_PASSWORD"]

    # Two way to have http method following if lambda proxy is enabled or not
    if event.get("httpMethod"):
        http_method = event["httpMethod"]
    else:
        http_method = event["requestContext"]["http"]["method"]

    headers = ""
    if event.get("headers"):
        headers = event["headers"]

    # Important to remove the Host header before forwarding the request
    if headers.get("Host"):
        headers.pop("Host")

    if headers.get("host"):
        headers.pop("host")

    body = ""
    if event.get("body"):
        body = event["body"]

    auth_headers = urllib3.make_headers(basic_auth=f"{proxy_username}:{proxy_password}")

    try:
        http = urllib3.PoolManager()
        resp = http.request(
            method=http_method, url=url, headers={**headers, **auth_headers}, body=body
        )

        body = {"result": resp.data.decode}  # ('utf-8')

        response = {"statusCode": resp.status, "body": json.dumps(body)}
    except urllib3.exceptions.NewConnectionError:
        print("Connection failed.")
        response = {"statusCode": 500, "body": "Connection failed."}

    return response
