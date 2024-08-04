async function searchQuery() {
    var query = document.getElementById('search-bar').value;
    try {
        const response = await fetch('/.netlify/functions/query_database', {
            method: 'POST',
            body: JSON.stringify({ query: query }),
        });
        const data = await response.json();
        document.getElementById('results').innerHTML = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('results').innerHTML = 'An error occurred while processing your query.';
    }
}