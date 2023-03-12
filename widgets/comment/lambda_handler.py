import json

def lambda_handler(event, context):
    # 解析HTTP请求
    method = event['requestContext']['http']
    queryString = event['queryStringParameters']
    body = json.loads(event['body'])

    # 处理请求
    if method == "GET":
        result = foo(**queryString)
    elif method == "POST":
        data = json.loads(body)
        result = bar(data)
    else:
        raise ValueError(f"Invalid HTTP method: {method}")

    # 序列化结果
    return json.dumps(result)


def foo(**params: dict) -> dict:
    # 处理GET请求中的参数
    pass


def bar(data: dict) -> dict:
    # 处理POST请求中的数据
    pass
