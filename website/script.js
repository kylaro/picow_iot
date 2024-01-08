let chartInstance;

document.addEventListener("DOMContentLoaded", function() {
    fetchCurrentCO2();
    fetchDataAndRenderChart('1 hour');
});

function fetchCurrentCO2() {
    const url = `https://0wc4ksyc6a.execute-api.eu-west-3.amazonaws.com/GetCurrentCO2`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Assuming the Lambda function returns a string "device off" or an object with "averageCO2"
            const co2Text = typeof data === 'string' ? data : `Current CO2: ${data.averageCO2} ppm`;
            
            // Update the h2 element
            const co2Element = document.getElementById('currentCO2');
            co2Element.innerHTML = co2Text;
        })
        .catch(error => {
            console.error('Error fetching current CO2:', error);
            // Update the h2 element in case of an error
            const co2Element = document.getElementById('currentCO2');
            co2Element.innerHTML = 'Error fetching data';
        });
}



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
    //hide spinner

}

function renderChart(data) {
    const ctx = document.getElementById('environmentChart').getContext('2d');
    const timestamps = data.map(item => item.timestamp);//data.map(item => new Date(item.timestamp).toLocaleTimeString());
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
                    pointHitRadius: 7,
                    pointRadius: 1,      // Smaller value for smaller points
                    borderWidth: 1       // Smaller value for thinner line
                },
                {
                    label: 'Humidity (%)',
                    data: humidities,
                    borderColor: 'rgba(40, 167, 69, 1)',
                    backgroundColor: 'rgba(40, 167, 69, 0.5)',
                    yAxisID: 'yHumidity', // Corrected yAxisID
                    pointHitRadius: 7,
                    pointRadius: 1,      // Smaller value for smaller points
                    borderWidth: 1       // Smaller value for thinner line
                },
                {
                    label: 'CO2 (ppm)',
                    data: co2Levels,
                    borderColor: 'rgba(220, 53, 69, 1)',
                    backgroundColor: 'rgba(220, 53, 69, 0.5)',
                    yAxisID: 'yCo2', // Corrected yAxisID
                    pointHitRadius: 7,
                    pointRadius: 1,      // Smaller value for smaller points
                    borderWidth: 1       // Smaller value for thinner line
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


function updateCountdown() {
    const countdownElement = document.getElementById('countdown');
    const targetDate = new Date(Date.UTC(2024, 3, 7, 20, 55, 0)); // April 7th, 2024 at 20:55 UTC
    const now = new Date(); // User's local time
    const difference = targetDate - now;

    if (difference <= 0) {
        countdownElement.innerHTML = 'Countdown to April 7th, 2024: Time is up!';
        clearInterval(countdownInterval);
        return;
    }

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    const timeZoneString = Intl.DateTimeFormat().resolvedOptions().timeZone;
    countdownElement.innerHTML = `${days} days ${hours}h ${minutes}m ${seconds}s`;
}

const countdownInterval = setInterval(updateCountdown, 1000);
