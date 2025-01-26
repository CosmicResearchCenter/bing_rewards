import json
import random
import time
import logging
import argparse
from playwright.sync_api import sync_playwright, Page
from playwright_stealth import stealth_sync

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 选择器配置
SELECTORS = {
    'points_selector': '#rh_rwm .b_clickarea',
    'search_input': '#sb_form_q',
    'search_results': '#b_results',
    'rewards_card': '#daily-sets .c-card-content'
}

class BingReWards:
    def __init__(self, auth_file='auth.json', search_data_file='search_data.json', delay=5):
        """
        初始化 BingReWards 类。

        :param auth_file: 存储认证信息的 JSON 文件路径。
        :param search_data_file: 存储搜索数据的 JSON 文件路径。
        :param delay: 操作之间的延时（秒），默认为 5 秒。
        """
        self.auth_info = self.load_json_file(auth_file)
        self.search_data = self.load_json_file(search_data_file) if search_data_file else None
        self.delay = delay  # 操作之间的延时
        self.browser = None
        self.context = None

    @staticmethod
    def load_json_file(file_path):
        """
        加载 JSON 文件。

        :param file_path: JSON 文件路径。
        :return: 解析后的 JSON 数据。
        """
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"加载 JSON 文件失败: {e}")
            return None

    def get_random_search_content(self):
        """
        随机获取搜索内容。

        :return: 随机的搜索词或句子。
        """
        if random.choice([True, False]):
            return random.choice(self.search_data['search_terms'])
        else:
            return random.choice(self.search_data['search_sentences'])

    def scroll_page(self, page):
        """
        模拟页面滚动。

        :param page: Playwright 页面对象。
        """
        scroll_distance = random.randint(500, 1500)
        for _ in range(0, scroll_distance, random.randint(30, 100)):
            page.mouse.wheel(0, random.randint(30, 100))
            time.sleep(random.uniform(0.1, 0.5))
        logging.info(f"页面向下滑动 {scroll_distance} 像素")

    def get_points_search(self, page: Page):
        """
        获取当前积分。

        :param page: Playwright 页面对象。
        :return: 当前积分值。
        """
        try:
            page.wait_for_selector(SELECTORS['points_selector'], timeout=5000)
            points_element = page.query_selector(SELECTORS['points_selector'])
            if points_element:
                points_text = points_element.inner_text().strip()
                return int(points_text)
        except Exception as e:
            logging.error(f"获取积分失败: {e}")
        return 0

    def perform_search(self, page, search_content):
        """
        执行单次搜索。

        :param page: Playwright 页面对象。
        :param search_content: 搜索内容。
        :return: 是否成功执行搜索。
        """
        try:
            page.wait_for_selector(SELECTORS['search_input'])
            page.fill(SELECTORS['search_input'], search_content)
            page.press(SELECTORS['search_input'], 'Enter')
            page.wait_for_selector(SELECTORS['search_results'])
            return True
        except Exception as e:
            logging.error(f"搜索失败: {e}")
            return False

    def perform_searches(self):
        """
        执行 Bing 搜索任务。
        """
        if not self.search_data:
            logging.error("未提供搜索数据文件，无法执行搜索。")
            return

        with sync_playwright() as p:
            self.start_browser(p)
            page = self.context.new_page()
            page.goto('https://cn.bing.com')

            initial_points = self.get_points_search(page)
            logging.info(f"初始积分: {initial_points}")

            for i in range(40):
                search_content = self.get_random_search_content()
                logging.info(f"第 {i + 1} 次搜索内容: {search_content}")
                if self.perform_search(page, search_content):
                    current_points = self.get_points_search(page)
                    if current_points > initial_points:
                        logging.info(f"积分获取成功: +{current_points - initial_points}")
                    else:
                        logging.info("本次未获取积分")
                    initial_points = current_points
                    self.scroll_page(page)
                    time.sleep(random.uniform(self.delay - 2, self.delay + 2))  # 随机延时
            self.close_browser()

    def collect_rewards(self):
        """
        收集 Bing Rewards 积分。
        """
        with sync_playwright() as p:
            self.start_browser(p)
            page = self.context.new_page()
            page.goto('https://rewards.bing.com/?ref=rewardspanel')
            page.wait_for_selector(SELECTORS['rewards_card'])

            card_contents = page.query_selector_all(SELECTORS['rewards_card'])
            for index, card in enumerate(card_contents, start=1):
                card.click()
                time.sleep(random.uniform(self.delay - 2, self.delay + 2))  # 随机延时

            page.reload()
            self.close_browser()

    def start_browser(self, playwright):
        """
        启动浏览器并初始化上下文。
        """
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        stealth_sync(self.context)  # 反检测
        self.context.add_cookies(self.auth_info['cookies'])

    def close_browser(self):
        """
        关闭浏览器。
        """
        if self.browser:
            self.browser.close()

def save_login_state(auth_file='auth.json'):
    """
    保存登录状态到文件。

    :param auth_file: 保存登录状态的文件路径。
    """
    with sync_playwright() as p:
        # 启动浏览器（非无头模式，方便手动登录）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 导航到登录页面
        page.goto('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=170&id=264960&wreply=https%3a%2f%2fcn.bing.com%2fsecure%2fPassport.aspx%3fedge_suppress_profile_switch%3d1%26requrl%3dhttps%253a%252f%252fcn.bing.com%252f%253fwlexpsignin%253d1%26sig%3d22A6C719A8D160EE312ED266A9D0614F%26nopa%3d2&wp=MBI_SSL&lc=2052&CSRFToken=b5b2c4e5-e1ee-4d0f-8d22-2fc2475b0177&cobrandid=c333cba8-c15c-4458-b082-7c8ce81bee85&aadredir=1&nopa=2')

        # 提示用户手动登录
        print("请在浏览器中手动登录，完成后按回车继续...")
        input()  # 等待用户按回车

        # 保存登录状态到文件
        context.storage_state(path=auth_file)
        print(f"登录状态已保存到 {auth_file}")

        # 关闭浏览器
        browser.close()

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_file', default='auth.json', help='认证信息文件路径')
    parser.add_argument('--search_data_file', default='search_data.json', help='搜索数据文件路径')
    parser.add_argument('--delay', type=int, default=5, help='操作之间的延时（秒）')
    args = parser.parse_args()

    # 创建 BingReWards 实例
    bing_integration = BingReWards(auth_file=args.auth_file, search_data_file=args.search_data_file, delay=args.delay)

    # 执行搜索任务
    bing_integration.perform_searches()

    # 收集积分任务
    bing_integration.collect_rewards()