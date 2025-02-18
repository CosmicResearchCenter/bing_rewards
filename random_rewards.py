import os
import random
import time
import logging
import json
from datetime import datetime
from bing_rewards import BingReWards

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'bing_rewards_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

class RandomRewardsRunner:
    def __init__(self, accounts_dir="accounts", search_data_file="search_data.json"):
        """
        初始化随机奖励运行器
        
        :param accounts_dir: 存放账号认证文件的目录
        :param search_data_file: 搜索数据文件路径
        """
        self.accounts_dir = accounts_dir
        self.search_data_file = search_data_file
        self.available_accounts = self._load_available_accounts()

    def _load_available_accounts(self):
        """加载所有可用的账号文件"""
        if not os.path.exists(self.accounts_dir):
            raise FileNotFoundError(f"账号目录 {self.accounts_dir} 不存在")
        
        accounts = []
        for file in os.listdir(self.accounts_dir):
            if file.endswith('.json'):
                accounts.append(os.path.join(self.accounts_dir, file))
        
        if not accounts:
            raise FileNotFoundError("没有找到可用的账号文件")
        
        return accounts

    def _get_random_delay(self, min_minutes=30, max_minutes=120):
        """生成随机延迟时间（分钟）"""
        return random.uniform(min_minutes, max_minutes)

    def _get_operation_delay(self, min_seconds=2, max_seconds=8):
        """生成操作间随机延迟时间（秒）"""
        return random.uniform(min_seconds, max_seconds)

    def _get_random_account(self):
        """随机选择一个账号文件"""
        return random.choice(self.available_accounts)

    def _load_account_info(self, auth_file):
        """加载账号信息"""
        try:
            with open(auth_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('account_name', os.path.basename(auth_file))
        except:
            return os.path.basename(auth_file)

    def run_single_account(self):
        """运行单个随机账号的任务"""
        auth_file = self._get_random_account()
        account_name = self._load_account_info(auth_file)
        
        logging.info(f"选择账号: {account_name}")
        
        try:
            # 创建 BingReWards 实例，使用随机延迟时间
            delay = random.uniform(3, 7)  # 基础延迟3-7秒
            bing_rewards = BingReWards(
                auth_file=auth_file,
                search_data_file=self.search_data_file,
                delay=delay,
                headless=True
            )

            # 随机决定是否先执行搜索
            if random.choice([True, False]):
                logging.info("先执行搜索任务...")
                bing_rewards.perform_searches()
                time.sleep(self._get_operation_delay(5, 15))
                logging.info("执行积分收集任务...")
                bing_rewards.collect_rewards()
            else:
                logging.info("先执行积分收集任务...")
                bing_rewards.collect_rewards()
                time.sleep(self._get_operation_delay(5, 15))
                logging.info("执行搜索任务...")
                bing_rewards.perform_searches()

        except Exception as e:
            logging.error(f"账号 {account_name} 执行任务失败: {str(e)}")

    def run_continuous(self):
        """持续运行，随机选择账号执行任务"""
        while True:
            try:
                self.run_single_account()
                
                # 生成下次运行的随机延迟时间
                delay_minutes = self._get_random_delay()
                next_run_time = datetime.now().timestamp() + (delay_minutes * 60)
                logging.info(f"下次运行将在 {delay_minutes:.2f} 分钟后 "
                           f"({datetime.fromtimestamp(next_run_time).strftime('%Y-%m-%d %H:%M:%S')})")
                
                time.sleep(delay_minutes * 60)
                
            except KeyboardInterrupt:
                logging.info("程序被用户中断")
                break
            except Exception as e:
                logging.error(f"发生错误: {str(e)}")
                time.sleep(300)  # 发生错误时等待5分钟后继续

if __name__ == "__main__":
    try:
        runner = RandomRewardsRunner()
        runner.run_continuous()
    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")
