from playwright.sync_api import sync_playwright
import json
import random
import time
import logging

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BingReWards:
    def __init__(self, headless=False, storage_state="login_state.json"):
        self.headless = headless
        self.storage_state = storage_state
        self.browser = None
        self.context = None
        self.page = None

    def _initialize_browser(self):
        self.browser = sync_playwright().start().chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(storage_state=self.storage_state)
        self.page = self.context.new_page()

    def _cleanup(self):
        if self.browser:
            self.browser.close()
            self.browser = None
            self.context = None
            self.page = None

    def search(self, query1,query2,sleep_time=5):
        try:
            self._initialize_browser()
            self.page.goto("https://cn.bing.com/")
            
            # 定位搜索框并输入关键词
            search_box = self.page.wait_for_selector("#sb_form_q")
            search_box.fill(query1)
            
            # 模拟回车键进行搜索
            search_box.press("Enter")
            
            # 等待搜索结果加载
            self.page.wait_for_load_state("networkidle")
            
            # 保持页面一段时间，便于查看效果
            import time
            time.sleep(sleep_time)
            search_box = self.page.wait_for_selector("#sb_form_q")
            search_box.fill(query2)
            
            # 模拟回车键进行搜索
            search_box.press("Enter")
            # 等待搜索结果加载
            self.page.wait_for_load_state("networkidle")

            time.sleep(5)

        finally:
            self._cleanup()

    def task_points(self):
        try:
            self._initialize_browser()
            self.page.goto('https://rewards.bing.com/?ref=rewardspanel', timeout=100000)
            
            # 获取所有可点击的卡片
            cards = self.page.query_selector_all('.mee-icon.mee-icon-AddMedium')
            logging.info(f"找到 {len(cards)} 个可点击卡片")

            # 只处理前三个卡片
            for index, card in enumerate(cards[:3], 1):
                logging.info(f"正在点击第 {index} 个卡片...")
                
                # 点击卡片并等待新页面
                with self.page.expect_popup() as new_page_info:
                    card.click()
                
                # 获取新页面并关闭
                new_page = new_page_info.value
                new_page.close()
                
                # 随机延时5-10秒
                sleep_time = random.uniform(5, 10)
                time.sleep(sleep_time)

            logging.info("前三个卡片点击完成！")

        except Exception as e:
                logging.error(f"收集积分时出错: {str(e)}")
        finally:
            self._cleanup()

    def get_point_progress(self):
        try:
            self._initialize_browser()
            self.page.goto('https://rewards.bing.com/?ref=rewardspanel', timeout=100000)

            # 点击积分详情按钮
            breakdown_button = self.page.wait_for_selector('.pointbreakdownlink.ng-scope.c-call-to-action.c-glyph.f-lightweight')
            breakdown_button.click()
            logging.info("已点击积分详情按钮")

            # 等待积分进度元素加载
            progress_element = self.page.wait_for_selector('p.pointsDetail')
            progress_text = progress_element.inner_text().strip()

            logging.info(f"获取到的积分进度文本: {progress_text}")

            # 判断是否是 x/x 格式
            if '/' in progress_text:
                left, right = progress_text.split('/')
                return left.strip() == right.strip()

            return False

        except Exception as e:
            logging.error(f"获取积分进度时出错: {str(e)}")
            return False
        finally:
            self._cleanup()