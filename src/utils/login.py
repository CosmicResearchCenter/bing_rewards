import json
from playwright.sync_api import sync_playwright, Page

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

if __name__ == '__main__':
    auth_file_name = 'auth.json'
    auth_file_name = input(f'请输入要保存的登录状态文件名（默认为 {auth_file_name}）：') or auth_file_name
    save_login_state(auth_file=auth_file_name)