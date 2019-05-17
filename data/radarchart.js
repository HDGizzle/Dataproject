var RadarChart = {
  draw: function(id, d, cfg, d2){
// define axes and circle parameters
  var allAxis = (d[0].map(function(i, j){return i.nutrient}));
  var total = allAxis.length;
  var radius = cfg.factor*Math.min(cfg.w/2, cfg.h/2);
  var Format = d3.format('%');
  d3.select(id).select("svg").remove();

  var g = d3.select(id)
    .append("svg")
    .attr("width", cfg.w+cfg.ExtraWidthX)
    .attr("height", cfg.h+cfg.ExtraWidthY)
    .append("g")
    .attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");
// initiate tooltip
  var tooltip = d3.select("body").append("div").attr("class", "toolTip");
// draw the benchmark circles of the graph
  for(var j=0; j<cfg.levels; j++){
    var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
    g.selectAll(".levels")
     .data(allAxis)
     .enter()
     .append("svg:line")
     .attr("x1", function(d, i){return levelFactor*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
     .attr("y1", function(d, i){return levelFactor*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
     .attr("x2", function(d, i){return levelFactor*(1-cfg.factor*Math.sin((i+1)*cfg.radians/total));})
     .attr("y2", function(d, i){return levelFactor*(1-cfg.factor*Math.cos((i+1)*cfg.radians/total));})
     .attr("class", "line")
     .style("stroke", "grey")
     .style("stroke-opacity", "0.75")
     .style("stroke-width", "0.3px")
     .attr("transform", "translate(" + (cfg.w/2-levelFactor) + ", " + (cfg.h/2-levelFactor) + ")");
  }
// draw the percentual values of the graph
  for(var j=0; j<cfg.levels; j++){
    var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
    g.selectAll(".levels")
     .data([1]) //dummy data
     .enter()
     .append("svg:text")
     .attr("x", function(d){return levelFactor*(1-cfg.factor*Math.sin(0));})
     .attr("y", function(d){return levelFactor*(1-cfg.factor*Math.cos(0));})
     .attr("class", "legend")
     .style("font-family", "sans-serif")
     .style("font-size", "10px")
     .attr("transform", "translate(" + (cfg.w/2-levelFactor + cfg.ToRight) + ", " + (cfg.h/2-levelFactor) + ")")
     .attr("fill", "#737373")
     .text((j+1)*100/cfg.levels);
  }

  series = 0;
// initiate axis variable
  var axis = g.selectAll(".axis")
      .data(allAxis)
      .enter()
      .append("g")
      .attr("class", "axis");
// draw "web" spokes
  axis.append("line")
    .attr("x1", cfg.w/2)
    .attr("y1", cfg.h/2)
    .attr("x2", function(d, i){return cfg.w/2*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
    .attr("y2", function(d, i){return cfg.h/2*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
    .attr("class", "line")
    .style("stroke", "grey")
    .style("stroke-width", "1px");
// draw nutrient names at spoke axes
  axis.append("text")
    .attr("class", "legend")
    .text(function(d){return d})
    .style("font-family", "sans-serif")
    .style("font-size", "11px")
    .attr("text-anchor", "middle")
    .attr("dy", "1.5em")
    .attr("transform", function(d, i){return "translate(0, -10)"})
    .attr("x", function(d, i){return cfg.w/2*(1-cfg.factorLegend*Math.sin(i*cfg.radians/total))-60*Math.sin(i*cfg.radians/total);})
    .attr("y", function(d, i){return cfg.h/2*(1-Math.cos(i*cfg.radians/total))-20*Math.cos(i*cfg.radians/total);});
// draw and color data area - change opacity when hovered over

  if (typeof d !== undefined){
    WebDrawer(d, g, cfg, total, tooltip);
  };
  if (typeof d2 !== undefined){
    WebDrawer(d2, g, cfg, total, tooltip);
  };
  }
};

var WebDrawer = function(input, g, cfg, total, tooltip) {
  input.forEach(function(y, x){
    dataValues = [];
    g.selectAll(".nodes")
    .data(y, function(j, i){
      if (j.value > j.max){
        dataValues.push([
        cfg.w/2*(1-(parseFloat(1)*cfg.factor*Math.sin(i*cfg.radians/total))),
        cfg.h/2*(1-(parseFloat(1)*cfg.factor*Math.cos(i*cfg.radians/total)))
        ]);
      }
      else {
      dataValues.push([
      cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/j.max)*cfg.factor*Math.sin(i*cfg.radians/total)),
      cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/j.max)*cfg.factor*Math.cos(i*cfg.radians/total))
      ]);
    }
    });
    dataValues.push(dataValues[0]);
    g.selectAll(".nutrient")
     .data([dataValues])
     .enter()
     .append("polygon")
     .attr("class", "radar-chart-serie"+series)
     .style("stroke-width", "2px")
     .style("stroke", cfg.color(series))
     .attr("points",function(d) {
       var str="";
       for (pti = 0; pti < d.length; pti++){
         str=str+d[pti][0]+","+d[pti][1]+" ";
       }
       return str;
      })
     .style("fill", function(j, i){return cfg.color(series)})
     .style("fill-opacity", cfg.opacityArea)
     .on('mouseover', function (d){
      z = "polygon."+d3.select(this).attr("class");
      g.selectAll("polygon")
       .transition(200)
       .style("fill-opacity", 0.1);
      g.selectAll(z)
       .transition(200)
       .style("fill-opacity", .7);
      })
     .on('mouseout', function(){
      g.selectAll("polygon")
       .transition(200)
       .style("fill-opacity", cfg.opacityArea);
   });
    series++;
  });
  series=0;

// add data dots on spokes with tooltip
  input.forEach(function(y, x){
    g.selectAll(".nodes")
    .data(y).enter()
    .append("svg:circle")
    .attr("class", "radar-chart-serie"+series)
    .attr('r', cfg.radius)
    .attr("alt", function(j){return Math.max(j.value, 0)})
    .attr("cx", function(j, i){
      if (j.value > j.max) {
        dataValues.push([
        cfg.w/2*(1-(parseFloat(1)*cfg.factor*Math.sin(i*cfg.radians/total))),
        cfg.h/2*(1-(parseFloat(1)*cfg.factor*Math.cos(i*cfg.radians/total)))
        ]);
        return cfg.w/2*(1-(1)*cfg.factor*Math.sin(i*cfg.radians/total));
      }
      else {
        dataValues.push([
        cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/j.max)*cfg.factor*Math.sin(i*cfg.radians/total)),
        cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/j.max)*cfg.factor*Math.cos(i*cfg.radians/total))
        ]);
        return cfg.w/2*(1-(Math.max(j.value, 0)/j.max)*cfg.factor*Math.sin(i*cfg.radians/total));
      }
    })
    .attr("cy", function(j, i){
      if (j.value > j.max) {
        return cfg.h/2*(1-(1)*cfg.factor*Math.cos(i*cfg.radians/total));
      }
      else {
        return cfg.h/2*(1-(Math.max(j.value, 0)/j.max)*cfg.factor*Math.cos(i*cfg.radians/total));
      }
    })
    .attr("data-id", function(j){return j.nutrient})
    .style("fill", "#fff")
    .style("stroke-width", "2px")
    .style("stroke", cfg.color(series)).style("fill-opacity", .9)
    .on('mouseover', function (d){
      tooltip.style("left", d3.event.pageX - 40 + "px")
        .style("top", d3.event.pageY - 80 + "px")
        .style("display", "inline-block")
        .html((d.nutrient) + "<br><span>" + (d.value) + "</span>");
    })
      .on("mouseout", function(d){ tooltip.style("display", "none");});
    series++;
  });
}
