import re
import requests

ip_list = []
html = requests.get("http://haoip.cc/tiqu.htm")
ip_list_n = re.findall(r'r/>(.*?)<b', html.text, re.S)
for ip in ip_list_n:
    i = re.sub('\n', "", ip)
    ip_list.append(i.strip())
    print i.strip()
