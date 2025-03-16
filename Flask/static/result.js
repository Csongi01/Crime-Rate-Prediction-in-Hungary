document.addEventListener("DOMContentLoaded", function() {
    
// Fetch the data from the document
const crimeRate = parseFloat(document.getElementById('crime_rate').value); 
const crimeRatePlus = parseFloat(document.getElementById('crime_rate_plus').value); 
const crimeRateMinus = parseFloat(document.getElementById('crime_rate_minus').value); 

// Current year
const currentYear = parseInt(document.getElementById('year').innerText); 

// Prepare the data for the chart
const labels = [currentYear - 5, currentYear, currentYear + 5];
const data = [crimeRateMinus, crimeRate, crimeRatePlus];

// Setup the chart
const ctx = document.getElementById('crimeRateChart').getContext('2d');
const crimeRateChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Crime Rate',
            data: data,
            borderColor: 'rgba(255, 99, 132, 1)',  
            backgroundColor: 'rgba(255, 99, 132, 0.2)', 
            fill: true,
            tension: 0.4,  
            pointRadius: 5,  
            pointBackgroundColor: 'rgba(255, 99, 132, 1)',  
            pointBorderColor: '#fff',  
            pointBorderWidth: 2 
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    color: 'rgba(75, 192, 192, 1)'
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y.toFixed(2);
                        }
                        return label;
                    }
                },
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                titleColor: '#fff',
                bodyColor: '#fff'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Year',
                    color: '#333',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)' 
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Crime Rate',
                    color: '#333',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)' 
                },
                ticks: {
                    beginAtZero: true
                }
            }
        }
    }
});

 

    // Get the city name from the 'city' element
    const cityElement = document.getElementById('city');
    const city = cityElement.innerText;

    
    
    // Fetch latitude and longitude from OpenCage Geocoding API
    fetch(`https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(city)}&key=2edc29426f9f4f4ea1d604bd1f76690f`)
        .then(response => response.json())
        .then(data => {
            const location = data.results[0].geometry;
            const lat = location.lat;
            const lng = location.lng;

            // Initialize the map
            const map = L.map('map').setView([lat, lng], 12);

            // Add OpenStreetMap tiles
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Add a marker for the city
            L.marker([lat, lng]).addTo(map)
                .bindPopup(city)
                .openPopup();
        })
        .catch(error => console.error('Error fetching coordinates:', error));
});