var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Divya', 'Harsha', 'Joe', 'Kevin', 'Ramesh'],
    datasets: [{
      label: '#Stock Status',
      data: [20, 20, 20, 20, 20],
      backgroundColor: [
        'rgba(182, 15, 15, 1)',
        'rgba(194, 98, 1, 1)',
        'rgba(84, 291, 213, 1)',
        'rgba(84, 132, 231, 1)',
        'rgba(80, 193, 5, 1)'
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