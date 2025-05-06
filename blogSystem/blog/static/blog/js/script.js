// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

// Scroll-to-top button functionality
let scrollButton = document.createElement('button');
scrollButton.textContent = "↑";
scrollButton.classList.add('scroll-to-top-btn'); // Add custom styles

document.body.appendChild(scrollButton);

// Show the scroll button when scrolling down
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollButton.style.display = 'block';
    } else {
        scrollButton.style.display = 'none';
    }
});

// Scroll to the top when the button is clicked
scrollButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
