from playwright.async_api import async_playwright
import json
import random
import time
import logging
import asyncio

class BingReWards:
    def __init__(self, headless=False, storage_state="login_state.json"):
        self.headless = headless
        self.storage_state = storage_state
        self.browser = None
        self.context = None
        self.page = None

    async def _initialize_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(storage_state=self.storage_state)
        self.page = await self.context.new_page()

    async def _cleanup(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None
            self.page = None

    async def search(self, query1, query2, sleep_time=5):
        try:
            await self._initialize_browser()
            await self.page.goto("https://cn.bing.com/")
            
            search_box = await self.page.wait_for_selector("#sb_form_q")
            await search_box.fill(query1)
            await search_box.press("Enter")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(sleep_time)
            
            search_box = await self.page.wait_for_selector("#sb_form_q")
            await search_box.fill(query2)
            await search_box.press("Enter")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(5)

        finally:
            await self._cleanup()

    async def task_points(self):
        try:
            await self._initialize_browser()
            await self.page.goto('https://rewards.bing.com/?ref=rewardspanel', timeout=100000)
            
            cards = await self.page.query_selector_all('.mee-icon.mee-icon-AddMedium')
            logging.info(f"找到 {len(cards)} 个可点击卡片")

            for index, card in enumerate(cards[:3], 1):
                logging.info(f"正在点击第 {index} 个卡片...")
                async with self.page.expect_popup() as new_page_info:
                    await card.click()
                
                new_page = await new_page_info.value
                await new_page.close()
                await asyncio.sleep(random.uniform(5, 10))

            logging.info("前三个卡片点击完成！")

        except Exception as e:
            logging.error(f"收集积分时出错: {str(e)}")
        finally:
            await self._cleanup()

    async def get_point_progress(self):
        try:
            await self._initialize_browser()
            await self.page.goto('https://rewards.bing.com/?ref=rewardspanel', timeout=100000)

            breakdown_button = await self.page.wait_for_selector('.pointbreakdownlink.ng-scope.c-call-to-action.c-glyph.f-lightweight')
            await breakdown_button.click()
            logging.info("已点击积分详情按钮")

            progress_element = await self.page.wait_for_selector('p.pointsDetail')
            progress_text = await progress_element.inner_text()
            progress_text = progress_text.strip()

            logging.info(f"获取到的积分进度文本: {progress_text}")

            if '/' in progress_text:
                left, right = progress_text.split('/')
                return left.strip() == right.strip()

            return False

        except Exception as e:
            logging.error(f"获取积分进度时出错: {str(e)}")
            return False
        finally:
            await self._cleanup()