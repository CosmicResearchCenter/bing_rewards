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

if __name__ == "__main__":
    try:
        accounts = get_json_files("accounts")
        if not accounts:
            logging.error("没有找到账号文件，请检查 'accounts' 目录。")
            exit(1)
    except Exception as e:
        logging.exception("初始化账号时发生异常：")
        exit(1)
    
    # # 领取积分任务
    # for account in accounts:
    #     try:
    #         bing = BingReWards(headless=False, storage_state=account)
    #         bing.task_points()
    #         logging.info(f"已对账号 {account} 领取积分任务。")
    #     except Exception as e:
    #         logging.exception(f"账号 {account} 在领取积分任务时发生异常：")
    #     finally:
    #         time.sleep(20)

    # 获取搜索任务数据
    try:
        search_datas = TopHot().get_hot_data()
        if not search_datas:
            logging.error("没有获取到搜索任务数据！")
            exit(1)
    except Exception as e:
        logging.exception("获取搜索任务数据时发生异常：")
        exit(1)

    # 循环执行搜索任务
    while True:
        try:
            # 筛选出未完成积分任务的账号
            unfinished_accounts = []
            for account in accounts:
                try:
                    bing = BingReWards(headless=False, storage_state=account)
                    if not bing.get_point_progress():
                        unfinished_accounts.append(account)
                except Exception as e:
                    logging.exception(f"在检查账号 {account} 的积分任务进度时发生异常：")
            if not unfinished_accounts:
                logging.info("所有账号均已完成积分任务，搜索任务结束。")
                break

            # 从未完成的账号中随机选择一个
            account = random.choice(unfinished_accounts)
            logging.info(f"选中账号 {account} 进行搜索任务。")
            try:
                bing = BingReWards(headless=False, storage_state=account)
                bing.search(search_datas[0].title, search_datas[0].description)
            except Exception as e:
                logging.exception(f"账号 {account} 在执行搜索任务时发生异常：")
        except Exception as e:
            logging.exception("搜索任务循环中发生异常：")
        finally:
            time.sleep(20)
