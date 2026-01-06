// Function to load XML file and parse it
function loadWeatherData(callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'weather.xml', true);  // Open the file
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const xml = xhr.responseText;
            callback(xml);  // Call the callback function with the XML data
        }
    };
    xhr.send();  // Send the request
}

// Function to parse the XML and get the weather details for a city
function displayWeatherData(cityName) {
    loadWeatherData(function (xml) {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xml, 'application/xml');

        // Find the city in the XML by name
        const city = xmlDoc.querySelector(`city[name="${cityName}"]`);

        if (city) {
            const temperature = city.querySelector('temperature').textContent;
            const humidity = city.querySelector('humidity').textContent;
            const condition = city.querySelector('condition').textContent;
            const unit = city.querySelector('temperature').getAttribute('unit');

            // Update the weather details in the HTML
            const weatherDetails = document.getElementById('weatherDetails');
            weatherDetails.innerHTML = `
                <h2>Weather in ${cityName}</h2>
                <p>Temperature: ${temperature}° ${unit}</p>
                <p>Humidity: ${humidity}%</p>
                <p>Condition: ${condition}</p>
            `;
        } else {
            // If city not found in XML
            document.getElementById('weatherDetails').innerHTML = `<p>Weather data not available for ${cityName}.</p>`;
        }
    });
}

// Event listener for when a city is selected from the dropdown
document.getElementById('citySelect').addEventListener('change', function () {
    const selectedCity = this.value;
    displayWeatherData(selectedCity);
});

// Initial display for the default selected city
displayWeatherData(document.getElementById('citySelect').value);
