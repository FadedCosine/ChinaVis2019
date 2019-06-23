var margin = {top: 20, right: 10, bottom: 30, left: 40},
    width = 450 - margin.left - margin.right,
    height = 240 - margin.top - margin.bottom;


var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category20();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.temperature); });

var svg = d3.select("#lineChart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.tsv("../static/data/average_speed_10minutes.tsv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));
  //color.domain(d3.keys(data[0]).filter(function(key){return key!=data[0]}))
  data.forEach(function(d) {
    d.date = new Date(d.date*1000);
  });

  var cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, temperature: +d[name]};
      })//.filter(function(d){return +d.temperature!=0;})
    };
  });
  console.log(cities);
  x.domain(d3.extent(data, function(d) { return d.date; }));

  var yMax=d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; });});
  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
    //d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
    yMax
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + 200 + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("平均速度（每五分钟）");

  var city = svg.selectAll(".city")
      .data(cities)
      .enter().append("g")
      .attr("class", "city")
      .attr("id",function(d){
        return d.name;
      })

  /*svg.append("line")
  .attr("class","timePath").attr("x1",x(new Date(1525104000000))).attr("y1",y(yMax))
  .attr("x2",x(new Date(1525104000000))).attr("y2",y(0))
  .attr("stroke","black").attr("stroke-width","2px");
*/
  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .style('text-anchor','middle')
    .html(function (d) {return d.name;});

  svg.call(tip);

  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); })


/*
  city.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });
  */
  var clickFlag=0;
  /*
  city.selectAll("circle")
    .data(function(d){return d.values})
    .enter()
    .append("circle")
    .attr("r", 1)
    .attr("cx", function(d) { return x(d.date); })
    .attr("cy", function(d) { return y(d.temperature); })
    .style("fill", function(d,i,j) { return color(cities[j].name); })
    .on("mouseover",function(d){
      tip.show(d);
      d3.selectAll(".city").style("opacity",0.1);
      d3.select(this.parentNode).style("opacity",1);
    })
    .on("mouseout",function(d){
      tip.hide(d);
      if (clickFlag==0)
        d3.selectAll(".city").style("opacity",1);
    })
    .on("click",function(d){
      if (clickFlag==0){
        d3.selectAll(".city").style("opacity",0.1);
        d3.select(this.parentNode).style("opacity",1);
        clickFlag=1;
      }
      else{
        d3.selectAll(".city").style("opacity",1);
        clickFlag=0;
      }
    });
*/
  city.style("opacity",0.1).on("mouseover",function(d){
      tip.show(d);
      d3.selectAll(".city").style("opacity",0.01);
      d3.select(this).style("opacity",1);
  }).on("mouseout",function(d){
      tip.hide(d);
      d3.selectAll(".city").style("opacity",1);
  });


});