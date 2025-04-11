document.getElementById('form').addEventListener("submit", function(event) {
    let word = document.getElementById('text').value.trim();
    let file = document.getElementById('document').files[0];

    if (!word || !file) {
        event.preventDefault();
        alert('Input data in all fields');
    }
})