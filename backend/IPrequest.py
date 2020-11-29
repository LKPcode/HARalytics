# d4a97e278b194fef9c1638c4035db5e2
import requests
import json


def get_ip_data(ip):
    res = requests.get(
        f"https://api.ipgeolocation.io/ipgeo?apiKey=d4a97e278b194fef9c1638c4035db5e2&ip={ip}&fields=latitude,longitude,country_name,city,isp,country_flag")
    jsn = json.loads(res.text)
    print(jsn)
    return jsn


def get_ips_data_array(ips):

    data_array = []
    for ip in ips:
        data_array.append(get_ip_data(ip))

    return data_array


print(get_ips_data_array(["1.1.1.1", "8.8.8.8"]))
