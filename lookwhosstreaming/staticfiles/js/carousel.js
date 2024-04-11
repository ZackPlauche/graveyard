// UI Variables
const dateCarousel = document.getElementById('date-carousel');
const liveCarousel = document.getElementById('live-list-carousel');
// const leftArrow = document.getElementById('left-arrow');
// const rightArrow = document.getElementById('right-arrow');


// Start carousel with center number link in center
dateCarousel.scrollLeft = 450;

addCarouselScrolling(dateCarousel, 150);
if (liveCarousel) {
  addCarouselScrolling(liveCarousel, 100);
}




function addCarouselScrolling(carousel, itemWidth, maxScrollWidth = null) {

  // Carousel Arrow Vars
  const leftArrow = carousel.parentElement.querySelector('.left-arrow');
  const rightArrow = carousel.parentElement.querySelector('.right-arrow');

  // Set Carousel max scroll width
  if (maxScrollWidth == null) {
    maxScrollWidth = carousel.scrollWidth;
  };

  // Check To Enable / Disable arrows on scroll
  carousel.onscroll = function (e) {
    checkToEnable(carousel, rightArrow, leftArrow, maxScrollWidth);
    checkToEnable(carousel, leftArrow, rightArrow, maxScrollWidth);
    checkToDisable(carousel, leftArrow, maxScrollWidth);
    checkToDisable(carousel, rightArrow, maxScrollWidth);
  }

  // Left arrow functionality
  leftArrow.onclick = function (e) {
    checkToEnable(carousel, this, rightArrow, maxScrollWidth);
    scrollCarousel(carousel, this, itemWidth);
    checkToDisable(carousel, this, maxScrollWidth);
  };

  // Right arrow functionality
  rightArrow.onclick = function (e) {
    console.log(this);
    checkToEnable(carousel, this, leftArrow, maxScrollWidth);
    scrollCarousel(carousel, this, itemWidth);
    checkToDisable(carousel, this, maxScrollWidth);
  };
};

function scrollCarousel(carousel, arrow, itemWidth) {
  if (!arrow.classList.contains('disabled')) {

    // Scroll left if left arrow
    if (arrow.classList.contains('left-arrow')) {
      carousel.scrollLeft -= itemWidth;

      // Scroll right if right arrow
    } else if (arrow.classList.contains('right-arrow')) {
      carousel.scrollLeft += itemWidth;
    }
  }

};

function checkToEnable(carousel, arrow, otherArrow, maxScrollWidth) {

  const maxScroll = calculateMaxScroll(carousel, maxScrollWidth);

  // Turn on left arrow if carousel is at the beginning
  if (arrow.classList.contains('right-arrow')) {
    if (carousel.scrollLeft >= 0) {
      otherArrow.classList.remove('disabled');
    }

    // Turn on right arrow if carousel is at max scroll
  } else if (arrow.classList.contains('left-arrow')) {
    if (Math.ceil(carousel.scrollLeft) <= maxScroll) {
      otherArrow.classList.remove('disabled');
    }
  }
}

function checkToDisable(carousel, arrow, maxScrollWidth) {
  const maxScroll = calculateMaxScroll(carousel, maxScrollWidth)

  // Turn off left arrow if carousel is at the beginning
  if (arrow.classList.contains('left-arrow')) {
    if (carousel.scrollLeft == 0) {
      arrow.classList.add('disabled');
    }

    // Turn off right arrow if carousel is at the maxScroll
  } else if (arrow.classList.contains('right-arrow')) {
    if (Math.ceil(carousel.scrollLeft) >= maxScroll) {
      arrow.classList.add('disabled');
    }
  }
}

// Calculate stupid max scroll width out of necessity
function calculateMaxScroll(carousel, maxScrollWidth) {
  const maxScroll = maxScrollWidth - carousel.clientWidth;
  return maxScroll;
};