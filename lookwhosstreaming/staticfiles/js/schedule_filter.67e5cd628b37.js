// UI Variables
const platforms = document.querySelectorAll('.platforms a');
const categories = document.querySelectorAll('.categories a');
const dates = document.querySelectorAll('.dates a');
const times = document.querySelectorAll('.time-range a');

// Data Vars
var query = new URLSearchParams(location.search);

// Add query filtering to different filter options
applyFilter(platforms, 'platform', true);
applyFilter(categories, 'category', true);
applyFilter(dates, 'date');
applyFilter(times, 'time');

// FUNCTIONS
function applyFilter(elementList, parameterName, exclusive=false) {

  // Iterate through list of elements
  elementList.forEach(function (element) {

    // Store data target value into a variable
    const data = element.dataset.target;

    // Query for platform on element click
    element.addEventListener('click', function (e) {
      elementSearch(this, parameterName, exclusive);
    });

    // Set queried platform is active
    if (location.search.includes(data)) {
      element.classList.add('active');
    }
  })
};

function elementSearch(element, parameterName, exclusive=false) {

  // Pull data from element and create a search parameter
  const parameterValue = element.dataset.target;

  if (query.get(parameterName) === parameterValue || parameterValue === "") {
    query.delete(parameterName);
  } else if (exclusive === true) {
    query = new URLSearchParams();
    query.set(parameterName, parameterValue)
  } else {
    query.set(parameterName, parameterValue)
  }

  location.search = query.toString();
}