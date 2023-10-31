document.addEventListener("DOMContentLoaded", function() {
    fetchDataAndRenderCharts();
});

function fetchDataAndRenderCharts() {
    fetch('https://0wc4ksyc6a.execute-api.eu-west-3.amazonaws.com/RetrieveData') // Replace with your API Gateway URL
        .then(response => response.json())
        .then(data => {
            renderChart(data, 'temperatureChart','temperature', 'Temperature (C)', 'rgba(0, 123, 255, 0.5)', 'rgba(0, 123, 255, 1)');
            renderChart(data, 'humidityChart', 'humidity', 'Humidity (%)', 'rgba(40, 167, 69, 0.5)', 'rgba(40, 167, 69, 1)');
            renderChart(data, 'co2Chart','co2', 'CO2 (ppm)', 'rgba(220, 53, 69, 0.5)', 'rgba(220, 53, 69, 1)');
        })
        .catch(error => console.error('Error fetching data:', error));
}

function renderChart(data, canvasId, key, label, backgroundColor, borderColor) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const timestamps = data.map(item => item.timestamp);
    const values = data.map(item => item[key]);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [{
                label: label,
                data: values,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
