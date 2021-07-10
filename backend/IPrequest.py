# d4a97e278b194fef9c1638c4035db5e2
import requests
import json
import re


def get_ip_data(ip):
    res = requests.get(
        f"http://ip-api.com/json/{ip}")
   
    jsn = json.loads(res.text)
    return jsn


def get_ips_data_array(ips):
    data_array = []
    for ip in ips:
        if ip == "":
            continue
        data_array.append(get_ip_data(ip))

    return data_array

