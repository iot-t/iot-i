var gRealTimeView = {

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

//wbsocket.close();        
    },
    "VideoView": function () {
    // Setup the WebSocket connection and start the player
    var wbsocket = new WebSocket("ws://120.76.52.151:8880/ws_socket");
    //var canvas = $("#device_view");
    var canvas = document.getElementById('device_view');
    var player = new jsmpeg(wbsocket, {canvas:canvas});
},

    "DoNothing" : function () {},

}
