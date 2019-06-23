  /*d3.select('#slider').call(d3.slider().scale(d3.time.scale()
    .domain([new Date(1984,1,1), new Date(2014,1,1)])).axis(d3.svg.axis())
    .value(new Date(2000,1,1))
    .on("slide", function(evt, value) {
      d3.select("text.title").text(value);
    }));*/
d3.select("#speedSlider").call(
	d3.slider().scale(d3.scale.ordinal()
	.domain(["1×", "2×", "3×", "5×","10×"])
	.rangePoints([0, 1], 0.5)).axis( d3.svg.axis() )
	.snap(true).value("1×"));


d3.select('#intervalSlider')
.call(d3.slider().axis(true)
	.min(5).max(60).step(10).snap(true));