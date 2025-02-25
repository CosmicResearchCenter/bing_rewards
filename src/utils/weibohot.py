import requests
from src.types.types import HotData
from typing import List

class WeiboHot:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
            "client-version": "v2.47.36",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "server-version": "v2025.02.25.3",
            "x-requested-with": "XMLHttpRequest",
            "x-xsrf-token": "-ZDFOmBlStvg3uHl6FWssaB2",
            "Referer": "https://weibo.com/hot/search"
        }

    def get_hot_data(self) -> List[HotData]:
        try:
            url = "https://weibo.com/ajax/side/hotSearch"
            response = self.session.get(url, headers=self.headers, verify=False)
            
            if response.status_code != 200:
                raise Exception(f"请求失败，状态码：{response.status_code}")
            
            json_data = response.json()
            if 'data' not in json_data or 'realtime' not in json_data['data']:
                raise Exception("响应数据格式错误")
                
            search_datas: List[HotData] = []
            for item in json_data['data']['realtime']:
                search_datas.append(HotData(
                    title=item.get('word', ''),
                    description=item.get('note', '')
                ))
                
            return search_datas
            
        except Exception as e:
            print(f"获取微博热搜数据失败：{str(e)}")
            return []

# 使用示例:
if __name__ == "__main__":
    weibo_hot = WeiboHot()
    hot_data = weibo_hot.get_hot_data()
    print(hot_data)
