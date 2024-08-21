document.addEventListener('DOMContentLoaded', () => {
    const countries = [
        'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua', 'Argentina', 'Armenia', 'Aruba', 'Australia',
        'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Benin', 'Bermuda', 'Bhutan',
        'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
        'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Cook Islands',
        'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador',
        'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon',
        'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
        'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica',
        'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
        'Liberia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Malawi', 'Maldives', 'Mexico',
        'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru',
        'Nepal', 'Netherlands', 'New Zealand', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palau',
        'Panama', 'Paraguay', 'Peru', 'Philippines', 'Palestine', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
        'Saint Kitts', 'Saint Lucia', 'Saint Vincent', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
        'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain',
        'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste',
        'Togo', 'Trinidad', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'Uruguay', 'United Kingdom', 'United States', 'Uzbekistan', 'Vanuatu', 'Venezuela',
        'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
    ];
  
    const sports = [
        'Aeronautics', 'Alpine Skiing', 'Alpinism', 'Art Competitions', 'Badminton', 'Baseball', 'Basketball', 'Biathlon',
        'Bobsleigh', 'Boxing', 'Canoeing', 'Cricket', 'Cross Country Skiing', 'Curling', 'Cycling', 'Diving', 'Equestrianism',
        'Fencing', 'Figure Skating', 'Football', 'Freestyle Skiing', 'Golf', 'Gymnastics', 'Handball', 'Hockey', 'Ice Hockey',
        'Judo', 'Jeu De Paume', 'Lacrosse', 'Luge', 'Modern Pentathlon', 'Motorboating', 'Nordic Combined', 'Polo', 'Racquets',
        'Roque', 'Rugby', 'Rugby Sevens', 'Sailing', 'Shooting', 'Skeleton', 'Snowboarding', 'Swimming', 'Synchronized Swimming', 'Table Tennis',
        'Taekwondo', 'Tennis', 'Timor-Leste', 'Trampolining', 'Triathlon', 'Tug-Of-War', 'Volleyball', 'Water Polo', 'Weightlifting',
        'Wrestling'
    ];
  
    let activeDropdown = null;
  
    function filterSuggestions(input, suggestions) {
      const value = input.value.toLowerCase();
      return suggestions.filter(suggestion => suggestion.toLowerCase().includes(value)).slice(0, 5); // Limit to 5 suggestions
    }
  
    function updateSuggestions(input, suggestionsElement, suggestions) {
      const matches = filterSuggestions(input, suggestions);
      suggestionsElement.innerHTML = matches.map(match => `<div class="suggestion-item">${match}</div>`).join('');
    }
  
    function setupAutocomplete(inputId, suggestionsId, suggestions) {
      const input = document.getElementById(inputId);
      const suggestionsElement = document.getElementById(suggestionsId);
  
      input.addEventListener('input', () => {
        if (input.value.trim() === '') {
          suggestionsElement.innerHTML = '';
        } else {
          updateSuggestions(input, suggestionsElement, suggestions);
        }
        // Ensure proper z-index management
        if (activeDropdown && activeDropdown !== suggestionsElement) {
          activeDropdown.style.zIndex = '10'; // Lower z-index of previous dropdown
        }
        suggestionsElement.style.zIndex = '20'; // Raise z-index of current dropdown
        activeDropdown = suggestionsElement; // Set active dropdown
      });
  
      document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !suggestionsElement.contains(e.target)) {
          suggestionsElement.innerHTML = '';
          suggestionsElement.style.zIndex = '10'; // Reset z-index when not active
          if (activeDropdown === suggestionsElement) {
            activeDropdown = null; // Clear active dropdown
          }
        }
      });
  
      suggestionsElement.addEventListener('click', (e) => {
        if (e.target.classList.contains('suggestion-item')) {
          input.value = e.target.textContent;
          suggestionsElement.innerHTML = '';
          suggestionsElement.style.zIndex = '10'; // Reset z-index after selection
          if (activeDropdown === suggestionsElement) {
            activeDropdown = null; // Clear active dropdown
          }
        }
      });
    }
  
    setupAutocomplete('country', 'country-suggestions', countries);
    setupAutocomplete('sport', 'sport-suggestions', sports);
  });
  