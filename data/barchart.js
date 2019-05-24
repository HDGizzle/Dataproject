var BarChart = {
  draw: function(figuredata, nutrientname, nutrientinfo) {

    console.log(nutrientinfo);
// define svg parameters
  var svg = d3.select("#histosvg"),
    margin = {top: 20, right: 20, bottom: 60, left: 80},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;
// define bar colours
  var colours = d3.scaleOrdinal()
    .range(["#6F257F", "#CA0D59"]);
// define tooltip
  var tooltip = d3.select("body").append("div").attr("class", "tooltip");
  var tooltip2 = d3.select("body").append("div").attr("class", "tooltip2");
// scale x and y axis
  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
      y = d3.scaleLinear().rangeRound([height, 0]);
// define drawing boundaries
  var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// distribute data over x and y axes
  x.domain(figuredata.map(function(d) { return d.Fruit; }));
  y.domain([0, d3.max(figuredata, function(d) { return d.nutrient; })]);

// draw x axis info
  g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
    .style("text-anchor", "right")
    .attr("dx", "1.5em")
    .attr("dy", "2.5em")
    .attr("transform", "rotate(25)");
// draw y axis info
  g.append("g")
    .attr("class", "axis axis--y")
    .call(d3.axisLeft(y).ticks(5).tickFormat(function(d) { return d; }).tickSizeInner([-width]))
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -38)
    .attr("dy", "0.1em")
    .attr("text-anchor", "end")
    .attr("fill", "#5D6971")
    .text(nutrientname);
// draw bars and add tooltip
  g.selectAll("rect")
      .data(figuredata)
    .enter().append("rect")
      .attr("x", function(d) { return x(d.Fruit); })
      .attr("y", function(d) { return y(d.nutrient); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.nutrient); })
      .attr("fill", function(d) { return d.color; })
      .style("fill-opacity", .7)
      .on("mouseover", function(d, i) {
        var xPos = +d3.select(this).attr("x")
        var wid = +d3.select(this).attr("width");
        d3.select(this).attr("x", xPos - 10).attr("width", wid + 20);
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip.html((d.Fruit) + "<br>" + (nutrientname) + (": ") + (d.nutrient))
        .style('left', `${d3.event.layerX}px`)
        .style('top', `${(d3.event.layerY - 28)}px`);})
      .on("mouseout", function() {
    d3.select(this).attr("x", function(d) {
            return x(d.Fruit)})
        .attr("width", x.bandwidth());
        tooltip.transition().duration(500).style('opacity', 0)});

  g.append("g")
    .attr("class", "Qmark")
    .append("text")
    .attr("x", 26)
    .attr("y", 19)
    .attr("text-anchor", "end")
    .attr("fill", "black")
    .text("?");

  g.append("rect")
    .attr("x", 10)
    .attr("y", 0)
    .attr("width", 25)
    .attr("height", 25)
    .style("fill", "#800000")
    .style("fill-opacity", .6)
    .on('mouseover', function (d){
      tooltip2.style("left", d3.event.pageX - 40 + "px")
        .style("top", d3.event.pageY - 80 + "px")
        .style("display", "inline-block")
        .html(nutrientinfo[0] + "<br><br>" + "<em>Too much?</em>" + "<br>" + nutrientinfo[1] + "<br><br>" + "<em>Too little?</em>" + "<br>" + nutrientinfo[2])
    })
      .on("mouseout", function(d){ tooltip2.style("display", "none");});

}
};
