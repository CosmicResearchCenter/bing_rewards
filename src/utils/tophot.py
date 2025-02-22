import requests
from src.types.types import HotData
from typing import List, Dict, Any, Union

class TopHot:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
        })
        
        # 初始化cookies
        self._init_cookies()
        # 初始化headers
        self.headers = {
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
        
    def _init_cookies(self) -> None:
        cookies = [
            {'name': 'Hm_lvt_3b1e939f6e789219d8629de8a519eab9', 'value': '1739963684', 'domain': '.tophub.today', 'path': '/'},
            {'name': 'Hm_lpvt_3b1e939f6e789219d8629de8a519eab9', 'value': '1739963684', 'domain': '.tophub.today', 'path': '/'},
            {'name': 'HMACCOUNT', 'value': '2D2279D7246377BB', 'domain': '.tophub.today', 'path': '/'}
        ]
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

    def get_hot_data(self) -> List[HotData]:
        try:
            url = "https://tophub.today/do"
            data = "c=hot&t=daily"
            response = self.session.post(url, headers=self.headers, data=data, verify=False)
            
            if response.status_code != 200:
                raise Exception(f"请求失败，状态码：{response.status_code}")
            
            json_data = response.json()
            if 'data' not in json_data:
                raise Exception("响应数据格式错误")
                
            search_datas: List[HotData] = []
            for item in json_data['data']:
                search_datas.append(HotData(title=item['title'], description=item['description']))
                
            return search_datas
            
        except Exception as e:
            print(f"获取热点数据失败：{str(e)}")
            return []

# 使用示例:
if __name__ == "__main__":
    top_hot = TopHot()
    hot_data = top_hot.get_hot_data()
    print(hot_data)