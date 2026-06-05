from wsgiref import headers

import requests
import time
import random
import base64



class AuthManager:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.token_type = None
        self.expires_time = 0  # 记录 accessToken 过期时间
        self.header = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuYmkuemtzaGxtLmNvbSIsImF1ZCI6ImFwaS5iaS56a3NobG0uY29tIiwiaWF0IjoxNzQzMjQxNTg5LCJuYmYiOjE3NDMyNDE1ODksImV4cCI6MTc0Mzg0NjM4OSwiYXV0aCI6IiIsImp0aSI6eyJpZCI6IjI1MzUiLCJ0eXBlIjoiYXBpIn19.Wstqo7OeVgWwJmWvpDvJQAkZ6T48_BNCELiPPn1OjDU"
    def is_token_valid(self):
        return int(time.time() * 1000) < self.expires_time

    def refresh_access_token(self):
        if not self.refresh_token:
            print("❌ 无 refreshToken，无法刷新！")
            return False

        refresh_url = "https://www.aircasyqc.cn:8032/canteen-server/app-api/system/auth/refresh"
        payload = {"refreshToken": self.refresh_token}
        headers = {"Content-Type": "application/json;charset=UTF-8"}

        try:
            print("🔄 正在刷新 accessToken...")
            response = requests.post(refresh_url, json=payload, headers=headers)
            response.raise_for_status()  # 检查 HTTP 错误
            data = response.json()
            if data.get("code") == 0:
                self.access_token = data["data"]["accessToken"]
                self.refresh_token = data["data"]["refreshToken"]
                self.expires_time = int(time.time() * 1000) + 3600 * 1000  # 假设 accessToken 有效期 1 小时
                print(f"✅ accessToken 刷新成功: {self.access_token}")
                return True
            else:
                print(f"❌ accessToken 刷新失败: {data['msg']}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return False

    def login(self):
        login_url = "https://www.aircasyqc.cn:8032/canteen-server/app-api/system/auth/login"
        payload = {
            "mobile": "13500486641",
            "nickName": "王亮",
            "openid": "osU5U5f81PUcSm8k-dxE64avPhvQ"
        }
        headers = {"Content-Type": "application/json;charset=UTF-8"}

        try:
            print("🔐 正在登录...")
            response = requests.post(login_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                self.access_token = data["data"]["accessToken"]
                self.refresh_token = data["data"]["refreshToken"]
                self.expires_time = int(time.time() * 1000) + 3600 * 1000
                print(f"✅ 登录成功！新的 accessToken: {self.access_token}")
                return True
            else:
                print(f"❌ 登录失败: {data['msg']}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return False

    def check_login(self):
        if not self.access_token or not self.is_token_valid():
            print("⚠️ accessToken 失效，尝试刷新...")
            if not self.refresh_access_token():
                print("🔄 无法刷新 accessToken，重新登录...")
                self.login()

        url = "https://api.bi.zkshlm.com/reserve/third/order/checkLogin"
        headers = {
            "Host": "api.bi.zkshlm.com",
            "Connection": "keep-alive",
            "Content-Length": "2",  # 注意：实际请求体长度为 2（如空字典 {}）
            "Authori-zation": f"Bearer {self.header}",  # 确保此处正确传递动态 Token
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://yyfu.zkshlm.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://yyfu.zkshlm.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        print(f"🔍 使用 accessToken: {self.access_token}")
        print(f"🔍 请求头: {headers}")
        try:
            response = requests.post(url, json={}, headers=headers)
            print(f"🔍 响应状态码: {response.status_code}")
            print(f"📜 响应内容: {response.text}")

            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    print("✅ 登录状态有效！")
                else:
                    print(f"❌ 登录验证失败: {data.get('msg')}")
            elif response.status_code == 401:
                print("❌ 401 Unauthorized - accessToken 可能无效！")
                self.login()
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")

    #这个接口是检查登录是否成功之后的查询用户姓名等等的接口 post
    def getUserInfo(self):
        url = "https://api.bi.zkshlm.com/reserve/schedule/scheduleServices/getUserInfo"
        headers = {
            "Authori-zation": f"Bearer {self.header}",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://yyfu.zkshlm.com",
            "Referer": "https://yyfu.zkshlm.com/"
        }
        json = {
            "item_name":"乒乓球",
        }
        try:
            response = requests.post(url, json=json, headers=headers)
            print(f"响应状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json().get("data")
                print("getinfo")
                print("返回数据为",data)
            else:
                print("失败获取")
        except requests.exceptions.RequestException as e:
            print("请求失败")

    #下面要实现获取时间信息接口
    def getTimeBlock(self):
        url = "https://api.bi.zkshlm.com/reserve/schedule/scheduleServices/getTimeBlock"
        headers = {
            "Authori-zation": f"Bearer {self.header}",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://yyfu.zkshlm.com",
            "Referer": "https://yyfu.zkshlm.com/"
        }
        ##这里面的时间可能需要自己修改，后期可以优化
        json = {
            "day_time":"2025-3-29",
            "item_name":"乒乓球",
            "selectStatus":"全部"
        }
        try:
            response = requests.post(url, json=json, headers=headers)
            print(f"响应状态码: {response.status_code}")
            if response.status_code == 200:
                print(response.json())
                data = response.json().get("data")
                result = [item for item in data
                          if item['time_content'] == '11:30-12:30'
                          and item['num'] == '01']
                if(len(result) <= 0 or result[0].get('disable_text') == '11:30-12:30'):
                    print("有8.30的空场地")
                else:
                    print("没有空场地了")
            else:
                print("失败获取")
        except requests.exceptions.RequestException as e:
            print("请求失败")
    def solve_captcha(self):
        """处理滑动验证码（示例逻辑）"""
        url = "https://api.bi.zkshlm.com/reserve/common/index/get"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json;charset=UTF-8",
            "Authori-zation": f"Bearer {self.header}",
        }
        payload = {
            "captchaType": "blockPuzzle",
            "clientUid": f"slider-{random.randint(1000, 9999)}",  # 动态生成客户端ID
            "ts": int(time.time() * 1000)
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                captcha_data = response.json().get("data")
                self.token_type = captcha_data.get("token")
                print(self.token_type)
                base64_image = captcha_data.get("data", {}).get("originalImageBase64")
                if base64_image:
                    # 解码Base64数据
                    image_data = base64.b64decode(base64_image)

                    # 将解码后的数据保存为文件
                    with open('captcha_image.png', 'wb') as f:
                        f.write(image_data)
                    print("✅ 验证码图像已保存为 captcha_image.png")

                    # 进行图像识别，寻找缺口
                    self.solve_slider_captcha('captcha_image.png')

                return captcha_data.get("token")
            else:
                print(f"❌ 验证码获取失败: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 验证码请求异常: {str(e)}")
            return None

    def win(self):
        url = "https://api.bi.zkshlm.com/reserve/schedule/scheduleOrder/createOrder"
        k = self.token_type
        print(k)
        json = {
            "captchaToken": k,
            "item_name": "乒乓球",
            "name":"王亮",
            "unit":"三室",
            "value":"3049",
            "time_content":"12:30~13:30",
            "num":"02",
            "day_time":"2025-3-29",
            "phone":"13500486641",
        }
        headers = {
            "Authorization":f"Bearer {self.header}",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://yyfu.zkshlm.com",
            "Referer": "https://yyfu.zkshlm.com/"
        }
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            print(response.status_code)
            print(response.json())

        # 🔥 运行
auth_manager = AuthManager()
auth_manager.check_login()
auth_manager.getUserInfo()
auth_manager.getTimeBlock()
auth_manager.solve_captcha()
time.sleep(1)
auth_manager.win()