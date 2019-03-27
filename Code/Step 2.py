import sys
import pymongo
from kafka import KafkaProducer
from linebot.models import *
import time
import MySQLdb
import re
from os import path

"""
載入我們自用的工具包

"""
sys.path.append(path.dirname(sys.path[0]))
from Code.MyUtil import *
from Code.pylineliff.liff_api import *


"""

啟用伺服器基本樣板

"""

from flask import Flask, request, abort, render_template_string, redirect


from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入Follow事件
from linebot.models import FollowEvent

# 載入requests套件
import requests

""" Define Kafka Producer"""

producer = KafkaProducer(bootstrap_servers=["kafka:9093"],
                         key_serializer=str.encode,
                         value_serializer=lambda x: json.dumps(x).encode("utf-8"))

""" Basic File Data """

line_secret_file = path.join(sys.path[0], "line_secret_key")
secretFileContentJson = json.load(open(line_secret_file, 'r'))
channel_access_token = secretFileContentJson["channel_access_token"]
secret_key = secretFileContentJson["secret_key"]
self_user_id = secretFileContentJson["self_user_id"]
rich_menu_id = secretFileContentJson["rich_menu_id"]
server_url = secretFileContentJson["server_url"]

# 設定Server啟用細節
app = Flask(__name__, static_folder="./Images", static_url_path="/Images")

# 生成實體物件
# line-bot
# 給予 one paramater channel_access_token
# 給予 公司章 讓 line_bot_api 送到 LINE時 能被認證為我們的人員
line_bot_api = LineBotApi(channel_access_token)

# 生成 handler
# 要給予認證章 以便 handler 辨識出給我們的訊息
handler = WebhookHandler(secret_key)


# 啟動server對外接口，使Line能丟消息進來
# LINE 都是透過 POST 來發送訊息


