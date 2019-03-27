import statistics
import random

"""
餐廳主頁的 html
傳入 MongoDB 查詢結果

"""


# fetch 包成list 傳入
def res_html(fetchall, image_url):
    # sample fetchall
    if type(fetchall) != list:
        fetchall = list(fetchall)
    else:
        pass

    if not fetchall:
        sorryhtml = "<div><img src='https://3dmart.com.tw/upload/news/2015/0924/123.jpg'>抱歉，資料缺失了</div>"
        return sorryhtml

    rate = statistics.mean(list(map(lambda x: x.get("rate"), fetchall)))
    if len(fetchall) > 4:
        fetchall = random.sample(fetchall, 4)
    else:
        pass
    # {0} Name {1} phone {2} address {3} rate
    res_info = [
        list(map(lambda x: x.get("name"), fetchall))[0],
        list(map(lambda x: x.get("phone"), fetchall))[0],
        list(map(lambda x: x.get("address"), fetchall))[0],
        rate,
        image_url
    ]
    html = """
    <!DOCTYPE html>
<html>
<head>
	<meta charset='utf-8'>
	<meta name='viewport' content='width=device-width'>
	<title>{0}</title>
	<!-- Latest compiled and minified CSS -->
	<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<link rel='stylesheet' href='/Images/Style-Main_v2.css'>
  <link rel="stylesheet" href='https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css'>
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick-theme.min.css'>
	<!-- jQuery library -->
	<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'>
	</script>
</head>
<body class='body'>
	<div>
    <div id="floating-panel">
      <b>Mode of Travel: </b>
      <select id="mode">
        <option value="DRIVING">Driving</option>
        <option value="WALKING">Walking</option>
        <option value="BICYCLING">Bicycling</option>
        <option value="TRANSIT">Transit</option>
      </select>
      <button class='button' onclick='navigateMe()'> 導航GO</button>
    </div>
    <div id='navigate' style="color: red; text-align: center;"></div>
	<!-- Put Map here -->
	<div>
		<div id="map"></div>
	</div>

	<div class="responsive">

    <p style="font-size:18px;font-weight:bold;"> 餐廳名稱：</p>
    <p style="font-size:16px;font-weight:bold;"> {0} </p>
    <p style='font-size:16px;font-weight:bold;'>
       電話：
       <a href="tel:{1}">{1}</a>
       </p>
    <p style='font-size:14px;font-weight:bold;'> 地址：
      {2}</p>
    <p style='font-size:16px;font-weight:bold;'> 評分：{3}</p>


  </div>
  <div class="responsive">
      <img src="{4}" style='width:auto;height:100px;'>
  </div>
  <!--  可愛分隔線  -->
  <hr size='8px' width='100%'>
  <div style="font-size:22px;font-weight:bold;">
    食記：
    <br>
    """.format(*res_info)

    def get_article(x):
        # dict object
        # result = [title, href, img , trk1, trk2, trk3]
        prepare_img = {
            "m1": "https://attach2.mobile01.com/images/mobile01-facebook.jpg",
            "ifood": "https://img.3cpjs.com/2014/2ed_half/%E5%B0%81%E9%9D%A21.png",
            "ipeen": "/Images/ipeen.png",
            "ptt": "/Images/ptt.jpg"
        }
        result = []
        href = x.get("href")
        sentence = x.get("textrank")# list object
        if sentence:
            sentence = sentence[0:2]
        title = x.get("title")[0:12]
        result.append(title)
        result.append(href)
        if href.find("mobile01") != -1:
            result.append(prepare_img.get("m1"))
        elif href.find("ifoodtw") != -1:
            result.append(prepare_img.get("ifood"))
        elif href.find("ptt") != -1:
            result.append(prepare_img.get("ptt"))
        else:
            result.append(prepare_img.get("ipeen"))
        for every_sentence in sentence:
            result.append(every_sentence)

        return result

    article = list(map(get_article, fetchall))

    def gen_textrank(all_article):

        # list article
        # article = [title, href, img , trk1, trk2, trk3]
        textrank_html = """
        <div>
          <p style='font-size:16px;'>{0}.....</p>
          <a target="_blank" href='{1}'>
            <img class='comment' src='{2}'>
          </a>
          <p style='font-size:16px;'>摘要:</p>       
          <p class='textrank'>1. {3}</p>
        </div>
      """.format(*all_article)

        return textrank_html

    # textrank 摘要 部分
    html += " ".join(list(map(gen_textrank, article)))

    # 圖片部分
    # img_list = [img0,.....img9].__len__() = 10
    def extract_imgs(fetchall_obj):
        imgs_list = []
        if fetchall_obj.get("img"):
            for every_img in fetchall_obj.get("img"):
                imgs_list.append(every_img)

        return imgs_list

    sample = []
    for img_list in map(extract_imgs, fetchall):
        for img in img_list:
            sample.append(img)
    if len(sample) > 10:
        sample = random.sample(sample, 10)
    else:
        pass

    # <img src="{0}">
    if sample:
        html += """     
      </div>
      <div style="font-size:22px;font-weight:bold;">
        圖片：
        <br>
        <div class='slick'>
            {0}          
        """.format("\n\t\t".join(map(lambda x: """<img src="{0}">""".format(x), sample)))

    # 相似推薦部分
    html += """
    </div>
  </div>
  <div style="font-size:22px;font-weight:bold;">
    為你推薦：
    <div class='slick'>
      <a target="_blank" href=''>
        Name
        <img class='recommand'
         src='https://attach.mobile01.com/attach/201508/thumbnail_720_1707260_7d21a0b5be801ea22a72138a8b732588.jpg'>
      </a>
      <a target="_blank" href=''>
        Name
        <img class='recommand'
         src='https://attach.mobile01.com/attach/201508/thumbnail_720_2632917_c82e91d714b91b1fcdcce1aa53f39e00.jpg'>
      </a>
      <a target="_blank" href=''>
        Name
        <img class='recommand'
         src='https://attach.mobile01.com/attach/201508/thumbnail_720_2632917_553c830ac70d41606585d7a490131c7e.jpg'>
      </a>
    </div>
  </div>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.7.1/slick.min.js"></script>
<script type="text/javascript" 
src="https://cdnjs.cloudflare.com/ajax/libs/danielgindi-jquery-backstretch/2.1.15/jquery.backstretch.min.js"></script>
</body>
"""

    # Script
    # location = [lat,lng]
    # escape format {} use {{ some script }}
    # JavaScript Main
    postion_x = list(set(map(lambda x: x.get("lat"), fetchall)))
    postion_y = list(set(map(lambda x: x.get("lon"), fetchall)))
    if postion_x and postion_y:
        if None not in postion_x:
            postion_x = postion_x[0]
            postion_y = postion_y[0]
        else:
            postion_x = 25.046891
            postion_y = 121.516602

    html += """
        <script>
        var shop_lat = {0}
        var shop_lng = {1}
        """.format(postion_x, postion_y)

    html += """
      // slick 幻燈片秀  
      $(document).ready(function() {    
        $(".slick").slick({
          dots: true,
          infinite: true,
          speed: 300,
          slideToShow: 1,
          autoplay: true,
          autoplaySpeed: 4000,
          fade: true,
          cssEase: 'linear',
          mobileFirst: true,
        });
        $(document.body).backstretch("/Images/anime2.gif");
        console.log("ready");
      });  

      function error(err) {
        console.log(err);
      };
      var directService;
      var directDisplay;
      var mylat;
      var mylng;
      var map;
      var mode = document.getElementById('mode').value

      function navigateMe() {   
        var markers=[];
        var infowindows=[];    
        // 設置請求 起點 終點 型態
        var request = {
          origin: {lat: mylat, lng: mylng},
          destination: {lat: 25.046891, lng: 121.516602},
          travelMode: mode
        };
        if (! mylat) {
          document.getElementById("navigate").innerHTML='Sorry Try Again and turn on your GPS';
        };

        // 繪製路線
        directService.route(request, function(result, status) {
          if (status == "OK") {        
            directDisplay.setDirections(result);
            // 設定路線細節
            var steps = result.routes[0].legs[0].steps;
            steps.forEach((e,i) => {
              // set marker
              markers[i] = new google.maps.Marker({
                position: {lat: e.start_location.lat(),lng: e.start_location.lng() },
                map: map,
                label: { text: i + '', color: '#fff'}
              });
              // set infowindow
              infowindows[i] = new google.maps.InfoWindow({
                content: e.instructions
              });

              // 點擊 marker 事件
              markers[i].addListener('click', function() {
                if (infowindows[i].anchor) {
                  //anchor 存在時 將其關閉
                  infowindows[i].close();
                } else {
                  //anchor 不存在 將其打開
                  infowindows[i].open(map, markers[i]);
                }
              });          
            })
          } else {
            console.log(status);        
          }
        })
      };

      function initMap() {    
        var Station_latlng = { lat: shop_lat, lng: shop_lng };
        // Direction API
        directService = new google.maps.DirectionsService();
        directDisplay = new google.maps.DirectionsRenderer();    
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: Station_latlng,
          mapTypeControl: true,
          mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
          },
          streetViewControl: false,
        });
        directDisplay.setMap(map);

        var marker = new google.maps.Marker({
          position: Station_latlng,
          map: map,
          label: {text:"C", color: "#fff"}
        });
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(pos) {
            mylat = pos.coords.latitude;
            mylng = pos.coords.longitude;
          }, error);
        } else {
          console.log("Can't use")
        };  

        $.ajax({
          type: "POST",
          url: "/countRes",
          data: JSON.stringify({'resID': 1}),
          dataType: 'json',
          success: function(response) {
            console.log(response);
          },
          error: function(err) {
            console.log(err);
          },
        });
      }
    </script>
    <script 
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCz9gOS87ThpLl0clXSto5gEYwnVjZEy6Y&callback=initMap" async defer>
    </script>


    </html>"""

    return html


if __name__ == "__main__":
    pass
