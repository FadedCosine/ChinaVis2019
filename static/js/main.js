var current_idx = 0;
var heatmap_data_point= Server.heatmap_data;
var up_order_data= Server.up_order;
var down_order_data= Server.down_order;
// var heatmap_data_point =  $(".docontent").html(heatmap_data);//{{ heatmap_data |tojson }}
// var up_order_data = $(".docontent").html(up_order);//{{up_order|tojson}}
// var down_order_data = $(".docontent").html(down_order);//{{down_order|tojson}}


var time_interval = 60 * 60;
var minDateUnix = 1525104000;
var maxDateUnix = 1525190400;
var heatmap_current_time = 0;
d3.select('#slider').call(d3.slider().scale(d3.time.scale()
    .domain([new Date(1525104000000), new Date(1525190399000)]))
    .axis(d3.svg.axis())
    .step(60*10)
    .on("slide", function(evt, value) {
        heatmap_current_time = value;
        var current_value = value / 1000;
        current_idx = parseInt((current_value - minDateUnix) / time_interval);
        console.log(current_idx);

        var interval_json = {
            data: JSON.stringify({
                'interval': current_idx,
            }),
        };
        $.ajax({
            url: "{{ url_for('data') }}",
            type: "POST",
            data: interval_json,
            dataType: 'json',
            success: function (data) {
                //成功后的一些操作

            },
            error: function (e) {

            }
        });
    })
);
function onclick_select() {
    $.post("/slider", {time:current_idx},
        function(data, status) {

            heatmap_data_point = data.heatmap_data;
            up_order_data = data.uporder_data;
            down_order_data = data.downorder_data;
            contour_layer.setData(heatmap_data_point, {
            lnglat: 'lnglat',
            value: 'count'
        });

        contour_layer.setOptions({
            smoothNumber: 3,
            threshold: 3,
            interpolation: {
                step: 300,
                effectRadius: 1000,
            },
            style: {
                height: 5 * 1E4,
                color: ["#3656CD", "#655FE7", '#20C2E1', '#23D561', '#9CD523', '#F1E229', '#FFBF3A', '#FB8C00', '#FF5252', "#BC54E2", "#FF6FCE"]
            }
        });
        contour_layer.render();


         heatmap_layer.setData(heatmap_data_point, {
            lnglat: 'lnglat',
            value: 'count'
        });
        heatmap_layer.render();

        });
    console.log(heatmap_data_point[0]);

    map.remove(down_order_layer);
    $("#downorder_btn").text("显示下车订单始末点");
    down_order_button_mode = 0;
    map.remove(up_order_layer);
    $("#uporder_btn").text("显示上车订单始末点");
    up_order_button_mode = 0;
    set_up_order(up_order_data);
    set_down_order(down_order_data);

}

var map = new AMap.Map('container', {
    //mapStyle: 'amap://styles/dark',
    viewMode: '3D',
   // features: ['bg', 'road'],
    center: [104.031944, 30.456944],
    resizeEnable: true,
    showIndoorMap: false,
    zoom:13,
    pitch: 60
});

var contour_layer = new Loca.ContourLayer({
    shape: 'isoline',
    map: map
});

contour_layer.setData(heatmap_data_point, {
    lnglat: 'lnglat',
    value: 'count'
});

contour_layer.setOptions({
    smoothNumber: 3,
    threshold: 3,
    interpolation: {
        step: 300,
        effectRadius: 1000,
    },
    style: {
        height: 5 * 1E4,
        color: ["#3656CD", "#655FE7", '#20C2E1', '#23D561', '#9CD523', '#F1E229', '#FFBF3A', '#FB8C00', '#FF5252', "#BC54E2", "#FF6FCE"]
    }
});

contour_layer.render();


var heatmap_layer = new Loca.HeatmapLayer({
map: map,
});

heatmap_layer.setData(heatmap_data_point, {
lnglat: 'lnglat',
value: 'count'
});

heatmap_layer.setOptions({
style: {
    radius: 30

}
});

heatmap_layer.render();

