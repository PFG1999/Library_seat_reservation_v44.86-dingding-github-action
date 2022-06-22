from urllib.parse import unquote_plus
import requests
import json
import datetime
import time
import re
import datetime
import requests
import time
import os
import json
import hmac
import hashlib
import urllib
import base64


USERNAME=os.environ["Library_USERNAME"] #账号-->学号
PASSWORD=os.environ["Library_PASSWORD"] #密码
AREA_ID=[10,16] #想要预约的房间编号，默认是8、10，若想添加其他的，可以先运行脚本，会显示出其他房间的编号，再自行添加或者更改，同时越靠前越优先考虑
DD_BOT_ACCESS_TOKEN = os.environ["DD_BOT_ACCESS_TOKEN"]
DD_BOT_SECRET = os.environ["DD_BOT_SECRET"]


# 通过dingding进行通知结果
def inform_by_dingding(error_msg=''):

    timestamp = str(round(time.time() * 1000))  # 时间戳
    secret_enc = DD_BOT_SECRET.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, DD_BOT_SECRET)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # 签名
    print("开始使用 钉钉机器人 推送消息...", end="")
    url = f"https://oapi.dingtalk.com/robot/send?access_token={DD_BOT_ACCESS_TOKEN}&timestamp={timestamp}&sign={sign}"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    if SOMETHING_WRONG == 0:
        data = {
            "msgtype": "text",
            "text": {
                "content": f"📖 图书馆预约结果通知\n---------\n预约用户：{PRINT_NAME}\n\n预约项目：{str(PRINT_AREA_NAME)}\n\n预约情况：✅{AREA_ID_AND_NAME[RESERVE_SEAT[2]]}{RESERVE_SEAT[1]}号\n\n预约时间：{str(datetime.datetime.now())[0:16]}\n\n健康状况：{STATUS}"
            },
        }
    else:
        data = {
            "msgtype": "text",
            "text": {
                "content": f"📖 图书馆预约结果通知\n---------\n预约用户：{PRINT_NAME}\n\n预约项目：{str(PRINT_AREA_NAME)}\n\n预约情况：❌{error_msg}\n\n预约时间：{str(datetime.datetime.now())[0:16]}\n\n健康状况：{STATUS}"
            },
        }
    r = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=15).json()
    if not r['errcode']:
        print('消息经 钉钉机器人 推送成功！')
    else:
        print("dingding:" + str(r['errcode']) + ": " + str(r['errmsg']))
        print('消息经 钉钉机器人 推送失败，请检查错误信息')

# 处理连接超时的情况
def get(url,headers,):
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response
    except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
        global NETWORK_STATUS
        NETWORK_STATUS = False # 请求超时改变状态

        if NETWORK_STATUS == False:
            '''请求超时'''
            for i in range(1, 10):
                print(f'请求超时，第{i}次重复请求')
                # timeout单位为s
                response = requests.get(url=url, headers=headers, timeout=5)
                if response.status_code == 200:
                    return response
    return -1  # 当所有请求都失败，返回  -1  ，此时有极大的可能是网络问题或IP被封。

def post(url,headers,data):
    try:
        response = req.post(url=url, headers=headers, timeout=5,data=data)
        if response.status_code == 200:
            return response
    except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
        global NETWORK_STATUS
        NETWORK_STATUS = False # 请求超时改变状态

        if NETWORK_STATUS == False:
            '''请求超时'''
            for i in range(1, 10):
                print(f'请求超时，第{i}次重复请求')
                # timeout单位为s
                response = req.post(url=url, headers=headers, timeout=5)
                if response.status_code == 200:
                    return response
    return -1  # 当所有请求都失败，返回  -1  ，此时有极大的可能是网络问题或IP被封。

# cookie的寿命为5分钟，所以当到第4分钟的时候直接重新请求
def check_cookie_lifetime():
    global COOKIE_IS_EXPIRED
    expire = req.cookies.get('expire')
    expire_min = int(unquote_plus(expire)[14:16])
    # 这个时间存疑在，在55，00那个时间点
    if expire_min < 5:
        expire_min += 60
    time_list = time.asctime().split(" ")
    if len(time_list) == 5:
        now_min = int(time_list[3][3:5])
    elif len(time_list) == 6:
        now_min = int(time_list[4][3:5])
    else:
        now_min = int(time_list[3][3:5])
    COOKIE_IS_EXPIRED = True if expire_min > now_min else False


# 登录获取cookie
def login_in():
    res = post(url="http://rg.lib.xauat.edu.cn/api.php/login",
                   headers={"Referer": "http://www.skalibrary.com/",
                            "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74"},
                   data={"username": USERNAME, "password": PASSWORD, "from": "mobile"})
    if json.loads(res.content)['status']:
        global COOKIE_IS_EXPIRED
        COOKIE_IS_EXPIRED=0
        print(f"■■■ 姓名   \t{json.loads(res.content)['data']['list']['name']}")
        print(f"■■■登录状态\t{json.loads(res.content)['msg']}")
        global PRINT_NAME
        PRINT_NAME =json.loads(res.content)['data']['list']['name']
    else:
        global SOMETHING_WRONG
        SOMETHING_WRONG = 1
        print("登录失败",json.loads(res.content)['msg'])
        inform_by_dingding(f"登录失败 {json.loads(res.content)['msg']}")

