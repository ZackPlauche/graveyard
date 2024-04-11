// UI Vars
const platformSelect = document.getElementById('platform-select');
const fieldSelect = document.getElementById('field-select');
const streamRows = document.querySelectorAll('#stream-table tbody tr');

// Data Vars
const query = new URLSearchParams(location.search);

// Search on select switch
platformSelect.addEventListener('change', function (e) {selectSearch(this, 'platform')});
fieldSelect.addEventListener('change', function (e) {selectSearch(this, 'field')});


function selectSearch(selectElement, parameter) {

  // If select value isn't blank
  if (selectElement.value != '') {

    // Create add search query 
    query.set(parameter, selectElement.value);
    location.search = query.toString();
  } else {
    // Delete query
    query.delete(parameter)
    location.search = query.toString();
  }
}