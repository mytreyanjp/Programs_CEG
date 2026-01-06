
function displayProducts() {
    fetch('products.json')
        .then(response => response.json()) 
        .then(products => {
            const tableBody = document.querySelector('#productTable tbody');
            tableBody.innerHTML = '';
            products.forEach(product => {
                const row = document.createElement('tr');  
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>$${product.price.toFixed(2)}</td>
                    <td>${product.description}</td>
                `;
                tableBody.appendChild(row);  
            });
        })
        .catch(error => {
            console.error('Error fetching product data:', error);
        });
}
window.onload = displayProducts;
