// CAROUSEL

// UI Variables
const carousel = document.getElementById('date-carousel');
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');

// Start carousel with center number link in center
console.log(carousel.scrollWidth);
console.log(carousel.scrollLeft);
carousel.scrollLeft = 450;

leftArrow.onclick = function (e) {
  // Display current scroll
  console.log(carousel.scrollLeft);
  if (carousel.scrollLeft > 896) {
    rightArrow.firstChild.className = '';
  }

  carousel.scrollLeft -= 150;
  console.log(carousel.scrollLeft);
  // Add class disabled if carousel is all the way left
  if (carousel.scrollLeft == 0) {
    leftArrow.firstChild.className = 'disabled';
  }
  
};

rightArrow.onclick = function (e) {
  console.log(carousel.scrollLeft);

  if (carousel.scrollLeft == 0) {
    leftArrow.firstChild.className = '';
  }

  carousel.scrollLeft += 150;
  console.log(carousel.scrollLeft);

  // Add class disabled if carousel is all the way right
  if (carousel.scrollLeft > 896) {
    rightArrow.firstChild.className = 'disabled';
  }
};


// Dynamically list avaialble livestreams for the selected day