# 获取区域信息,不需要cookie
def get_area_id():
    res = get(url="http://rg.lib.xauat.edu.cn/api.php/areas?tree=1",
                  headers={"Referer": "http://www.skalibrary.com/",
                           "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74"})
    if json.loads(res.content)['status']:
        # 第一层-图书馆信息（可能是两个图书馆），第二层-楼层信息，第三层-空间信息
        for library_info in json.loads(res.content)['data']['list']:
            for floor_info in library_info['_child']:
                for area_info in floor_info['_child']:
                    if area_info['id'] in AREA_ID:
                        print(f"■■■\tid-{area_info['id']}\t{area_info['nameMerge']}")
                        PRINT_AREA_NAME.append(area_info['nameMerge'])
                    else:
                        print(f"   \tid-{area_info['id']}\t{area_info['nameMerge']}")
                    AREA_ID_AND_NAME.update({area_info['id']:area_info['nameMerge']})
                    # 部分未列出的参数，可作为(若某些区域禁止预约)判断依据，尤其注意'isValid'
                    # print(area_info['isValid'])
                    # print(area_info['levels'])
                    # print(area_info['sort'])
                    # print(area_info['type'])
                    # print(area_info['ROW_NUMBER'])
    else:
        global SOMETHING_WRONG
        SOMETHING_WRONG = 1
        print(f"获取区域信息失败 {json.loads(res.content)['msg']}")
        inform_by_dingding(f"获取区域信息失败 {json.loads(res.content)['msg']}")

def url_info():
    for area_id in AREA_ID:
        # 获取url信息,不需要cookie
        res = get(
            url=f"http://rg.lib.xauat.edu.cn/api.php/space_time_buckets?area={area_id}&day={datetime.date.today()}",
            headers={"Referer": "http://www.skalibrary.com/",
                     "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74"})
        if json.loads(res.content)['status']:
            spaceId = json.loads(res.content)['data']['list'][0]['spaceId']
            bookTimeId = json.loads(res.content)['data']['list'][0]['bookTimeId']
            endTime = json.loads(res.content)['data']['list'][0]['endTime']
            day = json.loads(res.content)['data']['list'][0]['day']
            startTime = json.loads(res.content)['data']['list'][0]['startTime']
            # status=json.loads(res.content)['data']['list'][0]['status']可能和禁止预约有关
            seat_info_url=f"http://rg.lib.xauat.edu.cn/api.php/spaces_old?area={area_id}&day={day}&endTime={endTime}&segment={bookTimeId}&startTime={startTime}"
            SEGMENT.append(bookTimeId)
            SEAT_INFO_URL.append(seat_info_url)
        else:
            global SOMETHING_WRONG
            SOMETHING_WRONG = 1
            print(f"获取可预约时间段失败 {json.loads(res.content)['msg']}")
            inform_by_dingding(f"获取可预约时间段失败 {json.loads(res.content)['msg']}")

def seat_info(seat_info_url):
    start=0
    # 获取seat信息,不需要cookie
    res = get(
        url=seat_info_url,
        headers={"Referer": "http://www.skalibrary.com/",
                 "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74"})
    if json.loads(res.content)['status']:
        all_seat_info=json.loads(res.content)['data']['list']
        all_seat_info.reverse()
        for seat_info in all_seat_info:
            seat_id = seat_info['id']
            seat_name = seat_info['name']
            seat_status_name = seat_info['status_name']
            seat_area=seat_info['area']
            if seat_status_name == "空闲":
                RESERVE_SEAT.extend([seat_id,seat_name,seat_area,SEGMENT[start]])
                print(f'■■预约信息■■seat_id {RESERVE_SEAT[0]}■■seat_name {RESERVE_SEAT[1]}■■area_id {RESERVE_SEAT[2]}■■area_segment {RESERVE_SEAT[2]}■■')
                global GET_THE_SEAT
                GET_THE_SEAT = 1
                return
    else:
        global SOMETHING_WRONG
        SOMETHING_WRONG = 1
        print(f"获取空间预约信息失败 {json.loads(res.content)['msg']}")
        inform_by_dingding(f"获取空间预约信息失败 {json.loads(res.content)['msg']}")
    start += 1

