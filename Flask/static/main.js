window.onload = function() {
    populateYearDropdown();   
};

function populateYearDropdown(){
    var yearDropdown = document.getElementById("year-dropdown");

    // Loop and add the Year values to DropDownList.
    for (var i = 2024; i <= 2050; i++) {
        var option = document.createElement("OPTION");
        option.innerHTML = i;
        option.value = i;
        yearDropdown.appendChild(option);
    }
}

// City autocomplete
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('city-input');
    const crimeDropdown = document.getElementById('crime-dropdown');

    input.addEventListener('input', async () => {
        const query = input.value;

        if (query.length < 2) {
            removeSuggestions();
            return;
        }

        try {
            const response = await fetch(`/autocomplete-cities?query=${encodeURIComponent(query)}`);
            const cities = await response.json();

            removeSuggestions();

            const suggestionList = document.createElement('ul');
            suggestionList.className = 'suggestions-list';

            // Append the suggestion list to the container
            const container = document.querySelector('.autocomplete-container');
            container.appendChild(suggestionList);

            cities.forEach(city => {
                const item = document.createElement('li');
                item.textContent = city;
                item.addEventListener('click', async () => {
                    input.value = city;
                    removeSuggestions();
                    await fetchCrimeTypes(city); // Fetch and populate crime types when city is selected
                });
                suggestionList.appendChild(item);
            });
        } catch (error) {
            console.error('Error fetching city suggestions:', error);
        }
    });

    async function fetchCrimeTypes(city) {
        try {
            const response = await fetch(`/crimes?city=${encodeURIComponent(city)}`);
            const crimes = await response.json();

            crimes.sort((a, b) => a.Crime.localeCompare(b.Crime));


            crimes.forEach(crime => {
                const option = document.createElement('option');
                option.value = crime.CrimeID;
                option.textContent = crime.Crime;
                crimeDropdown.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching crime types:', error);
        }
    }

    function removeSuggestions() {
        const suggestions = document.querySelector('.suggestions-list');
        if (suggestions) {
            suggestions.remove();
        }
    }
});

function validateForm() {
    // Get form elements and error spans
    const cityInput = document.getElementById('city-input');
    const crimeDropdown = document.getElementById('crime-dropdown');
    const yearDropdown = document.getElementById('year-dropdown');
    const cityError = document.getElementById('city-error');
    const crimeError = document.getElementById('crime-error');
    const yearError = document.getElementById('year-error');

    // Clear previous error messages
    cityError.textContent = '';
    crimeError.textContent = '';
    yearError.textContent = '';

    // Initialize a variable to track form validity
    let isValid = true;

    // Validate city input
    if (cityInput.value.trim() === '') {
      cityError.textContent = 'City is required.';
      isValid = false;
    }

    // Validate crime dropdown
    if (crimeDropdown.value === '') {
      crimeError.textContent = 'Crime type is required.';
      isValid = false;
    }

    // Validate year dropdown
    if (yearDropdown.value === '') {
      yearError.textContent = 'Year is required.';
      isValid = false;
    }

    // Submit the form if all fields are valid
    if (isValid) {
      document.getElementById('predictForm').submit();
    }
  }

  $(document).ready(function() {
    // Hide the error message when the user starts typing in the 'city' input
    $('#city-input').on('input', function() {
      $('#cityError').text('').hide();
    });

    // Hide the error message when the user selects a crime from the dropdown
    $('#crime-dropdown').on('change', function() {
      $('#crimeError').text('').hide();
    });

    // Hide the error message when the user selects a year from the dropdown
    $('#year-dropdown').on('change', function() {
      $('#yearError').text('').hide();
    });
  });
