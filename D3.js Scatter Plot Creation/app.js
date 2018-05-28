var margin = {top: 20, right: 20, bottom: 50, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scaleLinear()
    .range([0, width]);

var y = d3.scaleLinear()
    .range([height, 0]);

var color = d3.scaleOrdinal(d3.schemeCategory10);

var xAxis = d3.axisBottom(x);

var yAxis = d3.axisLeft(y);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("data.csv", function(error, data) {
  if (error) throw error;

  data.forEach(function(d) {
    d.active_past_month = +d.active_past_month;
    d.bachelors_over_25 = +d.bachelors_over_25;
  });

  x.domain(d3.extent(data, function(d) { return d.bachelors_over_25; })).nice();
  y.domain(d3.extent(data, function(d) { return d.active_past_month; })).nice();

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Sepal Width (cm)");

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Sepal Length (cm)")

  var toolTip = d3.select("body")
      .append("div")
      .style("display", "none")
      .classed("tooltip", true)

  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5)
      .attr("cx", function(d) { return x(d.bachelors_over_25); })
      .attr("cy", function(d) { return y(d.active_past_month); })
      .style("fill", "grey") //function(d) { return color(d.state); });
      .on("mouseover", function (d) {
        toolTip.style("display", "block")
          .html(
            `<strong>${d.bachelors_over_25}<strong>`)
          .style("left", d3.event.pageX + "px")
          .style("top", d3.event.pageY + "px")
      })
      // Step 3: Create "mouseout" event listener to hide tooltip
      .on("mouseout", function () {
        toolTip.style("display", "none")
      });
  svg.selectAll(".dodo")
      .data(data)
     .enter().append("text")
      .attr("class", "dodo")
      .attr("x", function(d) { return x(d.bachelors_over_25); })
      .attr("y", function(d) { return y(d.active_past_month); })
      .attr("dx", "-.8em")
      .attr("dy", ".35em")
      .text(function(d) { return d.abbv;});

  svg.append("text")             
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("% Population with Bachelors Degree or Higher");  
  
  svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("% of People Who Exercise >= Once per Month"); 
  
      //var legend = svg.selectAll(".legend")
      //.data(color.domain())
    //.enter().append("g")
      //.attr("class", "legend")
      //.attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  //legend.append("rect")
      //.attr("x", width - 18)
      //.attr("width", 18)
      //.attr("height", 18)
      //.style("fill", color);

  //legend.append("text")
      //.attr("x", width - 24)
      //.attr("y", 9)
      //.attr("dy", ".35em")
     // .style("text-anchor", "end")
     // .text(function(d) { return d; });

});