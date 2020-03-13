// function getData() {
//     let spending = [], vals = [];
//     d3.csv('testData.csv', function(d) {
//       spending.push(Number(d.dollars));
//       return {
//         spent: Number(d.dollars.trim())
//       }
//     }).then(function(d) {
//       vals = spending.spent;
//       makePlotly(vals);
//     })
// }
//
// function makePlotly(vals) {
//   console.log(vals);
//   // create line chart
//   Plotly.plot('chart',[{
//       y: vals, // pass array
//       type:'line'
//   }]);
//
// }
// getData();

function makeplot() {
  Plotly.d3.csv("testData.csv", function(data){ processData(data) } );

};

function processData(allRows) {

  console.log(allRows);
  var y = [];

  for (var i=0; i<allRows.length; i++) {
    row = allRows[i];
    y.push( row['dollars'] );
  }
  console.log('Y',y);
  makePlotly(y);
}

function makePlotly(y){
  var plotDiv = document.getElementById("chart");
  var traces = [{
    y: y
  }];

  Plotly.newPlot('myDiv', traces,
    {title: 'Plotting CSV data from AJAX call'});
};
  makeplot();

function replot() {
  Plotly.d3.csv("testData.csv", function(data){ reprocessData(data) } );

};

function reprocessData(allRows) {

  var y = [];

  for (var i=0; i<allRows.length; i++) {
    row = allRows[i];
    y.push( row['dollars'] );
  }
  return y;
}

// automatically retrieve next data point
var cnt = 0;
setInterval(function(){
    let newY = [];
    newY = replot();
    // extend chart with new datapoints
    Plotly.extendTraces('myDiv',{ y:[[newY]]}, [0]);
    // slide chart along with new data
    cnt++;
    // start sliding chart after 500 data points
    if(cnt > 500) {
        Plotly.relayout('myDiv',{
            xaxis: {
                range: [cnt-500,cnt] // redefine x-axis range
            }
        });
    }
},1500); // chart updating frequency