var up_order_layer, down_order_layer;
map.on('complete', function () {
set_up_order(up_order_data);

set_down_order(down_order_data);

});
function set_up_order(order_data)
{
 up_order_layer = new AMap.LabelsLayer({
    zooms: [3, 20],
    zIndex: 1000,
    // 关闭标注避让，默认为开启，v1.4.15 新增属性
    animation: false,
    // 关闭标注淡入动画，默认为开启，v1.4.15 新增属性
    collision: false
});

// 将图层添加到地图


var markers = [];
var positions = order_data;
var up_icon = {
    type: 'image',
    image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
    size: [10, 15],
    anchor: 'bottom-center',
    angel: 0,
    retina: true
};
var down_icon = {
    type: 'image',
    image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
    size: [10, 15],
    anchor: 'bottom-center',
    angel: 0,
    retina: true
};
for (var i = 0; i < positions.length; i++) {
    var up_Position = positions[i][0];
    var up_Data = {
        position: up_Position,
        icon: up_icon
    };
    var down_Position = positions[i][1];
    var down_Data = {
        position: down_Position,
        icon: down_icon
    };
    var up_label_marker = new AMap.LabelMarker(up_Data);
    var down_label_marker = new AMap.LabelMarker(down_Data);

    markers.push(up_label_marker);
    markers.push(down_label_marker);
}

// 一次性将海量点添加到图层
up_order_layer.add(markers);
}
function set_down_order(order_data)
{
 down_order_layer = new AMap.LabelsLayer({
    zooms: [3, 20],
    zIndex: 1000,
    // 关闭标注避让，默认为开启，v1.4.15 新增属性
    animation: false,
    // 关闭标注淡入动画，默认为开启，v1.4.15 新增属性
    collision: false
});

// 将图层添加到地图


var markers = [];
var positions = order_data;
var up_icon = {
    type: 'image',
    image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
    size: [10, 15],
    anchor: 'bottom-center',
    angel: 0,
    retina: true
};
var down_icon = {
    type: 'image',
    image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png',
    size: [10, 15],
    anchor: 'bottom-center',
    angel: 0,
    retina: true
};
for (var i = 0; i < positions.length; i++) {
    var up_Position = positions[i][0];
    var up_Data = {
        position: up_Position,
        icon: up_icon
    };
    var down_Position = positions[i][1];
    var down_Data = {
        position: down_Position,
        icon: down_icon
    };
    var up_label_marker = new AMap.LabelMarker(up_Data);
    var down_label_marker = new AMap.LabelMarker(down_Data);

    markers.push(up_label_marker);
    markers.push(down_label_marker);
}

// 一次性将海量点添加到图层
down_order_layer.add(markers);
}
var heatmap_button_mode = 0;
var isoline_button_mode = 0;
var up_order_button_mode = 0;
var down_order_button_mode = 0;
function onclick_heatmap() {
console.log("onclick_heatmap");
if(heatmap_button_mode==0)
{
    heatmap_layer.hide();
    $("#heatmap_btn").text("显示热力图");

    heatmap_button_mode = 1;
}
else if(heatmap_button_mode==1)
{
    heatmap_layer.show();
    $("#heatmap_btn").text("隐藏热力图");
    heatmap_button_mode = 0;
}
}
function onclick_isoline() {
console.log("onclick_isoline");
if(isoline_button_mode==0)
{
    contour_layer.hide();
    $("#isoline_btn").text("显示等值线");
    isoline_button_mode = 1;
}
else if(isoline_button_mode==1)
{
    contour_layer.show();
    $("#isoline_btn").text("隐藏等值线");
    isoline_button_mode = 0;
}
}
function onclick_uporder() {
console.log("onclick_uporder");
var uporder_btn = document.getElementById("uporder_btn");
if(up_order_button_mode==0)
{
    map.add(up_order_layer);
    $("#uporder_btn").text("隐藏上车订单起始点");

    up_order_button_mode = 1;
}
else if(up_order_button_mode==1)
{
    map.remove(up_order_layer);
    $("#uporder_btn").text("显示上车订单起始点");
    up_order_button_mode = 0;
}
}
function onclick_downorder() {
console.log("onclick_downorder");
if(down_order_button_mode==0)
{
    map.add(down_order_layer);
    $("#downorder_btn").text("隐藏下车订单起始点");
    down_order_button_mode = 1;
}
else if(down_order_button_mode==1)
{
    map.remove(down_order_layer);
    $("#downorder_btn").text("显示下车订单起始点");
    down_order_button_mode = 0;
}
}
function changeInterval(value) {
if(value == 0)
{
    heatmap_data = heatmap_data_1h;
    up_order = up_order_1h;
    down_order = down_order_1h;
}
else if(value == 1){
    heatmap_data = heatmap_data_30min;
    up_order = up_order_30min;
    down_order = down_order_30min;
}
else if(value == 2){
    heatmap_data = heatmap_data_10min;
    up_order = up_order_10min;
    down_order = down_order_10min;
}
}
function changeInterval(value) {
    console.log("changeInterval!");
    if(value != -1)
    {
        console.log(value);
        if(value == 0){
            time_interval = 60*60;
        }
        else if(value == 1){
            time_interval = 60 * 30;
        }
        else if(value == 2) {
            time_interval = 60 * 10;
        }
        console.log("current time:");
        console.log(heatmap_current_time);
        console.log("time_interval:");
        console.log(time_interval);
        console.log("current time idx:");
        console.log(parseInt((heatmap_current_time/1000 - minDateUnix)/time_interval));
         $.post("/interval", {interval:value, current_time : parseInt((heatmap_current_time/1000 - minDateUnix)/time_interval)},
            function(data, status) {

                heatmap_data_point = data.heatmap_data;
                up_order_data = data.uporder_data;
                down_order_data = data.downorder_data;
                contour_layer.setData(heatmap_data_point, {
                lnglat: 'lnglat',
                value: 'count'
            });


            contour_layer.setOptions({
                smoothNumber: 3,
                threshold: 3,
                interpolation: {
                    step: 300,
                    effectRadius: 1000,
                },
                style: {
                    height: 5 * 1E4,
                    color: ["#3656CD", "#655FE7", '#20C2E1', '#23D561', '#9CD523', '#F1E229', '#FFBF3A', '#FB8C00', '#FF5252', "#BC54E2", "#FF6FCE"]
                }
            });
            contour_layer.render();


             heatmap_layer.setData(heatmap_data_point, {
                lnglat: 'lnglat',
                value: 'count'
            });
            heatmap_layer.render();

            });
        console.log(heatmap_data_point[0]);

        map.remove(down_order_layer);
        $("#downorder_btn").text("显示下车订单始末点");
        down_order_button_mode = 0;
        map.remove(up_order_layer);
        $("#uporder_btn").text("显示上车订单始末点");
        up_order_button_mode = 0;
        set_up_order(up_order_data);
        set_down_order(down_order_data);
    }
}
function lockMapBounds() {
  var bounds = map.getBounds();

 // var bounds = { southWest:[103.822773,30.388466]  , northEast: [104.207021,30.641933] };
  map.setLimitBounds(bounds);
}
lockMapBounds();
var geocoder;

function regeoCode(location) {
if(!geocoder){
    geocoder = new AMap.Geocoder({
        city: "成都", //城市设为北京，默认：“全国”
    });
}
var lnglat  = [location.getLng(),location.getLat()];


geocoder.getAddress(lnglat, function(status, result) {
    if (status === 'complete'&&result.regeocode) {
        var address = result.regeocode.addressComponent['street']//.formattedAddress;
        if (address!=""){
            d3.selectAll(".city").style("opacity",0.01);
            d3.select("#"+address).style("opacity",1);
            d3.selectAll("#lineChart").selectAll(".titleText").remove();
            d3.selectAll("#lineChart").append("text").attr("class","titleText").attr("x",200).attr("y",200).text(address);
        }
    }else{
        console.log('根据经纬度查询地址失败')
    }
});
}
AMap.event.addListener(map, 'click', getLnglat);
function getLnglat(e) {
console.log("hadhasd");
var x = e.lnglat.getLng();
var y = e.lnglat.getLat();
regeoCode(e.lnglat)
}