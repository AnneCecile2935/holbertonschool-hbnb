import { getCookie } from './auth.js';
import { fetchPlaceDetails as fetchPlaceDetailsFromAPI, displayPlaceDetails as showPlace } from './place.js';
import { submitReview } from './review.js'; // utile seulement si tu veux forcer un refresh après le submit, sinon peut être retiré

// Fonction pour extraire l'ID du lieu depuis l'URL
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// Fonction asynchrone pour récupérer les détails du lieu via l'API avec authentification
export async function fetchPlaceDetails(token, placeId) {
  if (!placeId) {
    console.error('Place ID is undefined');
    return null;
  }

  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching place details:', error);
    return null;
  }
}

// Fonction pour afficher les détails du lieu dans la page HTML
export function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) {
    console.error('Element with ID "place-details" not found.');
    return;
  }

  container.innerHTML = `
    <h2>${place.title}</h2>
    <p>${place.description}</p>
    <p><strong>Prix:</strong> ${place.price}€</p>
    <h4>Equipements:</h4>
    <ul>${place.amenities.map(a => `<li>${a.name}</li>`).join('')}</ul>
    <a href="update_place.html?id=${place.id}" class="edit-button">Modifier</a>
  `;

  const reviewList = document.getElementById('review-list');
  if (!reviewList) {
    console.error('Element with ID "review-list" not found.');
    return;
  }

  reviewList.innerHTML = place.reviews?.length
    ? place.reviews.map(r => `
      <li class="review-card">
        <p class="review-user">${r.user?.first_name || "Anonyme"}</p>
         <div class="review-rating">${r.rating}/5</div>
        <p class="review-text">${r.text}</p>
      </li>
    `).join('')
    : '<li>No review for this place.</li>';
}

// Initialisation de la page (à faire uniquement si on est sur place.html)
document.addEventListener('DOMContentLoaded', async () => {
  if (!window.location.pathname.endsWith('place.html')) return;

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    console.error('No place ID provided in the URL.');
    return;
  }

  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review-section');
  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
  }

  const place = await fetchPlaceDetails(token, placeId);
  if (place) {
    displayPlaceDetails(place);
  } else {
    console.error('Failed to load place details.');
  }

});
