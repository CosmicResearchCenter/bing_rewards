import requests
from src.types.types import HotData
from typing import List, Dict, Any, Union
# 创建会话并设置User-Agent
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
})

# 添加Cookies
cookies = [
    {'name': 'Hm_lvt_3b1e939f6e789219d8629de8a519eab9', 'value': '1739963684', 'domain': '.tophub.today', 'path': '/'},
    {'name': 'Hm_lpvt_3b1e939f6e789219d8629de8a519eab9', 'value': '1739963684', 'domain': '.tophub.today', 'path': '/'},
    {'name': 'HMACCOUNT', 'value': '2D2279D7246377BB', 'domain': '.tophub.today', 'path': '/'}
]
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

# 设置请求头
headers = {
    "Host": "tophub.today",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
    "origin": "https://tophub.today",
    "priority": "u=1, i",
    "referer": "https://tophub.today/",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

# 发送POST请求
url = "https://tophub.today/do"
data = "c=hot&t=daily"
response = session.post(url, headers=headers, data=data,verify=False)

# 输出响应
print(f"Status Code: {response.status_code}")
print("Response Text:")
# print(response.json()['data'])

data = response.json()['data']

search_datas:List[HotData] = []

for item in data:
    search_datas.append(HotData(title=item['title'], description=item['description']))
    
print(search_datas) 