@app.route("/", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body : " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


"""
用戶follow 就給目前的菜單

"""

# 準備 greeting 訊息
greeting_message_list = [
    TextSendMessage(
        text="歡迎來到台北美食戰情室"
    ),
    TextSendMessage(
        text="請使用下方功能選單"
    ),
    TextSendMessage(
        text="任何問題，請使用 [聯絡我們]"
    )

]


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    # 先取出用戶資料
    user_id = line_bot_api.get_profile(event.source.user_id)

    # 將用戶資訊存在檔案內
    with open("./users.txt", "a+") as myfile:
        myfile.write(json.dumps(vars(user_id), sort_keys=True))
        myfile.write("\r\n")

    # 將 菜單綁至用戶上
    linkRichMenuId = rich_menu_id
    linkMenuEndpoint = 'https://api.line.me/v2/bot/user/%s/richmenu/%s' % (event.source.user_id, linkRichMenuId)
    linkMenuRequestHeader = {'Content-Type': 'image/jpeg', 'Authorization': 'Bearer %s' % channel_access_token}
    lineLinkMenuResponse = requests.post(linkMenuEndpoint, headers=linkMenuRequestHeader)
    app.logger.info("Link Menu to %s status :" % user_id, lineLinkMenuResponse)
    # 回覆文字消息與圖片消息
    line_bot_api.reply_message(
        event.reply_token,
        greeting_message_list
    )


""" Global Function Generate LIFF ID """


def apply_liff_id(userid, route, pattern):
    if type(pattern) != str:
        raise ValueError('Pattern can only be string e.g: (compact, tall, full)')
    elif type(route) != str:
        raise ValueError('Route can only be string without / e.g: (compact, tall, full)')
    elif route.find("/") != -1:
        raise ValueError('Route can only be string without / e.g: (compact, tall, full)')

    # make sure userid is string
    userid = str(userid)
    liff_init(access_token=channel_access_token)
    liff_url = "https://%s/%s%s" % (server_url, route, userid)

    # make sure liff amount not exceed 15
    if liff_list().get("apps") is not None:
        if len(liff_list().get("apps")) >= 15:
            for every_liff in liff_list().get("apps"):
                liff_delete(every_liff.get("liffId"))

    liff_app_id = liff_add(liff_url, pattern)

    return liff_app_id


"""
針對 [::text:] 吃啥 的回應


"""


def flex_send_whateat():
    bubble_list = cluster_bubbles()
    content = CarouselContainer.new_from_json_dict(json.loads(gen_flex(bubble_list)))
    Flex_message = FlexSendMessage(alt_text="flex", contents=content)
    return Flex_message


def flex_return_whateat(cluster):
    cluster = str(cluster)
    a = MyAccount()
    # charset = utf-8
    conn = MySQLdb.connect(a.host, a.account, a.passwd, db="test", charset="utf8")

    days = get_days()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT Name,rate,address,%s,phone,image 
        from res_2 
        where rate >= 3 && %s != '' && cluster = '%s' 
        order by rand() 
        limit 5""" % (days, days, cluster))
    tu = cursor.fetchall()
    conn.close()

    # 對 Tuple 內所有參數 使用 gen_bubble 產生 bubble_message
    # 用 map 搭配 lambda
    # 再用 list 包住 傳給 gen_flex 產生 flexMessage
    bubble_list = list(map(lambda x: gen_bubble(x, server_url=server_url), tu))

    bubble_content = gen_flex(bubble_list)
    flex_content = CarouselContainer.new_from_json_dict(json.loads(bubble_content))

    Flex_message = FlexSendMessage(alt_text="Flex", contents=flex_content)
    return Flex_message


"""

# # 針對圖片推薦的回應
# 
# ## 這邊預計要放入 html 來點選圖片
# 
# 
# 流程 
# 
# 先回覆flex 點選兩個圖片選一
# 
# 回傳後再次送兩個選一
# 
# 重複上述
# 
# 算出推薦後回覆

"""


# 塞進 flex bubble
def graph_liff_message(userID):
    User = userID
    liff_id = apply_liff_id(User, route='graphLIFF=', pattern='tall')
    graph_liff_url = "line://app/%s" % liff_id.get("liffId")

    liff_flex_bubble = graph_bubble(graph_liff_url)

    bubble_container = BubbleContainer.new_from_json_dict(json.loads(liff_flex_bubble))

    liff_message = FlexSendMessage(alt_text="Check on your phone", contents=bubble_container)
    return liff_message


"""
針對 [::text:] 圖片推薦 的回應


"""

"""
[::text:] 圖片推薦 get_img_reply_flex()
"""


@app.route("/graphLIFF=<userid>")
def graph(userid):
    html = get_image_reply_html(userid)

    return render_template_string(html)


@app.route("/post_graph", methods=["POST"])
def post_graph():
    body = json.loads(request.get_data(as_text=True))

    user = body.get("user")
    user_graph = body.get("graph")

    graph_future = producer.send(topic="mytopics", key=user, value=list(user_graph.values()))
    graph_future.get(timeout=50)
    print(body)

    line_bot_api.push_message(
        body.get("user", None),
        TextSendMessage(
            text="Your select graph data is get by lineBot ! Please Wait"
        )
    )

    return "OK"


"""
# # 針對位置推薦
# 
# 
# ### 流程 :
# 
# 用戶點了位置推薦 -> 取得用戶ＩＤ 並裝進 HTML LIFF -> 用戶點了回傳位置後 -> 傳回 post back location 接口 並傳回告知可關閉資訊
# 
# 
# -> 接口取得用戶ＩＤ與位置資訊後 分析位置模式 判斷在哪個公車上 -> 推薦資訊透過推播訊息完成

"""


@app.route("/liffID=<userid>")
def liffID(userid):
    html = location_reply(userid=userid)

    return render_template_string(html)


def location_liff_message(userid):
    user = userid

    liff_id = apply_liff_id(user, route='liffID=', pattern='compact')
    location_liff_url = "line://app/%s" % liff_id.get("liffId")

    liff_flex_bubble = location_bubble(location_liff_url)

    bubble_container = BubbleContainer.new_from_json_dict(json.loads(liff_flex_bubble))
    liff_message = FlexSendMessage(alt_text="Check on your phone", contents=bubble_container)

    return liff_message


"""
# # 處理丟過來的 位置資訊
# 
# ## 算出週圍多邊形後
# 
# ## 丟入 sql st_within
# 
# ## push 推薦內容


"""


@app.route("/post_location", methods=["POST"])
def post_location():
    body = json.loads(request.get_data(as_text=True))

    with open("./location.txt", "a+") as f:
        f.write(json.dumps(body))

        f.write("\r\n")
    line_bot_api.push_message(
        body.get("user", None),
        TextSendMessage(
            text="Your data is get by lineBot ! Please Wait"
        )
    )

    location = body.get("location")
    sql_location_string = ""
    if location:

        lat = location[2].get("lat")
        lon = location[2].get("lng")
        tups = count_gps(lat, lon)

        new_tuple = ()
        for tup in tups:
            lat, lon = tup
            req_string = ""
            req_string += str(lat) + " " + str(lon)
            new_tuple += (req_string,)

        sql_location_string += ",".join(new_tuple)

    else:
        # android 無法使用 LIFF geolocation
        line_bot_api.push_message(
            body.get("user", None),
            [TextSendMessage(
                text="抱歉 !請以Chrome開啟網頁並重試"
            ),
                TextSendMessage(
                    text="https://%s/liffID=%s" % (server_url, body.get("user"))
                )]
        )
        return "OK"

    # connect to sql
    a = MyAccount()
    # charset = utf-8
    conn = MySQLdb.connect(a.host, a.account, a.passwd, db="test", charset="utf8")
    cursor = conn.cursor()
    days = get_days()
    tu = ()
    if sql_location_string:
        sql_string = """SELECT Name,rate,address,%s,phone 
            from res 
            where (select ST_Within(
                res.geo,
                ST_GeomFromText(
                    'POLYGON((%s))',4326)
                ) = True
                 ) && rate >= 3 && %s != '' 
            order by rand() 
            limit 5""" % (days, sql_location_string, days)

        cursor.execute(sql_string)
        tu = cursor.fetchall()
    if len(tu) == 0:
        line_bot_api.push_message(
            body.get("user", None),
            TextSendMessage(
                text="Sorry ! There is no restaurant near your location"
            )
        )

    else:
        # 對 Tuple 內所有參數 使用 gen_bubble 產生 bubble_message
        # 用 map 搭配 lambda 
        # 再用 list 包住 傳給 gen_flex 產生 flexMessage
        bubble_list = list(map(lambda x: gen_bubble(x, server_url=server_url), tu))
        flex = gen_flex(bubble_list)
        carousel_content = CarouselContainer.new_from_json_dict(json.loads(flex))
        message = FlexSendMessage(alt_text="Check phone", contents=carousel_content)

        line_bot_api.push_message(
            body.get('user', None),
            message
        )

    return "OK"


"""
# # 針對聯絡我們的回應
# 
# ## 這邊要放入主要部份回應 quick button


"""

"""
針對 [::text:] 聯絡我們 的回應


"""

# 創建quick button


# 創建文字快捷
textQuickButton = QuickReplyButton(
    action=MessageAction(
        label="文字消息",
        text="發送這個消息"
    )

)

# 創建選擇日期快捷
dataQuickButton = QuickReplyButton(
    action=DatetimePickerAction(
        label="選擇日期",
        data="data3",
        mode="date",
        initial="2013-04-01",
        min="2011-06-23",
        max="2019-04-23"
    )
)

# 創建相機使用快捷
cameraQuickButton = QuickReplyButton(
    action=CameraAction(
        label="拍個照！開心開心"
    )
)

# 相機卷使用快捷
cameraRollQuickButton = QuickReplyButton(
    action=CameraRollAction(
        label="選擇相片！爽爽爽"
    )
)

# 傳送地點快捷
locationQuickButton = QuickReplyButton(
    action=LocationAction(
        label="上傳地點！ㄏ ㄏ "
    )
)

# PostBack 快捷
postBackQuickButton = QuickReplyButton(
    action=PostbackAction(
        label="我是postback事件",
        display_text='postback text2',
        data='action=buy&itemid=2'

    )
)

# 創建 quick reply button List
quickReplyList = QuickReply(
    items=[textQuickButton,
           dataQuickButton,
           cameraQuickButton,
           cameraRollQuickButton,
           locationQuickButton,
           postBackQuickButton]
)

# 封裝進 textsendMessage
quickReplyTextSendMessage = TextSendMessage(text="發送你的問題！", quick_reply=quickReplyList)

"""
# # 定義Main Page
# 
# ## flask get return html
# 
# ### 傳入餐廳 ID UserID

"""


@app.route("/index/resid=<phone>", methods=["GET"])
def main_page(phone):
    if str(phone) == "Not Available":
        sorryhtml = "<div><img src='https://3dmart.com.tw/upload/news/2015/0924/123.jpg'>抱歉，網頁建置中</div>"

        return render_template_string(sorryhtml)

    a = MyAccount()
    # charset = utf-8
    conn = MySQLdb.connect(a.host, a.account, a.passwd, db="test", charset="utf8")

    cursor = conn.cursor()
    cursor.execute("select image from res_2 where phone=%s" % phone)
    image = cursor.fetchone()[0]
    conn.close()

    m = MongoBase()
    mongo = pymongo.MongoClient("mongodb://mongodb:27017/",
                                username=m.username,
                                password=m.password,
                                authSource=m.authSource,
                                authMechanism=m.authMechanism,
                                connect=False
                                )
    db = mongo["res"]
    col = db["resinfo5"]
    query = {"phone": phone}

    doc = col.find(query, {"_id": 0})

    return render_template_string(res_html(doc, image_url=image))


"""
# # 定義 協同式過濾
# 
# ## 開啟接口給 MainPage ajax request

"""


@app.route("/countRes", methods=["POST"])
def countRes():
    data = json.loads(request.get_data(as_text=True))
    timestamp = time.time()

    resID = data.get("resID")

    response_data = {
        "resID": resID,
    }

    future = producer.send(topic="mytopics",
                           key="timestamp",
                           value=response_data)
    future.get(timeout=50)
    return redirect("https://%s/cosin/time=%s" % (server_url, timestamp))


@app.route("/cosin/time=<timestamp>", methods=["GET"])
def testing(timestamp):
    from kafka import KafkaConsumer
    consumer = KafkaConsumer("mytopics",
                             bootstrap_servers=["kafka:9093"],
                             auto_offset_reset='latest')
    response_data = []

    for msg in consumer:
        if msg.key == timestamp:
            response_data.append(msg.value)

    return "ok"


"""
# # Handler define here
# 
# ### 遇到的問題 : 
# 
# * handler觸發後 回應準備字典內的所有方法都觸發
# 
# * 預期為 : 對應哪個key 只觸發指定的 value
# 
# * 修正 : 定義傳遞方法
# 
# * 另個修正 : 定義空字典 handler 觸發後 重新修改 指定 value 或 方法 

"""


text_reply_dict = {
    1: TextSendMessage(text="醒醒 !"),
    2: TextSendMessage(text="醒 !"),
    3: TextSendMessage(text="你沒有 !"),
    4: TextSendMessage(text="該起床了 !"),
    5: TextSendMessage(text="醒了沒 ?"),
}


def parse_dict(key, userid=None):
    if key == "[::text:] 位置推薦":
        return location_liff_message(userid)
    elif key == "[::text:] 吃啥":
        return flex_send_whateat()
    elif key == "[::text:] 圖片推薦":
        return graph_liff_message(userid)
    elif key == "[::text:] 聯絡我們":
        return quickReplyTextSendMessage
    elif key == "[::text:] 第0群":
        return flex_return_whateat(0)
    elif key == "[::text:] 第1群":
        return flex_return_whateat(1)
    elif key == "[::text:] 第2群":
        return flex_return_whateat(2)
    elif key == "[::text:] 第3群":
        return flex_return_whateat(3)
    elif key == "[::text:] 第4群":
        return flex_return_whateat(4)
    elif key == "[::text:] 第5群":
        return flex_return_whateat(5)
    elif key == "[::text:] 第6群":
        return flex_return_whateat(6)
    elif key == "[::text:] 第7群":
        return flex_return_whateat(7)


"""
Handler 處理進入的所有消息


"""


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.find('::text:') != -1:

        line_bot_api.reply_message(
            event.reply_token,
            parse_dict(key=event.message.text, userid=event.source.user_id))
    elif re.findall(r"妹+|婆+|[女友]+|[女朋友]+", event.message.text):
        line_bot_api.reply_message(
            event.reply_token,
            text_reply_dict.get(random.randint(1, 5)))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請點擊菜單 來取得更多資訊喔"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
