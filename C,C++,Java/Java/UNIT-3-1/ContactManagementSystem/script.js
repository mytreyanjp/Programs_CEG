// Function to load contacts from localStorage and display them
function loadContacts() {
    const contacts = JSON.parse(localStorage.getItem('contacts')) || [];
    const contactList = document.getElementById('contactList');
    contactList.innerHTML = ''; // Clear existing list

    contacts.forEach(contact => {
        const li = document.createElement('li');
        li.className = 'contact-item';
        li.innerHTML = `
            <strong>${contact.name}</strong><br>
            Email: ${contact.email}<br>
            Phone: ${contact.phone}
            <button class="delete" onclick="deleteContact('${contact.name}')">Delete</button>
        `;
        contactList.appendChild(li);
    });
}

// Function to add a new contact
document.getElementById('contactForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent form submission (page reload)

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;

    const newContact = { name, email, phone };

    // Retrieve contacts from localStorage, or initialize empty array if none exist
    let contacts = JSON.parse(localStorage.getItem('contacts')) || [];

    // Add new contact
    contacts.push(newContact);

    // Save updated list back to localStorage
    localStorage.setItem('contacts', JSON.stringify(contacts));

    // Reset form and reload contacts
    document.getElementById('contactForm').reset();
    loadContacts();
});

// Function to delete a contact
function deleteContact(contactName) {
    // Retrieve contacts from localStorage
    let contacts = JSON.parse(localStorage.getItem('contacts')) || [];

    // Remove the contact that matches the name
    contacts = contacts.filter(contact => contact.name !== contactName);

    // Save updated list back to localStorage
    localStorage.setItem('contacts', JSON.stringify(contacts));

    // Reload contacts after deletion
    loadContacts();
}

// Function to search contacts based on user input
function searchContacts() {
    const searchQuery = document.getElementById('searchInput').value.toLowerCase();
    const contacts = JSON.parse(localStorage.getItem('contacts')) || [];
    const contactList = document.getElementById('contactList');
    contactList.innerHTML = '';

    contacts.filter(contact => {
        return contact.name.toLowerCase().includes(searchQuery) || 
               contact.email.toLowerCase().includes(searchQuery) || 
               contact.phone.includes(searchQuery);
    }).forEach(contact => {
        const li = document.createElement('li');
        li.className = 'contact-item';
        li.innerHTML = `
            <strong>${contact.name}</strong><br>
            Email: ${contact.email}<br>
            Phone: ${contact.phone}
            <button class="delete" onclick="deleteContact('${contact.name}')">Delete</button>
        `;
        contactList.appendChild(li);
    });
}

// Load contacts initially when the page loads
window.onload = loadContacts;
