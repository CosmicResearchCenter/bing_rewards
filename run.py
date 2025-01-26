import argparse
from bing_rewards import BingReWards, save_login_state  # 假设 BingReWards 类在 bing_rewards.py 文件中

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
    args = parser.parse_args()

    # 根据参数执行相应功能
    if args.login:
        # 保存登录状态
        print(f"正在保存登录状态到 {args.auth_file}...")
        save_login_state(args.auth_file)
        print(f"登录状态已保存到 {args.auth_file}")
    else:
        # 初始化 BingReWards 实例
        bing_rewards = BingReWards(
            auth_file=args.auth_file,
            search_data_file=args.search_data_file,
            delay=args.delay
        )

        if args.search:
            # 执行搜索任务
            print("正在执行搜索任务...")
            bing_rewards.perform_searches()
            print("搜索任务完成！")

        if args.collect:
            # 领取积分
            print("正在领取积分...")
            bing_rewards.collect_rewards()
            print("积分领取完成！")

if __name__ == "__main__":
    main()