var gRealTimeView = window.gRealTimeView = {

    "TemplateView": 
function (){
var view_ctx = $("#device_view");
var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "RealTime IOT",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: [65, 59, 80, 81, 56, 55, 40],
            spanGaps: false,
        }
    ]
};
var myLineChart = Chart.Line(view_ctx, {
    data: data,
});
//myLineChart.data.datasets[0].data[2] = 50; // Would update the first dataset's value of 'March' to be 50
//myLineChart.update(); // Calling update now animates the position of March from 90 to 50.

// websocket
var wbsocket = new WebSocket(gWbSocketUrl);
//var wbsocket = new WebSocket("ws://120.76.52.151:8888/ws_socket");
wbsocket.onopen = function (event) {
  wbsocket.send('hello');
};

wbsocket.onmessage = function (event) {
  console.log(event.data);
  data.datasets[0].data.shift();
  data.datasets[0].data.push(event.data);
  data.labels.shift();
  data.labels.push(Date());
  myLineChart.update();
};

wbsocket.onerror = function(){
  console.log('wbsocket error')
};        
    },
    "VideoMpgView": function () {
    // Setup the WebSocket connection and start the player
    var wbsocket = new WebSocket("ws://120.76.52.151:8880/ws_socket");
    //var canvas = $("#device_view");
    var canvas = document.getElementById('device_view');
    var player = new jsmpeg(wbsocket, {canvas:canvas});
},

    "AudioView": function () {
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    var context = new AudioContext();

    function playSound(buffer) {
        var source = context.createBufferSource(); // creates a sound source
        source.buffer = buffer;                    // tell the source which sound to play
        source.connect(context.destination);       // connect the source to the context's destination (the speakers)
        source.start(0);                           // play the source now
                                             // note: on older systems, may have to use deprecated noteOn(time);
    };
    
    var wbsocket = new WebSocket(gWbSocketUrl);
    wbsocket.onopen = function (event) {
        // do nothing
    };
    
    wbsocket.onmessage = function (event) {
        playSound(event.data);
    };
    
    wbsocket.onerror = function () {
        console.log('wbsocket error')
    };
},
    
    "ImgView": function () {
     var ctxt = $('#device_view').getContext('2d');
     
     function drawit(base64Image) {
        var img = new Image();
        img.onload = function () {
            context.drawImage(img, 0, 0);
        }
        // todo need to parse image types
        img.src = "data:image/png;base64," + base64Image;
     };
    
    var wbsocket = new WebSocket(gWbSocketUrl);
    wbsocket.onopen = function (event) {
        // do nothing
    };
    
    wbsocket.onmessage = function (event) {
        drawit(event.data);
    };
    
    wbsocket.onerror = function () {
        console.log('wbsocket error')
    };

},

    "VideoLiveView": function () {
    if (flvjs.isSupported()) {
        
        var videoElement = $('#video_live');
        var flvPlayer = flvjs.createPlayer({
            type: 'flv',
            isLive: true,
            url: gWbSocketUrl,
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
        flvPlayer.play();
    }
},
    "DevMappView": function () {
    var map = new AMap.Map('dev_mapp_view', {
        resizeEnable: true,
        zoom:11,
        center: gDevLocation
    });
    map.plugin(["AMap.ToolBar"], function() {
         map.addControl(new AMap.ToolBar());
    });
    map.plugin(["AMap.Geocoder"], function() {
        map.addControl(new AMap.Geocoder());
    });

    var marker = new AMap.Marker({
        position: gDevLocation,
        title: "test-ll"
    });
    marker.setMap(map);

    var pathArray = [gDevLocation];
    var oldArray = pathArray.slice(0)
    var polyline = new AMap.Polyline({
        path: pathArray,
        strokeColor: "#3366FF",
        strokeOpacity: 1,    
        strokeWeight: 5, 
        strokeStyle: "solid",
        strokeDasharray: [10, 5]
    });
    polyline.setMap(map);
    polyline.setPath(pathArray);

    function drawPath(point, title) {
        var marker = new AMap.Marker({
            position: point,
            title: title
        });
        marker.setMap(map);

        //oldArray.push(point);
        pathArray = polyline.getPath();
        pathArray.push(point)
        console.log(pathArray);
        polyline.setPath(pathArray);
        polyline.setMap(map);
    };
    var geocoder = new AMap.Geocoder({city: '010'});
    var wbsocket = new WebSocket(gWbSocketUrl);
    wbsocket.onopen = function (event) {
        // do nothing
    };
    
    wbsocket.onmessage = function (event) {
        console.log(typeof(event.data))
        var data = JSON.parse(event.data)
        //逆地理编码
    function cover_to_gaode_xy(lnglatXY) {
        geocoder.getAddress(lnglatXY, function(status, result) {
            if (status === 'complete' && result.info === 'OK') {
                //获得了有效的地址信息:
                address = result.regeocode.formattedAddress
                //即，result.regeocode.formattedAddress
            }else{
                console.log(status)
                console.log(result)
                //获取地址失败
                console.log('get address failed')
                address = ''
            }
            drawPath(lnglatXY, address);
        });
    }
        // conver
        params = {key:'06312eff529473eeb9716f301b0cd29a',locations:data.join(","), coordsys: 'gps'}
        $.getJSON('http://restapi.amap.com/v3/assistant/coordinate/convert', params,
        function(ret) {
            if(ret['status']) {
                cover_to_gaode_xy(ret['locations'].split(','));
            } else {
                console.log('getJson fail')
            }
        });
        //lnglat = AMap.LngLat(data[0],data[1]);
        //AMap.convertFrom(lnglat,'gps', function(stat, ret) {
          //  console.log(stat);
            //console.log(ret);
            //cover_to_gaode_xy([ret[0].getLng(), ret[0].getLat()]);
        //});
    };
    
    wbsocket.onerror = function () {
        console.log('wbsocket error')
    };

},
    "DoNothing" : function () {},

}
