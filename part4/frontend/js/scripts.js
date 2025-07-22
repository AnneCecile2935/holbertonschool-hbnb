let allPlaces = [];

function checkAuthentication() {
      const token = getCookie('access_token');
      const loginLink = document.getElementById('login-button');

      if (!token) {
          loginLink.style.display = 'block';
      } else {
          loginLink.style.display = 'none';
          // Fetch places data if the user is authenticated
          fetchPlaces(token);
      }
  }
function getCookie(name) {
  const cookies = document.cookie.split(';'); // découpe tous les cookies
  for (let cookie of cookies) {
    cookie = cookie.trim(); // enlève les espaces autour
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1); // récupère la valeur après 'name='
    }
  }
  return null; // si cookie non trouvé
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';  // Vide la liste avant de la remplir

  if (!places || places.length === 0) {
      placesList.innerHTML = '<p>No places to display.</p>';
      return;
  }

  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.classList.add('place-card');
    placeCard.dataset.price = place.price;

    placeCard.innerHTML = `
      <h2>${place.title}</h2>
      <p>Price per night: $${place.price}</p>
      <p>${place.description}</p>
      <button class="details-button">View Details</button>
    `;

    placesList.appendChild(placeCard);
  });
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/places/', {
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + token },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // 💡 ajoute ceci :
    allPlaces = data;

    displayPlaces(allPlaces);
  } catch (error) {
    console.log('Erreur lors de la récupération des places:', error);
  }
}
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');

    priceFilter.addEventListener('change', () => {
        const maxPrice = priceFilter.value ? parseFloat(priceFilter.value) : null;

        if (!maxPrice) {
            // Affiche toutes les places si "All" ou valeur vide sélectionnée
            displayPlaces(allPlaces);
            return;
        }

        // Filtre la liste globale et affiche uniquement les places <= maxPrice
        const filteredPlaces = allPlaces.filter(place => place.price <= maxPrice);
        displayPlaces(filteredPlaces);
    });
}
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  setupPriceFilter(); // 💡 ajoute ça
});
