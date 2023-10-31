let chartInstance;

document.addEventListener("DOMContentLoaded", function() {
    fetchDataAndRenderChart('1 day');
});

function fetchDataAndRenderChart(timeRange) {
    const url = `https://0wc4ksyc6a.execute-api.eu-west-3.amazonaws.com/RetrieveData?range=${timeRange}`;

    // change time-range header to reflect new timeRange
    const timeRangeElement = document.getElementById('time-range');
    timeRangeElement.innerHTML = `Time range = ${timeRange}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (chartInstance) {
                chartInstance.destroy();
            }
            renderChart(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function renderChart(data) {
    const ctx = document.getElementById('environmentChart').getContext('2d');
    const timestamps = data.map(item => new Date(item.timestamp).toLocaleTimeString());
    const temperatures = data.map(item => item.temperature);
    const humidities = data.map(item => item.humidity);
    const co2Levels = data.map(item => item.co2);

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            
            datasets: [
                {
                    label: 'Temperature (C)',
                    data: temperatures,
                    borderColor: 'rgba(0, 123, 255, 1)',
                    backgroundColor: 'rgba(0, 123, 255, 0.5)',
                    yAxisID: 'yTemperature', // Corrected yAxisID
                    pointHitRadius: 10,
                },
                {
                    label: 'Humidity (%)',
                    data: humidities,
                    borderColor: 'rgba(40, 167, 69, 1)',
                    backgroundColor: 'rgba(40, 167, 69, 0.5)',
                    yAxisID: 'yHumidity', // Corrected yAxisID
                    pointHitRadius: 10,
                },
                {
                    label: 'CO2 (ppm)',
                    data: co2Levels,
                    borderColor: 'rgba(220, 53, 69, 1)',
                    backgroundColor: 'rgba(220, 53, 69, 0.5)',
                    yAxisID: 'yCo2', // Corrected yAxisID
                    pointHitRadius: 10,
                }
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            tooltips: {
                mode: 'index',
                intersect: false
            },        
            scales: {
                yTemperature: {
                    position: 'right',
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Temperature (C)'
                    }
                },
                yHumidity: {
                    position: 'left',  // Changed position for Humidity to 'right'
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    }
                },
                yCo2: {
                    position: 'right',
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'CO2 (ppm)'
                    },
                    offset: true
                }
            }
        }        
    });
}
