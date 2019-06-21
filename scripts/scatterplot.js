var Scatterplot = {
  draw: function(data, xtext, cfg, linked) {
// define data for x and y axis
var x = function(d) { return d.nutrient; }
var y = function(d) { return d.kcal; }

// scale data for x and y axis
var xScaler = function(d) { return xScale(d.nutrient); }

var yScaler = function(d) { return yScale(d.kcal); }

console.log(linked);

// define colors for scatterplot categories
var colorcategory = function(d) {
  if (d.Fruit === linked) { return "#000000";}
  else { return d.color;}
 }

 var circleradius = function(d) {
   if (d.Fruit === linked) { return 8;}
   else { return 5;}
  }

// define text for axes and title
var ytext = "Kcal per 100 grams"

// define tooltip data and according text
var tooltipdata = (d) => {
  tooltip.transition().duration(200).style('opacity', 0.9);
  // replace text with desired tooltip text
  tooltip.html(`<span>${d.Fruit}</span> <br> Calories:  <span>${d.kcal}</span> <br>  <span>${xtext}</span>:  <span>${d.nutrient}</span>`)
  .style('left', `${d3.event.layerX}px`)
  .style('top', `${(d3.event.layerY - 28)}px`);
}

// function for xScaler
   var xScale = d3.scaleLinear()
     .domain([(d3.min(data, x)) - (d3.max(data, x) / 75), d3.max(data, x) + (d3.max(data, x) / 50)])
     .range([cfg.margin, cfg.w - cfg.margin * 4]);

   // Function for yScaler
   var yScale = d3.scaleLinear()
  // d3.min(data, y) - (d3.max(data, y) / 25) if you do not want to start at 0
     .domain([0, d3.max(data, y) + (d3.max(data, y) / 15)])
     .range([cfg.h - cfg.margin, cfg.margin]);

   // axis scaling
   var xAxis = d3.axisBottom().scale(xScale);
   var yAxis = d3.axisLeft().scale(yScale);

   // define scatterplot tooltip
   const tooltip = d3.select('plot').append('div')
     .attr('class', 'tooltip')

   // create scatterplot svg
   var svg = d3.select("#scattersvg")
         .attr("width", cfg.w)
         .attr("height", cfg.h);

   // draw dots with according color and tooltip
   svg.selectAll("circle")
     .data(data)
     .enter()
     .append("circle")
     .attr("cx", xScaler)
     .attr("cy", yScaler)
     .attr("r", circleradius)
     .attr("fill", (colorcategory))
     .style("stroke-width", "2px")
     .style("stroke", "#000000")
     .on('mouseover', tooltipdata)
     .on('mouseout', () => tooltip.transition().duration(500).style('opacity', 0))


   // draw x axis title
   svg.append('text')
     .style("font", "12px Sans-serif")
     .attr('x', cfg.w - cfg.margin * 4)
     .attr('y', cfg.h - cfg.margin * 1.2)
     .attr('text-anchor', 'end')
     .attr('class', 'label')
     .text(xtext);



   // draw x axis
   svg.append("g")
     .attr("class", "axis")
     .attr("transform", "translate(000," + (cfg.h - cfg.margin) + ")")
     .call(xAxis)
     .style("font", "15px Sans-serif")

   // draw y axis
   svg.append("g")
     .attr("class", "axis")
     .attr("transform", "translate(" + cfg.margin + ")")
     .call(yAxis)
     .style("font", "15px Sans-serif")
     .append("text")
     .attr("fill", "#000")
     .attr("transform", "rotate(-90)")
     .attr("x", - cfg.margin)
     .attr("dy", "2em")
     .attr("text-anchor", "end")
     .text(ytext);
}
}
