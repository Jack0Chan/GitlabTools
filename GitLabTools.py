from playwright.sync_api import sync_playwright
from typing import List
import time


class GitLabTools:
    def __init__(self, gitlab_url: str):
        self.url = gitlab_url

        self.__playwright = sync_playwright().start()
        self.__browser = self.__playwright.chromium.launch(headless=False)
        self.__context = self.__browser.new_context()
        self.__page = self.__context.new_page()

    def __del__(self):
        self.__context.close()
        self.__browser.close()
        self.__playwright.stop()

    def sign_in(self, account: str, password: str):
        sign_in_url = self.url + "/users/sign_in"
        sign_in_url = sign_in_url.replace('//', '/')

        self.__page.goto(sign_in_url)
        self.__page.locator("input[name=\"user\\[login\\]\"]").fill(account)
        self.__page.locator("input[name=\"user\\[password\\]\"]").fill(password)
        self.__page.locator("text=Sign in").click()
        time.sleep(0.2)
        return None

    def create_new_account(self, name: str, username: str, mail: str):
        add_new_url = self.url + '/admin/users/new'
        add_new_url = add_new_url.replace('//', '/')

        self.__page.goto(add_new_url)
        self.__page.locator("input[name=\"user\\[name\\]\"]").fill(name)
        self.__page.locator("input[name=\"user\\[username\\]\"]").fill(username)
        self.__page.locator("input[name=\"user\\[email\\]\"]").fill(mail)
        time.sleep(0.5)
        self.__page.locator("text=Create user").click()
        # 最少等3秒再发送邮件，防止被ban
        time.sleep(3)
        return None

    def create_new_group(self, group_name: str):
        create_group_url = self.url + '/groups/new'
        create_group_url = create_group_url.replace('//', '/')

        self.__page.goto(create_group_url)
        self.__page.locator("h3:has-text(\"Create group\")").click()
        # 组名
        self.__page.locator('input#group_name').fill(group_name)
        # 组等路径
        self.__page.locator('input#group_path').fill(group_name)
        with self.__page.expect_navigation():
            self.__page.locator("input:has-text(\"Create group\")").click()
        time.sleep(1)
        return None

    def create_new_blank_project(self, project_name: str, assign_to: str):
        """
        给assign_to的用户创建Private的Project
        """
        create_proj_url = self.url + '/projects/new#blank_project'
        create_proj_url = create_proj_url.replace('//', '/')

        self.__page.goto(create_proj_url)
        # 填写项目名
        self.__page.locator('xpath=//html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/div/div/form/div[1]/div[1]/input').fill(project_name)
        # 选择assign的用户
        self.__page.locator("[id=\"__BVID__15__BV_toggle_\"]").click()
        time.sleep(0.1)
        self.__page.locator(f"button[role=\"menuitem\"]:has-text(\"{assign_to}\")").click()
        time.sleep(0.1)
        # 点击创建项目
        self.__page.locator('xpath=//html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/div/div/form/input[2]').click()
        time.sleep(0.5)

    def invite_group_members(self, group_name: str, members: List[str], role='Maintainer'):
        """
        members可以是邮箱，可以是用户名
        """
        group_url = self.url + f'/groups/{group_name}/-/group_members'
        group_url = group_url.replace('//', '/')

        # 页面一直在刷新，会超时。我们等待commit结束就可以了，没必要等刷新完
        self.__page.goto(group_url, wait_until='commit')

        # 添加成员
        for member in members:
            self.__page.locator("#s2id_autogen1").fill(member)
            time.sleep(0.5)
            self.__page.locator("#s2id_autogen1").press("Enter")
        # 设置权限
        level_dict = {'Guest': '10', 'Reporter': '20', 'Developer': '30', 'Maintainer': '40', 'Owner': '50'}
        self.__page.locator('select#access_level').select_option(level_dict[role])
        # 点击邀请
        self.__page.locator("[data-testid=\"invite-users-form\"] >> text=Invite").click()
        return None
