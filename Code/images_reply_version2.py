import json

def get_image_reply_html(title):
    title = str(title)
    html = """    
    <!DOCTYPE html>
<html>

<head>
	<meta charset='utf-8'>
	<meta name='viewport' content='width=device-width'>
	<title>Submit Graph</title>

	<!-- Latest compiled and minified CSS -->
	<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<link rel='stylesheet' href='Images/style.css'>

	<!-- jQuery library -->
	<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'>

	</script>

	<!-- Latest compiled JavaScript -->
	<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'>

	</script>
</head>



<body>
  
  
	<!--註解 (固定格式)  -->
	<div style='text-align:center'>
		<p style="font-size:24px">
			請以第一印象選擇
		</p>
		<p style="font-size:14px" id="test">
			雙擊可放大顯示
		</p>
	</div>
	<!--    put modal here    -->
	<div id="myModal" class="modal">
		<span class="close">×</span>
    <img class="modal-content" id="img01">
    <div id="caption"></div>
  </div>

	
	<div id='imageMap' class="w3-animate-opacity">
		<!--第一個圖片放這邊    -->
		
    <div class='responsive'>
			<div class='gallery'>
        
				<img class="myImg" src='https://www.goodmorninggif.com/wp-content/uploads/2018/05/Beautiful-Nature-Good-Morning-Images.jpg' alt='Cat01' width='600' height='400' data-brand='夕陽'>
        
      </div>
    </div>
<!--第二個圖片放這邊    -->
    <div class='responsive'>
      <div class='gallery'>
      
      <img class="myImg" src='https://www.w3schools.com/w3css/img_lights.jpg' alt='Cat02' width='600' height='400' data-brand='極光''>
       
      </div>
    </div>
<!--第三個圖片放這邊    -->    
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='https://www.w3schools.com/howto/img_forest.jpg' alt='Cat01' width='600' height='400' data-brand='橋'>
       
      </div>
    </div>

<!--第四個圖片放這邊    -->
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='https://www.w3schools.com/howto/img_mountains.jpg' alt='Cat01' width='600' height='400' data-brand='山水''>
       
      </div>
    </div>

<!--第五個圖片放這邊    -->
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='https://www.w3schools.com/howto/img_snow.jpg' alt='Cat01' width='600' height='400' data-brand='冰河'>
       
      </div>
    </div>
<!--第六個圖片放這邊    -->
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='https://global.canon/en/imaging/eosd/samples/eos1300d/img/sp/image_thumb_01.jpg' alt='Cat01' width='600' height='400' data-brand='Paris'>
       
      </div>
    </div>
	
  <br> 



  <div>
    <button class="button disabled"> Next Page </button>
  </div>


<!--images map    -->
  </div>
  
  <br>

<script>
  // use jquery to get images
  // define prepared list
  // change here to get our new images and data tags
  


  var prepared_list = [
    // first element
    "<!--第一個圖片放這邊    -->		<div class='responsive'> 			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='http://www.bigfoto.com/stones-background.jpg' alt='stone1' width='600' height='400' data-brand='石頭'>      </div>    </div><!--第二個圖片放這邊    -->    <div class='responsive'>      <div class='gallery w3-animate-opacity'>      <img class='myImg' src='http://www.wearedesignteam.com/design/images/free-images-of-travel.jpg' alt='night' width='600' height='400' data-brand='晚霞''>      </div>    </div><!--第三個圖片放這邊    -->       <div class='responsive'> <div class='gallery w3-animate-opacity'>				<img class='myImg' src='https://www.sony.net/Products/di_photo-gallery/images/extralarge/1229.jpg' alt='Cat02' width='600' height='400' data-brand='山貓'>      </div>    </div><!--第四個圖片放這邊    -->    <div class='responsive'>			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='http://www.bigfoto.com/lines-image.jpg' alt='structure' width='600' height='400' data-brand='抽象''>       </div>    </div><!--第五個圖片放這邊    -->    <div class='responsive'>			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='https://www.imagesfromcolorado.com/images/xl/Meadow-Creek-Reservoir-1.jpg' alt='water' width='600' height='400' data-brand='倒影'>      </div>    </div><!--第六個圖片放這邊    -->    <div class='responsive'>			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='http://2.bp.blogspot.com/-5cJ7kzLilvo/U2fsRlOR6kI/AAAAAAAACMM/jsN7mAjKQm8/s1600/holding+hand+friend+love+close++(21).jpg' alt='couple' width='600' height='400' data-brand='情侶'>       </div>    </div>  <br>   <div>    <button class='button'> Next Page </button>  </div>",
    // second element
    "<!--第一個圖片放這邊    -->		<div class='responsive'> 			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='https://images.redframe.com/64026/1000/Image%%202%%20-%%20Caba%%20Perfection.jpg' alt='beach' width='600' height='400' data-brand='海灘'>      </div>    </div><!--第二個圖片放這邊    -->    <div class='responsive'>      <div class='gallery w3-animate-opacity'>      <img class='myImg' src='https://cdn.zekkei-japan.jp/images/articles/fbd48098c0c2dd575d819ff12d93e578.jpg' alt='文具' width='600' height='400' data-brand='文具''>      </div>    </div><!--第三個圖片放這邊    -->       <div class='responsive'> <div class='gallery w3-animate-opacity'>				<img class='myImg' src='http://shopsimage.com/wp-content/uploads/2018/06/26-11781-post/810%%E5%%A9%%9A%%E7%%B4%%97%%E6%%94%%9D%%E5%%BD%%B1-%%E5%%A9%%9A%%E7%%B4%%97%%E7%%85%%A7-%%E5%%8C%%97%%E6%%B5%%B7%%E5%%B2%%B8-%%E6%%B5%%B7%%E9%%82%%8A-%%E5%%A4%%95%%E9%%99%%BD(pp_w1200_h800).jpg' alt='photo01' width='600' height='400' data-brand='婚紗'>      </div>    </div><!--第四個圖片放這邊    -->    <div class='responsive'>			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='https://i2.wp.com/img.sainteat.tw/pixnet/56bff8373d08e0600618f7c9ee933e6b.jpg' alt='food' width='600' height='400' data-brand='美食''>       </div>    </div><!--第五個圖片放這邊    -->    <div class='responsive'>			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='https://watermark.lovepik.com/photo/50029/8274.jpg_wh1200.jpg' alt='資訊' width='600' height='400' data-brand='資訊'>      </div>    </div><!--第六個圖片放這邊    -->    <div class='responsive'>			<div class='gallery w3-animate-opacity'>				<img class='myImg' src='https://www.taiwanhot.net/wp-content/uploads/2018/11/5bfba50e4a699.jpg' alt='學術' width='600' height='400' data-brand='學術'>       </div>    </div>  <br>   <div>    <button class='button'> Next Page </button>  </div>"

    
  ]
  var secret = "%s"
  // get modal 
  var modal = document.getElementById("myModal");
  var images = new Array()
  function preload() {
    for (var i = 0; i < preload.arguments.length ; i++) {
      images[i] = new Image();
      images[i].src = preload.arguments[i];
    }
  }
  function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
      window.onload = func;
    } else {
      window.onload = function() {
        if (oldonload) {
          oldonload();
          
        }
        func();
      }
    }
  }
  
  // preload images
  addLoadEvent(preload(
    'https://www.goodmorninggif.com/wp-content/uploads/2018/05/Beautiful-Nature-Good-Morning-Images.jpg',
    'https://www.w3schools.com/w3css/img_lights.jpg',
    'https://www.w3schools.com/howto/img_forest.jpg',
    'https://www.w3schools.com/howto/img_mountains.jpg',
    'https://www.w3schools.com/howto/img_snow.jpg',
    'https://global.canon/en/imaging/eosd/samples/eos1300d/img/sp/image_thumb_01.jpg',
    'http://www.bigfoto.com/stones-background.jpg',
    'http://www.wearedesignteam.com/design/images/free-images-of-travel.jpg',
    'https://www.sony.net/Products/di_photo-gallery/images/extralarge/1229.jpg',
    'http://www.bigfoto.com/lines-image.jpg',
    'https://www.imagesfromcolorado.com/images/xl/Meadow-Creek-Reservoir-1.jpg',
    'http://2.bp.blogspot.com/-5cJ7kzLilvo/U2fsRlOR6kI/AAAAAAAACMM/jsN7mAjKQm8/s1600/holding+hand+friend+love+close++(21).jpg',
    'https://images.redframe.com/64026/1000/Image%%202%%20-%%20Caba%%20Perfection.jpg',
    'https://cdn.zekkei-japan.jp/images/articles/fbd48098c0c2dd575d819ff12d93e578.jpg',
    'http://shopsimage.com/wp-content/uploads/2018/06/26-11781-post/810%%E5%%A9%%9A%%E7%%B4%%97%%E6%%94%%9D%%E5%%BD%%B1-%%E5%%A9%%9A%%E7%%B4%%97%%E7%%85%%A7-%%E5%%8C%%97%%E6%%B5%%B7%%E5%%B2%%B8-%%E6%%B5%%B7%%E9%%82%%8A-%%E5%%A4%%95%%E9%%99%%BD(pp_w1200_h800).jpg',
    'https://i2.wp.com/img.sainteat.tw/pixnet/56bff8373d08e0600618f7c9ee933e6b.jpg',
    'https://watermark.lovepik.com/photo/50029/8274.jpg_wh1200.jpg',
    'https://www.taiwanhot.net/wp-content/uploads/2018/11/5bfba50e4a699.jpg'

  ))

  // define remove element in array
  
  function arrayRemove(arr, value) {
   // filter 
   // Array.filter return elements not matching a value
   return arr.filter(function(ele){
       return ele != value;
   });

  }
  
  var modalImg = $('#img01');
  var captionText = document.getElementById("caption");
  var tapped = false;
  var output = [];
  // 將點擊圖片 等動作 裝成一個 function
  function dfclick(){
    $('.myImg').on("click", function(e) {
    if(!tapped) {
      //if tap is not set, set up single tap
      var imgcs = $(this);
      var imgcc = this;
      tapped = setTimeout(function(){
        tapped = null;
        // set up single click event
        if(imgcc.alt.search("-") == -1) {
          // 沒點過
          imgcc.alt = imgcc.alt + "-";
          output.push(imgcc.getAttribute("data-brand"));
          imgcs.addClass("galleryOnClick");
          console.log(output);
          $('.button').removeClass("disabled");
          
        } else {
          // 點過一次 重置點擊次數 並刪除元素資料
          output = arrayRemove(output,imgcc.getAttribute("data-brand"));
          imgcc.alt = imgcc.alt.substring(0,imgcc.alt.length-1);
          imgcs.removeClass("galleryOnClick");
          console.log(output);
          if(output.length == 0) {
            $('.button').addClass("disabled");
          }
        }
        
      },300); // wait 300ms then run single click code
    } else { //tapped within 300ms of last tap. double tap
      clearTimeout(tapped); //stop single tap callback
      tapped = null;
      // set up double click event
      modal.style.display = "block";
      var newSrc = this.src;
      modalImg.attr('src', newSrc);
      captionText.innerHTML = this.alt;
    }
    e.preventDefault();
    
  });
  }
  // define click image 
  // only on mobile device
  dfclick();
  // define click X
  var span = document.getElementsByClassName("close")[0];
  span.onclick = function() {
    modal.style.display = "none";
  };

  // define buttion click to change image 
  // and record data
  //第一頁
  var imageMap = document.getElementById("imageMap");
  $('.button').click(function() {
    // 第二頁
    imageMap.innerHTML = prepared_list[0];
    dfclick();
    $('.button').click(function(){
      // 第三頁
      imageMap.innerHTML = prepared_list[1];
      dfclick();
      $('.button').click(function(){
        // send to our server
        $.ajax({
          type: "POST",
          url: "/post_graph",
          
          data: JSON.stringify({graph: output, user:secret}),
        });
        imageMap.innerHTML = "<div style='text-align:center'><h1 style='color:#1E90FF'>收到回覆後就可以關閉了</h1></div>"
      })
    })
  })


  /*
  // send information to server
  $.ajax({
      type: "POST",
      url: "https://501cc88b.ngrok.io/post_graph",
      
      data: JSON.stringify({graph: output, user:title}),
    });

  */
 



</script>


</body>

</html>
    
    
    """ % title
    
    return html
    
    
    
    
    
    
    
    