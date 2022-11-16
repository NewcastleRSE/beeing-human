function highlightErrorToggle(errorId) {
    const error = document.getElementById(errorId.toString())
    if (error.classList.contains('active')) {
        error.classList.remove('active');
    } else {
        error.classList.add("active");
        error.scrollIntoView();
    }
}

function transferEditedText() {
    const text = document.getElementById('text').textContent
    document.getElementById('text-form').textContent = text
}