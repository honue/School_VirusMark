import json
import requests


class Data:
    def __init__(self, school: str, tno: str, jing: float, wei: float, province: str, city: str, district: str, street: str) -> None:
        self.school = str(school)
        self.tno = str(tno)
        self.jing = jing
        self.wei = wei
        self.province = province
        self.city = city
        self.district = district
        self.street = street

    def post(self):
        try:
            url = 'https://fxgl.jx.edu.cn/' + self.school + '/public/homeQd?loginName=' + self.tno + '&loginType=1'
            sess = requests.session()
            sess.get(url)
            url_json = 'https://fxgl.jx.edu.cn/' + self.school + '/teacher/saveTea'
            headers = {
                'Host': 'fxgl.jx.edu.cn',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Origin': 'https://fxgl.jx.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Content-type': 'application/x-www-form-urlencoded',
                'Referer': 'https://fxgl.jx.edu.cn/' + self.school + '/user/qdbp',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            position = self.province + self.city + self.district + self.street
            js = {"xszt": "0", "lng": self.jing, "lat": self.wei, "province": position, "city": self.city,
                  "district": self.district, "street": self.street, "sddlwz": position, "mqtw": "0", "mqtwxq": "",
                  "zddlwz": position,
                  "bprovince": self.province, "bcity": self.city, "bdistrict": self.district, "bstreet": self.street,
                  "sprovince": self.province, "scity": self.city, "sdistrict": self.district, "sfby": "1", "jkzk": "0",
                  "jkzkxq": "", "sfgl": "1", "gldd": ""}
            r_json = sess.post(url=url_json, data=js, headers=headers)
            return json.loads(r_json.text)['msg']
        except:
            return "未知错误"

    def verify(self):
        url = 'https://fxgl.jx.edu.cn/' + self.school + '/public/homeQd?loginName=' + self.tno + '&loginType=1'
        sess = requests.session()
        sess.get(url)
        url_json = 'https://fxgl.jx.edu.cn/' + self.school + '/teacher/teacherIsQd'
        headers = {
            'Host': 'fxgl.jx.edu.cn',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://fxgl.jx.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://fxgl.jx.edu.cn/' + self.school + '/user/qdbp',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        try:
            r_json = sess.post(url=url_json, headers=headers)
            msg = json.loads(r_json.text)
            if msg["data"] == 1:
                print(self.tno + " 已签到")
            else:
                print(self.tno + " 未签")
        except:
            print("数据错误")


def main(*args):
    # 参数需修改 1.学校代码 2.个人工号 3，4.打卡位置的经纬 5，6，7，8 按照打卡位置填对应经纬
    data = Data("4136010403", "8000123456", 115.801325, 28.656317, "江西省", "南昌市", "红谷滩区", "学府大道999号")
    # 上传打卡数据
    data.post()
    # 验证打卡
    data.verify()


if __name__ == '__main__':
    main()
