from playwright.sync_api import sync_playwright
import time
import random

def main():
    with sync_playwright() as p:
        try:
            # 启动浏览器并加载登录状态
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                storage_state="yzg.json"  # 你的登录状态文件
            )
            page = context.new_page()

            # 访问目标页面，增加超时时间
            page.goto("https://rewards.bing.com/?ref=rewardspanel", timeout=100000)
            
            # 等待页面加载完成
            # page.wait_for_selector('.mee-icon.mee-icon-AddMedium', timeout=100000)

            # 获取所有目标元素
            cards = page.query_selector_all('.mee-icon.mee-icon-AddMedium')
            
            print(f"找到 {len(cards)} 个可点击卡片")

            # 依次点击每个卡片
            for index, card in enumerate(cards, 1):
                print(f"正在点击第 {index} 个卡片...")
                
                # 点击卡片并等待新页面打开
                with page.expect_popup() as new_page_info:
                    card.click()
                
                # 获取新页面并关闭
                new_page = new_page_info.value
                new_page.close()
                
                # 随机等待5-10秒
                sleep_time = random.uniform(5, 10)
                time.sleep(sleep_time)

            print("所有卡片点击完成！")

        except Exception as e:
            print(f"运行出错：{str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()