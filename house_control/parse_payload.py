
def parse_payload(payload):
    params = {}
    key_value_list = payload.split("&")
    for item in key_value_list:
        (key, value) = item.split("=")
        params[key] = value
    return params