def reserve():
    # 预约,需要cookie
    res = post(
        url=f"http://rg.lib.xauat.edu.cn/api.php/spaces/{RESERVE_SEAT[0]}/book",
        headers={"Referer": "http://www.skalibrary.com/",
                 "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74"},
        data = {"access_token": req.cookies.get("access_token"), "userid": USERNAME, "type": 1,"id": RESERVE_SEAT[0],"segment": RESERVE_SEAT[3]})
    if json.loads(res.content)['status']:
        # json.loads(res.content)['msg']--->预约成功<br/>您已违约2次,详情请登录web端或联系管理员
        if "违约" in json.loads(res.content)['msg']:
            global STATUS
            STATUS=re.search("已违约\w次", json.loads(res.content)['msg']).group()
        else:
            STATUS = json.loads(res.content)['msg']
        print(f"{AREA_ID_AND_NAME[RESERVE_SEAT[2]]} 座位号-{RESERVE_SEAT[1]} {STATUS}")
        inform_by_dingding()
    else:
        global SOMETHING_WRONG
        SOMETHING_WRONG = 1
        print(f"预约失败 {json.loads(res.content)['msg']}")
        inform_by_dingding(f"预约失败 {json.loads(res.content)['msg']}")

def cancel_reserve():
    # 注意这里会先查询历史记录，并向RESERVE_SEAT里append一个id编号，不要与自动刷新座位时的append混用
    # 获取预约历史信息,需要cookie:userid=2102210421;access_token=d810f72e23effcd671571dba9d9726df
    res = get(
        url=f"http://rg.lib.xauat.edu.cn/api.php/profile/books/",
        headers={
            "Referer": "http://rg.lib.xauat.edu.cn/user/index/book",
            "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74",
            'Cookie': f'userid={USERNAME};access_token={req.cookies.get("access_token")}'})
    if json.loads(res.content)['data']['list'][0]['statusName'] == '预约开始提醒':
        print('■■■预约状态   \t预约中&未签到')
        RESERVE_SEAT.append(json.loads(res.content)['data']['list'][0]['id'])
        # 取消预约
        res = post(
            url=f"http://rg.lib.xauat.edu.cn/api.php/profile/books/{RESERVE_SEAT[0]}",
            headers={
                "Referer": "http://rg.lib.xauat.edu.cn/user/index/book",
                "User-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.74",
                'Cookie': f'userid={USERNAME};access_token={req.cookies.get("access_token")}'},
            data={"access_token": req.cookies.get("access_token"), "userid": USERNAME, "_method": 'delete',
                  "id": RESERVE_SEAT[0]})
        if json.loads(res.content)['status'] == 0:
            print('■■■取消预约   \t当日取消次数已达上限')
            inform_by_dingding('取消预约   \t当日取消次数已达上限')
        elif json.loads(res.content)['status'] == 1:
            print('■■■取消预约   \t成功取消')
            inform_by_dingding('取消预约   \t成功取消')
        else:
            print('■■■取消预约   \t取消预约失败：', json.loads(res.content))
            inform_by_dingding('取消预约   \t取消预约失败', json.loads(res.content))
    else:
        print('■■■取消预约   \t未预约或者预约超时，无需取消预约')
        inform_by_dingding('取消预约   \t未预约或者预约超时，无需取消预约')


if __name__ == '__main__':

    COOKIE_IS_EXPIRED=1
    SOMETHING_WRONG=0
    GET_THE_SEAT=0

    AREA_ID_AND_NAME = {}
    SEAT_INFO_URL = []
    RESERVE_SEAT = []  # 座位id,座位name,座位所在房间的编号,座位所在房间对应的segment
    SEGMENT = []
    STATUS=''
    PRINT_NAME = ''
    PRINT_AREA_NAME = []

    while COOKIE_IS_EXPIRED and not GET_THE_SEAT:

        req=requests.session()

        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
        login_in()
        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")

        # 获取区域id信息，便于选择,仅作展示用，且只执行一次
        get_area_id()
        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")

        ################################功能一：预约座位################################
        ###############################################################################
        # 获取url信息，便于构造获取seat信息的url地址
        url_info()
        while not COOKIE_IS_EXPIRED and not GET_THE_SEAT:
            for seat_info_url in SEAT_INFO_URL:
                if not COOKIE_IS_EXPIRED and not GET_THE_SEAT:
                    seat_info(seat_info_url)
                    if RESERVE_SEAT:
                        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
                        COOKIE_IS_EXPIRED = check_cookie_lifetime()
                        if not COOKIE_IS_EXPIRED:
                            reserve()
                        else:
                            AREA_ID_AND_NAME = {}
                            SEAT_INFO_URL = []
                            RESERVE_SEAT = []
                            SEGMENT = []
                            GET_THE_SEAT = 0
        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
        ###############################################################################
        ###############################################################################

        if SOMETHING_WRONG:
            break

        if COOKIE_IS_EXPIRED==1:
            continue

        ################################功能二：取消预约################################
        ###############################################################################
        # cancel_reserve()
        # print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
        # break
        ###############################################################################
        ###############################################################################
