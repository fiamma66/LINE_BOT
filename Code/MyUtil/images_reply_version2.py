"""
給予用戶點選圖片的 html
主要使用 JQuery 完成圖片點選

"""


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
	<link rel='stylesheet' href='Images/style-graph.css'>

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

				<img class="myImg" src='/Images/movie.jpg' alt='Cat01' height='150' data-brand='影音藝文'>

      </div>
    </div>
<!--第二個圖片放這邊    -->
    <div class='responsive'>
      <div class='gallery'>

      <img class="myImg" src='/Images/3c.jpg' alt='Cat02' height='150' data-brand='3C商品''>

      </div>
    </div>
<!--第三個圖片放這邊    -->    
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='/Images/travel.jpg' alt='Cat01' height='150' data-brand='休閒旅遊'>

      </div>
    </div>

<!--第四個圖片放這邊    -->
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='/Images/service.PNG' alt='Cat01' height='150' data-brand='生活服務''>

      </div>
    </div>

<!--第五個圖片放這邊    -->
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='/Images/food.jpg' alt='Cat01' height='150' data-brand='美食'>

      </div>
    </div>
<!--第六個圖片放這邊    -->
    <div class='responsive'>
			<div class='gallery'>

				<img class="myImg" src='/Images/beauti.jpg' alt='Cat01' height='150' data-brand='美容美妝'>

      </div>
    </div>

  <br> 
  <br>   
  <br> 
  <br> 
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
    "/Images/beauti.jpg",
    "/Images/food.jpg",
    "/Images/service.PNG",
    "/Images/travel.jpg",
    "/Images/3c.jpg",
    "/Images/movie.jpg"
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
  var output = {
    "美食": 0,
    "影音藝文": 0,
    "3C商品": 0,
    "休閒旅遊": 0,
    "美容美妝": 0,
    "生活服務":0
  };
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
          output[imgcc.getAttribute("data-brand")] = 1;
          imgcs.addClass("galleryOnClick");
          console.log(output);
          $('.button').removeClass("disabled");

        } else {
          // 點過一次 重置點擊次數 並刪除元素資料
          output[imgcc.getAttribute("data-brand")] = 0;
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
  var imageMap = document.getElementById("imageMap");
  $('.button').click(function() {
    $.ajax({
      type: "POST",
      url: "/post_graph",

      data: JSON.stringify({graph: output, user:secret}),
    });
    imageMap.innerHTML = "<div style='text-align:center'><h1 style='color:#1E90FF'>收到回覆後就可以關閉了</h1></div>"
  });


</script>


</body>

</html>


    """ % title

    return html
