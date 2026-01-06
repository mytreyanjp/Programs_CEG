document.getElementById('searchInput').addEventListener('input', function() {
    const query = this.value.trim();

    if (query.length >= 3) {
        // Construct the OMDB API URL with the search query
        const apiUrl = `http://www.omdbapi.com/?s=${query}&apikey=b8476fc9`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const resultsList = document.getElementById('resultsList');
                resultsList.innerHTML = ''; // Clear previous results

                // Check if the response contains Search results
                if (data.Response === "True") {
                    data.Search.forEach(item => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <strong>${item.Title}</strong> (${item.Year})
                            <img src="${item.Poster}" alt="${item.Title}" style="width: 50px; height: 75px; margin-left: 10px;" />
                        `;
                        resultsList.appendChild(li);
                    });
                } else {
                    resultsList.innerHTML = '<li>No results found.</li>';
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    } else {
        document.getElementById('resultsList').innerHTML = ''; // Clear results if input is too short
    }
});

