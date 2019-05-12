var BarChart = {
  draw: function(figuredata, nutrientname) {
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
    .attr("y", -35)
    .attr("dy", "0.71em")
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
      .on('mouseover', (d) => {
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip.html((d.Fruit) + "<br>" + (nutrientname) + (": ") + (d.nutrient))
        .style('left', `${d3.event.layerX}px`)
        .style('top', `${(d3.event.layerY - 28)}px`);})
      .on('mouseout', () => tooltip.transition().duration(500).style('opacity', 0));


   }
};
