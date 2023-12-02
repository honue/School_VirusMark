import json
import requests


class Data:
    def __init__(self, school: str, sno: str, jing: float, wei: float, province: str, city: str, district: str,
                 street: str) -> None:
        self.school = str(school)
        self.sno = str(sno)
        self.jing = jing
        self.wei = wei
        self.province = province
        self.city = city
        self.district = district
        self.street = street

    def login(self, auth_token):
        auth_url = "https://xyfyapi.jx.edu.cn/ali-pay/login"
        headers = {
            'Accept-Charset': 'utf-8',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20A5312j Ariver/1.1.0 AliApp(AP/10.2.76.6000) Nebula WK RVKType(0) AlipayDefined(nt:WIFI,ws:390|780|3.0) AlipayClient/10.2.76.6000 Language/zh-Hans Region/CN NebulaX/1.0.0',
            'Referer': 'https://2021001118673392.hybrid.alipay-eco.com/2021001118673392/0.2.2204231510.33/index.html#pages/home/index',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Accept': '*/*'
        }
        data_json = "{\"app_id\":\"2021001118673392\",\"auth_code\":\"%s\",\"id_card_md5\":\"\",\"card_id\":\"\",\"name\":\"\"}" % auth_token

        sess = requests.session()
        response = sess.post(auth_url, headers=headers, data=data_json)
        token_info = json.loads(response.text)
        if token_info["message"] == "Success":
            print("token1获取成功")  # return token_info["info"]["token"]
        else:
            print("error token1获取失败")

        get_token_url = 'https://xyfyapi.jx.edu.cn/user/get-user-info'
        token1 = token_info["info"]["token"]
        headers = {
            'Accept-Charset': 'utf-8',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20A5312j Ariver/1.1.0 AliApp(AP/10.2.76.6000) Nebula WK RVKType(0) AlipayDefined(nt:WIFI,ws:390|780|3.0) AlipayClient/10.2.76.6000 Language/zh-Hans Region/CN NebulaX/1.0.0',
            'Referer': 'https://2021001118673392.hybrid.alipay-eco.com/2021001118673392/0.2.2204231510.33/index.html#pages/home/index',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Accept': '*/*',
            'Authorization': token1,
        }
        sess = requests.session()
        response = sess.post(get_token_url, headers=headers)
        token_info = json.loads(response.text)

        if token_info["message"] == "Success":
            card_id = token_info["info"]["card_id"]
            id_card_md5 = token_info["info"]["id_card_md5"]
            token2 = token_info["info"]["token"]
            self.login_url = "https://fxgl.jx.edu.cn/"+self.school+"/third/alipayLogin?cardId=%s&sfzMd5=%s&token=%s" % (
                card_id, id_card_md5, token2)
        else:
            print("error 获取token2失败 登录url拼接失败")

    def post(self):
        try:
            sess = requests.session()
            sess.get(self.login_url)
            url_json = 'https://fxgl.jx.edu.cn/' + self.school + '/studentQd/saveStu'
            position = self.province + self.city + self.district + self.street
            js = {"xszt": "0", "lng": self.jing, "lat": self.wei, "province": position, "city": self.city,
                  "district": self.district, "street": self.street, "sddlwz": position, "mqtw": "0", "mqtwxq": "",
                  "zddlwz": position,
                  "bprovince": self.province, "bcity": self.city, "bdistrict": self.district, "bstreet": self.street,
                  "sprovince": self.province, "scity": self.city, "sdistrict": self.district, "sfby": "1", "jkzk": "0",
                  "jkzkxq": "", "sfgl": "1", "gldd": ""}
            r_json = sess.post(url=url_json, data=js)
            print(json.loads(r_json.text)['msg'])
        except:
            print("未知错误")

    def verify(self):
        print(self.login_url)
        sess = requests.session()
        sess.get(self.login_url)
        # 查询数据签到
        url_json = 'https://fxgl.jx.edu.cn/' + self.school + '/studentQd/studentIsQd'
        try:
            r_json = sess.post(url=url_json)
            msg = json.loads(r_json.text)
            if msg["data"] == 1:
                print(self.sno + " 已签到")
            else:
                print(self.sno + " 未签")
        except:
            print("数据错误")


def main(*args):
    # 参数需修改 1.学校代码 2.个人学号 3，4.打卡位置的经纬 5，6，7，8 按照打卡位置填对应经纬
    data = Data("4136010403", "8000123456", 115.801325, 28.656317, "江西省", "南昌市", "红谷滩区", "学府大道999号")
    # 填写auth_token
    data.login(auth_token="ec0ff2591a08189f17f84")  # 相比原来认证方式发生了改变 需要抓包获取auth_code
    # 上传打卡数据
    data.post()
    # 验证打卡
    data.verify()


if __name__ == '__main__':
    main()
