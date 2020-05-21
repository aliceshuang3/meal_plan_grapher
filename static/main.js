// Tutorials:
// https://plot.ly/javascript/ajax-call/
// https://redstapler.co/javascript-realtime-chart-plotly/

/*************Functions for Plotting Data Points********************/
// load file
function makeplot(divName, filename) {
  // add random #s to csv name to prevent ajax caching
  Plotly.d3.csv(filename+"?"+(new Date()).getTime(), function(data){ processData(data, divName) } );

};

// extract column of data
function processData(allRows, divName) {
  y = [], projected = [], rec = [];

  for (var i=0; i<allRows.length; i++) {
    row = allRows[i];
    y.push( row['dollars'] );
    projected.push( row['projected'] );
    rec.push( row['rec'] );
  }
  makePlotly(y, projected, rec, divName);
}

// plot chart
function makePlotly(y, y2, y3, divName){
  var plotDiv = document.getElementById(divName);
  var traces = [{
    y: y,
    name: "spending"
  },
  {
    y: y2,
    name: "projected"
  },
  {
    y: y3,
    name: "recommended"
  }];
  if (cnt > 0) {
    // update existing traces efficiently
    Plotly.react(divName, traces, {title: divName});
  } else {
    // first time
    // create new plot with 3 traces 
    Plotly.newPlot(divName, traces, {title: divName});
  }
};

/*************Functions for Updating Graph********************/

function updateGraph(graph, filename) {
  // extend chart with new datapoints
  makeplot(graph, filename);
  cnt++;

  // Plotly.extendTraces(graph, { y: [[replot(graph, filename)]]}, [0]);
  // slide chart along with new data
  if(cnt > 20) {
      Plotly.relayout(graph,{
          xaxis: {
              range: [cnt-20,cnt] // redefine x-axis range
          }
      });
  }
}

/**********************JavaScript Program****************************/
// start loading data and plotting charts
makeplot('Dining Dollars', 'static/diningDollars.csv');
// makeplot('Swat Points', 'static/swatPoints.csv');

// automatically retrieve next data point
var cnt = 0;
setInterval(function(){
    // update all 3 lines
    updateGraph('Dining Dollars', 'static/diningDollars2.csv');
    // print("updating");
    // updateGraph('Swat Points', 'static/swatPoints2.csv');

},1000); // chart updating frequency
