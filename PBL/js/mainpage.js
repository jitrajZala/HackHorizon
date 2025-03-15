let currentIndex = 0;
const images = document.querySelectorAll('.carousel-images img');
const totalImages = images.length;

function updateCarousel() {
    const offset = -currentIndex * 100;
    document.querySelector('.carousel-images').style.transform = `translateX(${offset}%)`;
}

// Event listeners for carousel buttons
document.querySelector('.next').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % totalImages;
    updateCarousel();
});

document.querySelector('.prev').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + totalImages) % totalImages;
    updateCarousel();
});
