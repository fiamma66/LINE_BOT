import pytz
import datetime
from math import radians, cos, pi


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


def count_gps(lat, lon, distance=0.7):
    # KM
    lat_diff = distance / 110.574
    lon_distance = 111.320 * cos(radians(lat) * pi / 180)
    lon_diff = distance / lon_distance
    
    n = lat + abs(lat_diff)
    s = lat - abs(lat_diff)
    e = lon + abs(lon_diff)
    w = lon - abs(lon_diff)
    return (lat, n), (s, lon), (lat, w), (n, lon), (lat, e)


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


def get_gold_string():
    string = """
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
              "size": "sm"
            }"""
    return string


def get_grey_string():
    string = """
            {
              "type": "icon",
              "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png",
              "size": "sm"
            }"""
    return string


def gen_bubble(*tup):
    name, rate, address, optime, phone = ("", "", "", "", "")
    for a, b, c, d, e in tup:
        name = a
        rate = b
        address = c.replace("\r", "")
        optime = d
        phone = e
    
    getrate = get_rate_string(rate)
    
    bubble = """
{
    "type": "bubble",
    "hero": {
      "type": "image",
      "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Line",
        "uri": "https://linecorp.com/"
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
            "uri": "https://linecorp.com"
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
""" % (name, getrate, rate, address, optime, phone)

    return bubble


def gen_flex(*bubble):

    bubble_string = ",".join(*bubble)
    flex = """
    {
    "type": "carousel",
    "contents": [%s]
    }
    """ % bubble_string

    return flex
    

def get_days():
    tp = pytz.timezone("Asia/Taipei")
    now = datetime.datetime.now(tz=tp)
    return now.strftime("%A")


if __name__ == "__main__":
    pass
