import pytz
import datetime
from math import radians, cos, pi

"""
主要工具包
產生 LINE Bubble
產生 LINE Flex
計算地理位置
均在此處完成

"""

""" 分群的 Bubble """


def cluster_bubbles():

    def gen_every_cluster_bubble(*tup):
        cluster_name = None
        img_url = None
        cluster_number = None
        if tup:
            cluster_name, img_url, cluster_number = list(*tup)

        bubble = """
    {
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": "%s",
          "size": "sm",
          "align": "center",
          "weight": "bold",
          "color": "#AAAAAA"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "%s",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Action",
        "uri": "%s"
      }
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "md",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "flex": 2,
          "contents": [
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "spacer"
                },
                {
                  "type": "spacer"
                }
              ]
            },
            {
              "type": "text",
              "text": " ＊ 請至少選擇一群",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "bottom"
            },
            {
              "type": "spacer"
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "message",
            "label": "選擇",
            "text": "[::text:] 第%s群"
          }
        }
      ]
    }
  }
      """ % (cluster_name, img_url, img_url, cluster_number)

        return bubble

    define_cluster = [
        ("平價美食",
         "https://img.sunnylife.tw/pixnet/d018bb14eeef9104009c4e2e015de79f.jpg", 0),
        ("北方麵食",
         "https://i1.wp.com/img.kokoha.tw/uploads/20180503175426_45.jpg", 1),
        ("聚餐首選",
         "https://i0.wp.com/img.jennifersmilecc.com/20171030133714_30.jpg", 2),
        ("傳承老店",
         "https://www.mirrormedia.com.tw/assets/images/20190210135019-193e927d818f4c207b872a2d4268acc5-tablet.jpg", 3),
        ("背包族最愛",
         "https://cw1.tw/CH/club/images/article/201802/article-5a795d7a75c28.jpg", 4),
        ("打卡名店",
         "https://cdn.walkerland.com.tw/images/upload/subject/b5ed1ee0a60189371ba01bc512550765e35fbfd3.jpg", 5),
        ("口袋夠深",
         "https://kenalice.tw/wp-content/uploads/2017/08/1502989242-1ec6eaf1be94f8778c3861ec16e07fd6.jpg", 6),
        ("老饕聖地",
         "https://a4.att.hudong.com/11/05/16200000028160133878050163025.jpg", 7)
    ]
    return list(map(gen_every_cluster_bubble, define_cluster))


""" 給予用戶點選圖片的 Bubble """


def graph_bubble(liff_url):
    if type(liff_url) != str:
        raise ValueError('liff url should be string')

    bubble = """
    {
    "type": "bubble",
    "direction": "ltr",
    "hero": {
      "type": "image",
      "url": "https://png.pngtree.com/element_our/sm/20180620/sm_5b29c1925a478.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "fit",
      "backgroundColor": "#7F86E8",
      "action": {
        "type": "uri",
        "label": "Line",
        "uri": "%s"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "圖片推薦",
          "size": "xl",
          "align": "center",
          "weight": "bold"
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "separator",
              "margin": "none",
              "color": "#FFFFFF"
            },
            {
              "type": "text",
              "text": "點選一系列圖片",
              "size": "lg",
              "align": "center"
            },
            {
              "type": "separator",
              "color": "#FFFFFF"
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "將根據你的選擇來推薦",
                  "size": "md",
                  "align": "center"
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "flex": 0,
      "spacing": "sm",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "GO !",
            "uri": "%s"
          },
          "height": "sm",
          "style": "primary"
        },
        {
          "type": "spacer",
          "size": "sm"
        }
      ]
    }
  }
    """ % (liff_url, liff_url)
    
    return bubble


""" 給予用戶 位置推薦的 Bubble """


def location_bubble(liff_url):
    if type(liff_url) != str:
        raise ValueError('liff url should be string')

    bubble = """{
"type": "bubble",
    "direction": "ltr",
    "hero": {
      "type": "image",
      "url": "https://lh5.ggpht.com/EniMdvCZXqsBor5qAkyTcTM_pByvNtCmv4HSrKXoA-EglnaKNFRhjzxuzTpsb08u4CI",
      "flex": 0,
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "fit",
      "backgroundColor": "#E3B0A1",
      "action": {
        "type": "uri",
        "label": "Line",
        "uri": "%s"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "位置推薦",
          "flex": 2,
          "size": "xl",
          "align": "center",
          "weight": "bold",
          "color": "#6A2727"
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "需耗費一些時間 (5 - 10秒)",
              "flex": 0,
              "align": "center",
              "weight": "bold"
            },
            {
              "type": "text",
              "text": "請耐心等候傳送喔 ",
              "align": "center",
              "color": "#EA7171"
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "flex": 0,
      "spacing": "sm",
      "contents": [
        {
          "type": "spacer"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "GO !",
            "uri": "%s"
          },
          "flex": 6,
          "color": "#176DE7",
          "height": "md",
          "style": "primary"
        }
      ]
    }


}""" % (liff_url, liff_url)
    
    return bubble


