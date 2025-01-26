import argparse
import logging
from bing_rewards import BingReWards, save_login_state

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def validate_args(args):
    """
    校验命令行参数，确保至少选择一个功能。

    :param args: 命令行参数对象。
    :raises ValueError: 如果未选择任何功能。
    """
    if not any([args.login, args.search, args.collect]):
        raise ValueError("请至少选择一个功能：--login、--search 或 --collect")

def run_search_task(bing_rewards):
    """
    执行搜索任务。

    :param bing_rewards: BingReWards 实例。
    """
    logging.info("正在执行搜索任务...")
    try:
        bing_rewards.perform_searches()
        logging.info("搜索任务完成！")
    except Exception as e:
        logging.error(f"搜索任务失败: {e}")

def run_collect_task(bing_rewards):
    """
    执行积分领取任务。

    :param bing_rewards: BingReWards 实例。
    """
    logging.info("正在领取积分...")
    try:
        bing_rewards.collect_rewards()
        logging.info("积分领取完成！")
    except Exception as e:
        logging.error(f"积分领取失败: {e}")

def run_login_task(auth_file):
    """
    执行登录任务并保存登录状态。

    :param auth_file: 认证信息文件路径。
    """
    logging.info(f"正在保存登录状态到 {auth_file}...")
    try:
        save_login_state(auth_file)
        logging.info(f"登录状态已保存到 {auth_file}")
    except Exception as e:
        logging.error(f"保存登录状态失败: {e}")

def main():
    """
    主函数，根据命令行参数调用 BingReWards 类的功能。
    """
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="Bing Rewards 自动化工具")
    parser.add_argument('--login', action='store_true', help="保存登录状态")
    parser.add_argument('--search', action='store_true', help="执行搜索任务")
    parser.add_argument('--collect', action='store_true', help="领取积分")
    parser.add_argument('--auth_file', default='auth.json', help="认证信息文件路径")
    parser.add_argument('--search_data_file', default='search_data.json', help="搜索数据文件路径")
    parser.add_argument('--delay', type=int, default=5, help="操作之间的延时（秒）")
    parser.add_argument('--headless', action='store_true', help="是否启用无头模式")
    args = parser.parse_args()

    try:
        # 校验参数
        validate_args(args)

        if args.login:
            # 登录任务强制禁用无头模式
            run_login_task(args.auth_file)
        else:
            # 初始化 BingReWards 实例
            bing_rewards = BingReWards(
                auth_file=args.auth_file,
                search_data_file=args.search_data_file,
                delay=args.delay,
                headless=args.headless  # 传递无头模式参数
            )

            if args.search:
                # 执行搜索任务
                run_search_task(bing_rewards)

            if args.collect:
                # 执行积分领取任务
                run_collect_task(bing_rewards)

    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"程序运行失败: {e}")

if __name__ == "__main__":
    main()