var RadarData = function(){

  var radarconfig = {radius: 5, w: 550, h: 550, factor: 1, factorLegend: .85,
   levels: 10, radians: 2 * Math.PI, opacityArea: 0.5, ToRight: 5,
   TranslateX: 80, TranslateY: 80, ExtraWidthX: 170, ExtraWidthY: 120,
   color: d3.scaleOrdinal().range(["#800000", "#ffa500"])
  }

  // load data
  d3.json("data/nutrients.json").then(function (datas) {
  // extract fruit name strings
    fruitnames = Object.keys(datas)
  // extract nutrient name strings
    nutrienttypes = Object.keys(datas[fruitnames[0]])
    nutrienttypes.splice(0, 9)
    nutrienttypes.splice(2, 1)
    nutrienttypes.splice(4, 1)
    nutrienttypes.splice(5, 1)
    nutrienttypes.splice(6, 2)
    nutrienttypes.splice(7, 2)
    nutrienttypes.splice(8, 1)
    nutrienttypes.splice(10, 2)
    console.log(nutrienttypes);

    var select = document.getElementById("radar-dropdown");
    var select2 = document.getElementById("radar-dropdown2");

    for(var i = 0; i < fruitnames.length; i++) {
        var opt = fruitnames[i];
        var el = document.createElement("option");
        var el2 = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        el2.textContent = opt;
        el2.value = opt;
        select2.appendChild(el2);
        select.appendChild(el);

    }

  // recommended daily maxes of relevant nutrients
    maxes = [30, 300, 325, 15, 3000, 1.3, 1, 800, 1.3, 80];

  d3.select("#radar-dropdown").on("change",function(d){
   var grams = d3.select("#Grams").node().value;
   data = []
   DropdownObjectGrams("#radar-dropdown", datas, nutrienttypes, maxes, data, grams);
   dataz = [data]
  });

  d3.select("#radar-dropdown2").on("change",function(d){
     var grams = d3.select("#Grams").node().value;
     data2 = []
     DropdownObjectGrams("#radar-dropdown2", datas, nutrienttypes, maxes, data2, grams);
     dataz2 = [data2]
  });

  d3.select("#Grams").on("change",function(d){
    var grams = d3.select("#Grams").node().value;

    data = []
    DropdownObjectGrams("#radar-dropdown", datas, nutrienttypes, maxes, data, grams);
    dataz = [data]

    data2 = []
    DropdownObjectGrams("#radar-dropdown2", datas, nutrienttypes, maxes, data2, grams);
    dataz2 = [data2]
  })

  d3.select("#Kcaltoggle").on("click", function(d){
      var checkBox = document.getElementById("Kcaltoggle");
      if (checkBox.checked == false) {
        var grams = d3.select("#Grams").node().value;
        document.getElementById('unitlabel').innerHTML = 'Grams:';
        data = []
        DropdownObjectGrams("#radar-dropdown", datas, nutrienttypes, maxes, data, grams);
        dataz = [data]
        data2 = []
        DropdownObjectGrams("#radar-dropdown2", datas, nutrienttypes, maxes, data2, grams);
        dataz2 = [data2]
        if (typeof dataz === "undefined") {
           RadarChart.draw("#radar-svg", dataz2, radarconfig);
        }
        if (typeof dataz2 === "undefined") {
           RadarChart.draw("#radar-svg", dataz, radarconfig)
        }
        if (typeof dataz2 !== "undefined" && dataz !== "undefined") {
          RadarChart.draw("#radar-svg", dataz, radarconfig, dataz2);
        }

      }
      else {
        var grams = d3.select("#Grams").node().value;
        document.getElementById('unitlabel').innerHTML = 'Kcal:';
        data = []
        DropdownObjectKcal("#radar-dropdown", datas, nutrienttypes, maxes, data, grams);
        dataz = [data]
        data2 = []
        DropdownObjectKcal("#radar-dropdown2", datas, nutrienttypes, maxes, data2, grams);
        dataz2 = [data2]
        if (typeof dataz === "undefined") {
           RadarChart.draw("#radar-svg", dataz2, radarconfig);
        }
        if (typeof dataz2 === "undefined") {
           RadarChart.draw("#radar-svg", dataz, radarconfig)
        }
        if (typeof dataz2 !== "undefined" && dataz !== "undefined") {
          RadarChart.draw("#radar-svg", dataz, radarconfig, dataz2);
        }
      }
  });

  d3.select("#comparebutton").on("click",function(d){
    if (typeof dataz === "undefined") {
       RadarChart.draw("#radar-svg", dataz2, radarconfig);
    }
    if (typeof dataz2 === "undefined") {
       RadarChart.draw("#radar-svg", dataz, radarconfig)
    }
    if (typeof dataz2 !== "undefined" && dataz !== "undefined") {
      RadarChart.draw("#radar-svg", dataz, radarconfig, dataz2);
    }
  });

  })
};





