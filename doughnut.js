var ctx = document.getElementById("count-doughnut");
var myChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Divya', 'Harsha', 'Joe', 'Kevin', 'Ramesh'],
    datasets: [{
      label: '#Stock Status',
      data: [25, 20, 20, 25, 10],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(80, 193, 193, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(80, 193, 193, 0.2)'
      ],
      borderWidth: 1
    }]
  },
  options: {
   	cutoutPercentage: 60,
    responsive: false,

  }
});




