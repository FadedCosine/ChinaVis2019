$("input[name='barOption']").change(function(){
    var barOption=this.id;
    var chart;
    var data;
    $(".choice-label").css("background-color","white");
    if (barOption=='countsOption'){
        chart = new SproutChart(document.getElementById('part2'), data_sex);
        data=data_sex;
        $("label[for=countsOption]").css("background-color","yellow");
    }
    else if (barOption=='speedOption'){
        chart = new SproutChart(document.getElementById('part2'), data_degree);
        data=data_degree;
        $("label[for=speedOption]").css("background-color","yellow");
    }
    console.log(chart);
    var tmpHeight;
    if (data.length>8)
        tmpHeight=200/data.length;
    else tmpHeight=30

    var options = {
        offx:60,
        offy:-50,
        barHeight: tmpHeight,
        r: 120,
        innerRadius: 90,
        rHover: 120
    };
    chart.pieChart(options);

    $("#changeBtn").click(function(){
        if (this.checked) {
            chart.transformTo('pie', options);
        } else {
            chart.transformTo('bar', options);
        }
    });

});