var BarData = function() {
// function to change bar chart when new nutrient is chosen in dropdown
    d3.select("#barchart-dropdown").on("change",function(d){
// clear previously drawn svg
        d3.selectAll("#histosvg > *").remove();
// get string of nutrient names
        var selected = d3.select("#barchart-dropdown").node().value;
        console.log(selected);
// load json file
        d3.json("data/nutrients.json").then(function (data) {
// extract fruit names
          var fruitnames = Object.keys(data);
// initialize reformatted data list
          var figuredata = []

          console.log(figuredata);
        d3.json("data/fruitcolors.json").then(function (colors) {
          console.log(colors);

// Reformat data to list of dicts with universal keys
          for (i = 0; i < fruitnames.length; i++) {
            var nutrient = data[fruitnames[i]][selected];
            if (nutrient != null) {
            color = colors[fruitnames[i]]["color"]
            var dict = {"Fruit": fruitnames[i], "nutrient": nutrient, "color": color}
            figuredata.push(dict);
            }
            };

            ObjectSorter(figuredata, "nutrient");

            d3.json("data/nutrientinfo.json").then(function (info) {
              info = info[selected];

// call barchart function
          if (selected !== "Choose a nutrient") {
          BarChart.draw(figuredata, selected, info);
        }
        })
        })
      })

      });
};



var LinkedBarData = function(nutrientname, pickedfruit) {
// clear previously drawn svg
    d3.selectAll("#histosvg > *").remove();
// get string of nutrient names
    var selected = nutrientname;
    console.log(selected);
// load json file
    d3.json("data/nutrients.json").then(function (data) {
// extract fruit names
      var fruitnames = Object.keys(data);
// initialize reformatted data list
      var figuredata = []
    d3.json("data/fruitcolors.json").then(function (colors) {
      console.log(colors);

// Reformat data to list of dicts with universal keys
      for (i = 0; i < fruitnames.length; i++) {
        var nutrient = data[fruitnames[i]][selected];
        if (nutrient != null) {
        color = colors[fruitnames[i]]["color"]
        var dict = {"Fruit": fruitnames[i], "nutrient": nutrient, "color": color}
        figuredata.push(dict);
        }
        };

        ObjectSorter(figuredata, "nutrient");

        d3.json("data/nutrientinfo.json").then(function (info) {
          info = info[selected];

// call barchart function
          BarChart.draw(figuredata, selected, info, pickedfruit);
        })
        })
      })
};


var ScatterData = function() {
  scatterconfig = {margin: 40, w: 1000, h: 500};

// function to change bar chart when new nutrient is chosen in dropdown
  d3.select("#scatter-dropdown").on("change",function(d){
// clear previously drawn svg
      d3.selectAll("#scattersvg > *").remove();
// get string of nutrient names
      var selected = d3.select("#scatter-dropdown").node().value;
      console.log(selected);
// load json file
      d3.json("data/nutrients.json").then(function (data) {
// extract fruit names
        var fruitnames = Object.keys(data);
// initialize reformatted data list
        var figuredata = []

        console.log(figuredata);
      d3.json("data/fruitcolors.json").then(function (colors) {
        console.log(colors);

// Reformat data to list of dicts with universal keys
        for (i = 0; i < fruitnames.length; i++) {
          var nutrient = data[fruitnames[i]][selected];
          if (nutrient != null) {
            color = colors[fruitnames[i]]["color"]
            var dict = {"Fruit": fruitnames[i], "nutrient": nutrient, "color": color, "kcal": data[fruitnames[i]]["Energy in kcal"]}
            figuredata.push(dict);
          }
          };
          console.log(figuredata);
        if (selected !== "Choose a nutrient") {
        Scatterplot.draw(figuredata, selected, scatterconfig);
      }
      })
    })

    });
}

var LinkedScatterData = function(nutrientname, pickedfruit) {
  scatterconfig = {margin: 40, w: 1000, h: 500};
  console.log(pickedfruit);
// function to change bar chart when new nutrient is chosen in dropdown
// clear previously drawn svg
      d3.selectAll("#scattersvg > *").remove();
// get string of nutrient names
      var selected = nutrientname
      console.log(selected);
// load json file
      d3.json("data/nutrients.json").then(function (data) {
// extract fruit names
        var fruitnames = Object.keys(data);
// initialize reformatted data list
        var figuredata = []

        console.log(figuredata);
      d3.json("data/fruitcolors.json").then(function (colors) {
        console.log(colors);

// Reformat data to list of dicts with universal keys
        for (i = 0; i < fruitnames.length; i++) {
          var nutrient = data[fruitnames[i]][selected];
          if (nutrient != null) {
            color = colors[fruitnames[i]]["color"]
            var dict = {"Fruit": fruitnames[i], "nutrient": nutrient, "color": color, "kcal": data[fruitnames[i]]["Energy in kcal"]}
            figuredata.push(dict);
          }
          };
          console.log(figuredata);

        Scatterplot.draw(figuredata, selected, scatterconfig, pickedfruit);
      })
    })
}

var ObjectSorter = function(arr, key) {
    return arr.sort((a, b) => {
        return a[key] - b[key];
    });
};
