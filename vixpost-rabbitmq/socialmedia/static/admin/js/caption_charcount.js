function updateCharCount(textarea) {
    let max = textarea.getAttribute('maxlength');
    let currentLength = textarea.value.length;
    let remaining = max - currentLength;
    let counterId = textarea.id + '_counter';

    let counter = document.getElementById(counterId);

    if (!counter) {
        counter = document.createElement('div');
        counter.id = counterId;
        counter.style.fontWeight = 'bold';
        textarea.parentNode.appendChild(counter);
    }

    counter.textContent = remaining + " characters left";
    counter.style.color = remaining < 0 ? 'red' : 'green';
}

// Initialize counter on page load for all textareas with maxlength
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('textarea[maxlength]').forEach(textarea => {
        updateCharCount(textarea);
    });
});
