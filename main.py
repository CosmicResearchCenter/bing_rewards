import asyncio
from src.core.bing_rewards import BingReWards
from src.utils.tophot import TopHot
import random
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_json_files(directory):
    """
    返回指定目录下所有 JSON 文件的完整路径列表
    """
    json_files = []
    try:
        for filename in os.listdir(directory):
            if filename.lower().endswith('.json'):
                json_files.append(os.path.join(directory, filename))
    except Exception as e:
        logging.exception("获取账号文件列表时发生异常：")
    return json_files

async def main():
    try:
        accounts = get_json_files("accounts")
        if not accounts:
            logging.error("没有找到账号文件，请检查 'accounts' 目录。")
            return

        try:
            search_datas = TopHot().get_hot_data()
            if not search_datas:
                logging.error("没有获取到搜索任务数据！")
                return
        except Exception as e:
            logging.exception("获取搜索任务数据时发生异常：")
            return

        while True:
            try:
                # 筛选出未完成积分任务的账号
                unfinished_accounts = []
                for account in accounts:
                    try:
                        bing = BingReWards(headless=False, storage_state=account)
                        if not await bing.get_point_progress():
                            unfinished_accounts.append(account)
                    except Exception as e:
                        logging.exception(f"在检查账号 {account} 的积分任务进度时发生异常：")
                
                if not unfinished_accounts:
                    logging.info("所有账号均已完成积分任务，搜索任务结束。")
                    break

                account = random.choice(unfinished_accounts)
                logging.info(f"选中账号 {account} 进行搜索任务。")
                try:
                    bing = BingReWards(headless=False, storage_state=account)
                    await bing.search(search_datas[0].title, search_datas[0].description)
                except Exception as e:
                    logging.exception(f"账号 {account} 在执行搜索任务时发生异常：")
            except Exception as e:
                logging.exception("搜索任务循环中发生异常：")
            finally:
                await asyncio.sleep(20)

    except Exception as e:
        logging.exception("程序运行时发生异常：")

if __name__ == "__main__":
    asyncio.run(main())