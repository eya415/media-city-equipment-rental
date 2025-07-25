document.addEventListener('DOMContentLoaded', function () {
  const carousel = document.getElementById('carousel');
  const scrollAmount = 270; // Adjust based on card width + margin

  function scrollRight() {
    carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
  }

  function scrollLeft() {
    carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
  }

  // Make the functions available globally so HTML onClick works
  window.scrollRight = scrollRight;
  window.scrollLeft = scrollLeft;

  // Optional: Auto-scroll every 4s
  let autoScrollInterval;
  function startAutoScroll() {
    autoScrollInterval = setInterval(() => {
      if (carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth) {
        carousel.scrollTo({ left: 0, behavior: 'smooth' });
      } else {
        scrollRight();
      }
    }, 4000);
  }

  // Pause auto-scroll on hover
  carousel.addEventListener('mouseenter', () => clearInterval(autoScrollInterval));
  carousel.addEventListener('mouseleave', startAutoScroll);

  startAutoScroll();
});
