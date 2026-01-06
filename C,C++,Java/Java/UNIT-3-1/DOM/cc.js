// Get the display element
const display = document.getElementById('display');

// Append numbers and operators to the display
function appendToDisplay(value) {
    display.value += value;
}

// Clear the display
function clearDisplay() {
    display.value = '';
}

// Calculate the result of the expression
function calculateResult() {
    try {
        // Use the JavaScript eval() function to evaluate the expression
        display.value = eval(display.value);
    } catch (error) {
        // If there's an error (e.g., invalid expression), show an error message
        display.value = 'Error';
    }
}
