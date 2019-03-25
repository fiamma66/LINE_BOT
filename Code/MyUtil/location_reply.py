""" 取得用戶位置資訊的 HTML
使用 Geolocation API
1. getCurrentPosition
2. watchPosition
傳遞Json 回到 Flask 接口
1. JQuery Ajax

"""


def location_html(userid):
    userid = str(userid)
    html = """
    <!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
	<meta name="viewport" content="width=device-width">
	<title>GeoLocation</title>

	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

	<style>
    #mymap {
      width: 90%%;
      height: 300px;
      margin: auto;
    }
	</style>

	<!-- jQuery library -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js">

	</script>

	<!-- Latest compiled JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">

	</script>

</head>



<body>
	<!--註解 (固定格式)  -->

  
	<!-- <div class="col-md-6 col-md-offset-3">
		<button id="geo" type="submit" class="btn btn-primary btn-lg btn-block">Submit my Position</button>

    

  </div> -->
  <div> </div>
  <div id="mymap"></div>
  <br> 

  <div style="text-align:center" id="location"> 
    <h1 id="ajax" style='color:#1E90FF'>
      Here are your location


    </h1>


  </div>
  
  


<script>
  var map,
      currentPositionMarker,
      mapcenter = {lat:25.047761, lng:121.516934};
  var output = [];
  var watchID;
  
  // initMap
  function initMap() {
    map = new google.maps.Map(document.getElementById("mymap"),{
      zoom: 15,
      center: mapcenter,
      mapTypeControl: true,
      mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
      },
      streetViewControl: false,
      
      });
  }

  // handlError
  function handlError() {
    document.getElementById("ajax").innerHTML = "無法收到ＧＰＳ ！";
  }

  // set current position
  function setCurrentPosition(pos) {
    var lat = pos.coords.latitude;
    var lon = pos.coords.longitude;
    currentPositionMarker = new google.maps.Marker({
      map: map,
      position: {
        lat: lat,
        lng: lon
      },
      title: "Current Position"
    });
    // move map view to current position
    map.panTo({
      lat: lat,
      lng: lon
    });
    document.getElementById("ajax").innerHTML = '<p>Latitude is ' + lat + '° <br>Longitude is ' + lon + '°</p>';
  }



  // displayMapWatch
  function displayMapWatch(position) {
    // set current position and move the map
    setCurrentPosition(position);

    // use watch position Here
    watchCurrentPosition();

  }
  
  function watchCurrentPosition() {
    watchID = navigator.geolocation.watchPosition(
      function (position) {
        setMarkerPosition(
          currentPositionMarker,
          position
        );
      },handlError,
      {enableHighAccuracy: true}
    );
    
  }

  // get watch position and set new Marker
  function setMarkerPosition(marker, position) {
    marker.setPosition({
      lat: position.coords.latitude,
      lng: position.coords.longitude
      
    });
    map.panTo({
      lat: position.coords.latitude,
      lng: position.coords.longitude
    });
    
    output.push({
      lat: position.coords.latitude,
      lng: position.coords.longitude
    });
    
    document.getElementById("ajax").innerHTML = '<p>Latitude is ' + position.coords.latitude + '° <br>Longitude is ' + position.coords.longitude + '°</p>';
    if (output.length >= 4) {
      navigator.geolocation.clearWatch(watchID);
      document.getElementById('ajax').innerHTML = '收到回覆就可以關閉了';
      $.ajax({
        type: "POST",
        url: "/post_location",
        data: JSON.stringify({location: output, user:"%s"}),
      });
    }
    
  }

  function iniGeoLocation() {
    initMap()
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(displayMapWatch, handlError);
    } else {
      // 無法使用 geolocation
      document.getElementById("ajax").innerHTML = "Sorry ! Your brower can't use location API."
    }
  };


  

  

</script>
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCz9gOS87ThpLl0clXSto5gEYwnVjZEy6Y&callback=iniGeoLocation"></script>


</body>

</html>
    
    """ % userid

    return html
