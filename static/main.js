// Src: https://plot.ly/javascript/ajax-call/

// load file
function makeplot(divName, filename) {
  Plotly.d3.csv(filename, function(data){ processData(data, divName) } );

};

// extract column of data
function processData(allRows, divName) {

  console.log(allRows);
  var y = [], projected = [], rec = [];

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

  Plotly.newPlot(divName, traces, {title: divName});
};

/*************Functions for Plotting New Data Points********************/

function updateGraph(graph, filename) {
  // extend chart with new datapoints
  Plotly.extendTraces(graph, { y: [[replot(graph, filename)]]}, [0]);
  // slide chart along with new data
  cnt++;
  // start sliding chart after 500 data points
  if(cnt > 500) {
      Plotly.relayout(graph,{
          xaxis: {
              range: [cnt-500,cnt] // redefine x-axis range
          }
      });
  }
}

// open up file
function replot(divName, filename) {
  Plotly.d3.csv(filename, function(data){ reprocessData(data, divName) } );

};

// read in column of data
function reprocessData(allRows, divName) {

  var y = [], projected = [], rec = [];

  for (var i=0; i<allRows.length; i++) {
    row = allRows[i];
    y.push( row['dollars'] );
    projected.push( row['projected'] );
    rec.push( row['rec'] );
  }
  makePlotly(y, projected, rec, divName);
}

/**********************JavaScript Program****************************/
// start loading data and plotting charts
makeplot('Dining Dollars', 'static/diningDollars.csv');
makeplot('Swat Points', 'static/swatPoints.csv');

// automatically retrieve next data point
var cnt = 0;
setInterval(function(){
    // update all 3 graphs
    updateGraph('Dining Dollars', 'static/diningDollars2.csv');
    updateGraph('Swat Points', 'static/swatPoints2.csv');

},3000); // chart updating frequency
