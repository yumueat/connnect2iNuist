from playwright.sync_api import Playwright, sync_playwright
from pathlib import Path

def run(playwright: Playwright,user_name: str,password: str,flag: str) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://10.255.255.34/authentication")
    page.fill("text=网络认证登录自动登录 漫游免认证 登 录 >> [placeholder=\"用户名\"]", user_name)
    page.fill("text=网络认证登录自动登录 漫游免认证 登 录 >> [placeholder=\"密码\"]", password)
    page.click("text=网络认证登录弱自动登录 漫游免认证 登 录 >> button")
    try:
        with page.expect_navigation():
            if flag == '1':
                page.click("button:has-text(\"中国移动\")")
            elif flag == '2':
                page.click("button:has-text(\"中国电信\")")
            elif flag == '3':
                page.click("button:has-text(\"中国联通\")")
    except:
        print("出现了一些问题，可能是用户名、密码、网络输入错误，也可能是因为网络原因登录失败，请检查后重试")
    if page.url == "http://10.255.255.34/authentication/detail":
        print("连接成功")
    context.close()
    browser.close()

def main():
    user_info = Path("user_info.txt")
    information = []
    if user_info.exists():
        with open("user_info.txt","r") as f:
            for line in f:
                information.append(line.strip())
        with sync_playwright() as playwright:
            run(playwright,information[0],information[1],information[2])

    else:
        user_name = input("请输入用户名")
        password = input("请输入密码")
        flag = input("请选择网络\n1.中国移动 2.中国电信 3.中国联通")
        with open("user_info.txt","w") as f:
            f.write(user_name+"\n"+password+"\n"+flag)
        with sync_playwright() as playwright:
            run(playwright,user_name,password,flag)

if __name__ == '__main__':
    main()