""" 計算用戶地理位置 之簡單函式 """


def count_gps(lat, lon, distance=0.7):
    # KM
    lat_diff = distance / 110.574
    lon_distance = 111.320 * cos(radians(lat) * pi / 180)
    lon_diff = distance / lon_distance
    
    n = lat + abs(lat_diff)
    s = lat - abs(lat_diff)
    e = lon + abs(lon_diff)
    w = lon - abs(lon_diff)
    return (lat, e), (s, lon), (lat, w), (n, lon), (lat, e)


""" 產生 Bubble 中 星星數量的函式 """


def get_rate_string(rate):
    covert = int(rate)
    srate = str(covert)

    rate_dict = {
        "1": "{0},{1},{1},{1},{1}".format(get_gold_string(), get_grey_string()),
        "2": "{0},{0},{1},{1},{1}".format(get_gold_string(), get_grey_string()),
        "3": "{0},{0},{0},{1},{1}".format(get_gold_string(), get_grey_string()),
        "4": "{0},{0},{0},{0},{1}".format(get_gold_string(), get_grey_string()),
        "5": "{0},{0},{0},{0},{0}".format(get_gold_string())
    }
    return rate_dict.get(srate)


""" 產生 Bubble 中 金色星星數量的工具 """


def get_gold_string():
    string = """
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
              "size": "sm"
            }"""
    return string


""" 產生 Bubble 中 灰色星星數量的工具 """


def get_grey_string():
    string = """
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
              "size": "sm"
            }"""
    return string


""" 產生推薦餐廳的 Bubble 傳入mysqlclient fetchall 結果 """


def gen_bubble(*tup, server_url):
    name, rate, address, optime, phone, image = list(*tup)
    # for a, b, c, d, e in tup:
    #     name = a
    #     rate = b
    #     address = c.replace("\r", "")
    #     optime = d
    #     phone = e
    address = address.replace("\r", "").replace("\n", "")
    optime = optime.replace("\t", "").replace("\r", "")
    getrate = get_rate_string(rate)
    if phone == "Not Available":
        phone = "Sorry"
    main_page = "https://" + server_url + "/index/resid=" + phone
    if image is None:
        image = "https://3dmart.com.tw/upload/news/2015/0924/123.jpg"
    
    bubble = """
{
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "%s",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Line",
        "uri": "%s"
      }
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "%s",
          "size": "xl",
          "weight": "bold"
        },
        {
          "type": "box",
          "layout": "baseline",
          "margin": "md",
          "contents": [
            %s,
            {
              "type": "text",
              "text": "%s",
              "flex": 0,
              "margin": "md",
              "size": "sm",
              "color": "#999999"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "margin": "lg",
          "contents": [
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "Place",
                  "flex": 1,
                  "size": "sm",
                  "color": "#AAAAAA"
                },
                {
                  "type": "text",
                  "text": "%s",
                  "flex": 5,
                  "size": "sm",
                  "color": "#666666",
                  "wrap": true
                }
              ]
            },
            {
              "type": "box",
              "layout": "baseline",
              "spacing": "sm",
              "contents": [
                {
                  "type": "text",
                  "text": "Time",
                  "flex": 1,
                  "size": "sm",
                  "color": "#AAAAAA"
                },
                {
                  "type": "text",
                  "text": "%s",
                  "flex": 5,
                  "size": "sm",
                  "color": "#666666",
                  "wrap": true
                }
              ]
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "flex": 0,
      "spacing": "sm",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "CALL",
            "uri": "tel://%s"
          },
          "height": "sm",
          "style": "link"
        },
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "WEBSITE",
            "uri": "%s"
          },
          "height": "sm",
          "style": "link"
        },
        {
          "type": "spacer",
          "size": "sm"
        }
      ]
    }
  }
""" % (image, image, name, getrate, rate, address, optime, phone, main_page)

    return bubble


""" 將產生的 Bubble 裝進 Flex """


def gen_flex(*bubble):

    bubble_string = ",".join(*bubble)
    flex = """
    {
    "type": "carousel",
    "contents": [%s]
    }
    """ % bubble_string

    return flex
    

""" 判斷今天星期幾的簡單工具 """


def get_days():
    tp = pytz.timezone("Asia/Taipei")
    now = datetime.datetime.now(tz=tp)
    return now.strftime("%A")


if __name__ == "__main__":
    pass
