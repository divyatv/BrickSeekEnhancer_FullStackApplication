//process the results obtained from doughnut.py (the Flask application)
// Plot a default doughnut plot when the user has not entered any SKU
var ctx = document.getElementById("count-doughnut");
var myChart = new Chart(ctx, {
type: 'doughnut',
data: {
 labels: ['Divya', 'Harsha', 'Joe', 'Kevin', 'Ramesh'],
 datasets: [{
   label: '#Default Doughnut Plot',
   data: [25, 25, 25, 25, 25],
   backgroundColor: [
     'rgba(10, 99, 132, 1)',
     'rgba(54, 162, 235, 1)',
     'rgba(254, 204, 86, 1)',
     'rgba(75, 192, 192, 1)',
     'rgba(255, 0, 0, 1)'
   ],
   borderColor: [
     'rgba(100, 99, 132, 1)',
     'rgba(54, 23, 235, 1)',
     'rgba(254, 204, 86, 1)',
     'rgba(32, 192, 192, 1)',
     'rgba(99, 193, 193, 1)'
   ],
   borderWidth: 1
 }]
},
options: {
    cutoutPercentage: 60,
 responsive: true,
}
});
// Select the button
var button = d3.select("#filter-btn-stock");
// define a function to process the data and plot when the user enters an SKU and loads the page
function processInputsandPlot() {
  
  myChart.destroy();
     // define a variable url which pulls the value of the user entered sku dynamically
     var url = "/count/"+document.getElementById("sku").value
     d3.json(url).then(function(result) {
     console.log(result);
     // define two arrays to store data obtained from executing the sky in the .py file for plotting
     plot_labels = [];
     plot_data = [];
     result.forEach( x =>  {
        count = Object.entries(x)[0][1];
        status  = Object.entries(x)[1][1];
        plot_labels.push(status);
        plot_data.push(count);
       });
       var ctx = document.getElementById("count-doughnut");
       var myChart = new Chart(ctx, {
       type: 'doughnut',
       data: {
         labels: plot_labels,
         datasets: [{
           label: '#Item Stock Status',
           data : plot_data,
           backgroundColor: [
             'rgba(202, 45, 11, 1)',
             'rgba( 73, 202, 11, 1 )',
             'rgba( 11, 69, 202, 1)'
           ],
           borderColor: [
             'rgba(255,99,132,1)',
             'rgba(54, 162, 235, 1)',
             'rgba(255, 206, 86, 1)'
           ],
           borderWidth: 1
         }]
       },
       options: {
            cutoutPercentage: 60,
         responsive: true,
       }
     });
   });
};
// define the function call when the "Display Stock Status" button is clicked
button.on("click",processInputsandPlot);