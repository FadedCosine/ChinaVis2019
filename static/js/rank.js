var tickDuration = 1000;
var top_n = 12;
var width=420;
var height=400;
var state=1;
var svg2 = d3.select("#rank-chart")
    .append("svg")
    .attr('width',width)
    .attr('height', height);


  var margin = {
    top: 80,
    right: 0,
    bottom: 5,
    left: 10
  };
  
  var barPadding = (height-(margin.bottom+margin.top))/(top_n*5);
  
  var title = svg2.append('text')
    .attr("class","title")
    .attr("y",24)
    .html('道路流量排名表');
  
  var subTitle = svg2.append('text')
    .attr("class","subTitle")
    .attr("y",55)
    .html('订单数（每五分钟）');
  
  var caption = svg2.append('text')
    .attr("class","caption")
    .attr("x",width)
    .attr("y",height-5)
    .style("text-anchor","end")
    .html('SJTU');

  var timeIndex=0;
  var year = 1525104000000;
  currentTime=new Date(year);
  $.post("/rank", {top_n:'top_n'}, 
        function(data, status){
          console.log(data);
        
  
  /*d3.csv('https://gist.githubusercontent.com/johnburnmurdoch/2e5712cce1e2a9407bf081a952b85bac/raw/08cf82f5e03c619f7da2700d1777da0b5247df18/INTERBRAND_brand_values_2000_2018_decimalised.csv',
    function(data){*/
      var brandData=data;
     
      /*
      brandData.forEach(function(d) {
        d.value = +d.value,
        d.lastValue = +d.lastValue,
        d.value = isNaN(d.value) ? 0 : d.value,
        d.year = +d.time,
        d.colour = d3.hsl(Math.random()*360,0.75,0.75)
      });
*/

      var yearSlice=brandData[timeIndex];
      yearSlice.forEach(function(d){
        d.name=d.location,
        d.year=d.time,
        d.colour = d3.hsl(Math.random()*360,0.75,0.75)
      });
      timeIndex+=1;
      /*
      var yearSlice = brandData.filter(function(d){
        return d.year == year && !isNaN(d.value)})
      .sort(function(a,b){return b.value - a.value})
      .slice(0,top_n);
      
      yearSlice.forEach(function(d,i){
        d.rank = i;
      }); 
      */
      var yearSlice=yearSlice.slice(0,top_n);
      console.log(yearSlice);
      
      
      var x = d3.scale.linear()
        .domain([0, d3.max(yearSlice, function(d){return d.value;})])
        .range([margin.left, width-margin.right-65]);
      
      var y = d3.scale.linear()
        .domain([top_n, 0])
        .range([height-margin.bottom, margin.top]);
      
      var xAxis = d3.svg.axis()
        .scale(x).orient("top")
        .ticks(width > 500 ? 5:2)
        .tickSize(-(height-margin.top-margin.bottom))
        .tickFormat(function(d){return d3.format(',')(d);});
      
      svg2.append('g')
        .attr("class","axis xAxis")
        .attr("transform",`translate(0, ${margin.top})`)
        .call(xAxis)
        .selectAll('.tick line')
        .classed('origin', function(d) {return d == 0;});

      svg2.selectAll('rect.bar')
        .data(yearSlice, function(d){return d.name;})
        .enter()
        .append('rect')
        .attr("class","bar")
        .attr("x",x(0)+1)
        .attr("width",function(d){return x(d.value)-x(0)-1;})
        .attr("y",function(d){return y(d.rank)+5;})
        .attr("height",y(1)-y(0)-barPadding)
        .style("fill",function(d){return d.colour;});

  
      svg2.selectAll('text.label')
        .data(yearSlice, function(d){return d.name;})
        .enter()
        .append('text')
        .attr("class","label")
        .attr("x",function(d){return x(d.value)-8;})
        .attr("y",function(d){return y(d.rank)+5+((y(1)-y(0))/2)+1;})
        .attr("text-anchor","end")
        .html(function(d){return d.name;});
  
      svg2.selectAll('text.valueLabel')
        .data(yearSlice, function(d){return d.name;})
        .enter()
        .append('text')
        .attr("class","valueLabel")
        .attr("x",function(d){return x(d.value)+5;})
        .attr("y",function(d){return y(d.rank)+5+((y(1)-y(0))/2)+1;})
        .text(function(d){return d3.format(',.0f')(d.lastValue);});


      var halo = function(text, strokeWidth) {
        text.select(function() { return this.parentNode.insertBefore(this.cloneNode(true), this); })
          .style("fill","#ffffff")
          .style("stroke","#ffffff")
          .style("stroke-width",strokeWidth)
          .style("stroke-linejoin","round")
          .style("opacity",1);
      }

      var yearText = svg2.append('text')
        .attr("class","yearText")
        .attr("x",width-margin.right)
        .attr("y",height-25)
        .style('text-anchor','end')
        .html(function(d){
          currentTime=new Date(year);
          console.log(d3.selectAll('.timePath'));
          var currentHour=currentTime.getHours();
          var currentMinutes=currentTime.getMinutes();
          if (currentMinutes<10){
            currentMinutes="0"+currentMinutes;
          }
          return currentHour+":"+currentMinutes;
        })
        .call(halo, 10);
      
      var ticker=null;
      function showChart(year){
      timeIndex=parseInt((year-1525104000000)/(300*1000));
      var yearSlice=brandData[timeIndex];
        yearSlice.forEach(function(d){
          d.name=d.location,
          d.year=d.time,
          d.colour = d3.hsl(Math.random()*360,0.75,0.75)
        });
        //timeIndex+=1;
        var yearSlice=yearSlice.slice(0,top_n);
        //yearSlice.forEach(function(d,i){return d.rank = i;});
        
        x.domain([0, d3.max(yearSlice, function(d) {return d.value;})]);
        
        svg2.select('.xAxis')
          .transition()
          .duration(tickDuration)
          .ease("linear")
          .call(xAxis);
        
        var bars = svg2.selectAll('.bar').data(yearSlice, 
          function(d){return d.name;});

        bars.enter()
          .append('rect')
          .attr("class",function(d){return  `bar ${d.name.replace(/\s/g,'_')}`;})
          .attr("x",x(0)+1)
          .attr("width",function(d){return x(d.value)-x(0)-1;})
          .attr("y",function(d){return y(top_n+1)+5;})
          .attr("height",y(1)-y(0)-barPadding)
          .style("fill",function(d){return d.colour;})
          .transition()
          .duration(tickDuration)
          .ease("linear")
          .attr("y",function(d){return y(d.rank)+5;});
        
        bars.transition()
          .duration(tickDuration)
          .ease("linear")
          .attr("width",function(d){return x(d.value)-x(0)-1;})
          .attr("y",function(d){return y(d.rank)+5;});
      
        bars.exit()
          .transition()
          .duration(tickDuration)
          .ease("linear")
          .attr("width",function(d){return x(d.value)-x(0)-1;})
          .attr("y",function(d){return y(top_n+1)+5;})
          .remove();


        var labels = svg2.selectAll('.label').data(yearSlice, 
          function(d){return d.name;});
    
        labels.enter()
        .append('text')
        .attr("class","label")
        .attr("x",function(d){return x(d.value)-8;})
        .attr("y",function(d){return y(top_n+1)+5+((y(1)-y(0))/2);})
        .attr("text-anchor","end")
        .html(function(d){return d.name;})    
        .transition()
        .duration(tickDuration)
        .ease("linear")
        .attr("y",function(d){return y(d.rank)+5+((y(1)-y(0))/2)+1;});
    
        labels
        .transition()
        .duration(tickDuration)
        .ease("linear")
        .attr("x",function(d){return x(d.value)-8;})
        .attr("y",function(d){return y(d.rank)+5+((y(1)-y(0))/2)+1;});
    
        labels.exit()
        .transition()
        .duration(tickDuration)
        .ease("linear")
        .attr("x",function(d){return x(d.value)-8;})
        .attr("y",function(d){return y(top_n+1)+5;})
        .remove();


        var valueLabels = svg2.selectAll('.valueLabel').data(yearSlice, 
          function(d){return d.name;});
    
        valueLabels.enter()
          .append('text')
          .attr("class","valueLabel")
          .attr("x",function(d){return x(d.value)+5;})
          .attr("y",function(d){return y(d.value)+5;})
          .text(function(d){return d3.format(',.0f')(d.lastValue);})
          .transition()
          .duration(tickDuration)
          .ease("linear")
          .attr("y",function(d){return y(d.rank)+5+((y(1)-y(0))/2)+1;});
        
        valueLabels.transition()
          .duration(tickDuration)
          .ease("linear")
          .attr("x",function(d){return x(d.value)+5;})
          .attr("y",function(d){return y(d.rank)+5+((y(1)-y(0))/2)+1;})
          .tween("text", function(d) {
            var i = d3.interpolateRound(d.lastValue, d.value);
            return function(t) {
              this.textContent = d3.format(',')(i(t));
            };
          });

        valueLabels.exit()
          .transition()
          .duration(tickDuration)
          .ease("linear")
          .attr("x",function(d){return x(d.value)+5;})
          .attr("y",function(d){return y(top_n+1)+5;})
          .remove();
        
        yearText.html(function(d){
          currentTime=new Date(year);
          var currentHour=currentTime.getHours();
          var currentMinutes=currentTime.getMinutes();
          if (currentMinutes<10){
            currentMinutes="0"+currentMinutes;
          }
          return currentHour+":"+currentMinutes;
        });
      }
      function setTicker(){
        ticker = setInterval(function(e){
        showChart(year);
        year = year+300*1000;
      },tickDuration);}
    setTicker();
    d3.select('#progressSlider').call(
      d3.slider().scale(d3.time.scale()
    .domain([new Date(1525104000000), new Date(1525190399000)]))
    .axis(d3.svg.axis())
    .value(1525104060000)
    .on("slide", function(evt, value) {
      currentTime=new Date(value);
      var currentHour=currentTime.getHours();
      var currentMinutes=currentTime.getMinutes();
      if (currentMinutes<10){
        currentMinutes="0"+currentMinutes;
      }
      d3.selectAll("text.yearText").html(currentHour+":"+currentMinutes);
      clearInterval(ticker);
      year=value;
      showChart(year);
      state=0;
    }));
    $("#stopBtn").click(function(){
        if (state==1) {
            clearInterval(ticker);
            state=0;
        } else {
            setTicker();
            state=1;
        }
    });
      //var nameList=[]
  });

/*
  
  
  
    
  
  },tickDuration);

  return svg.node();
  */