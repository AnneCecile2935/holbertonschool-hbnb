import { getCookie } from './auth.js';  // Importer la fonction utilitaire pour récupérer les cookies
import { submitReview } from './review.js';  // importer la fonction de soumission

// Fonction pour extraire l'id du lieu depuis l'URL (ex: place.html?id=123)
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);  // Récupère les paramètres GET de l'URL
  return params.get('id');  // Retourne la valeur du paramètre 'id'
}

// Fonction asynchrone pour récupérer les détails du lieu via l'API avec authentification
export async function fetchPlaceDetails(token, placeId) {
  try {
    // Effectuer une requête fetch avec un header d'authentification Bearer
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: {
        'Authorization': `Bearer ${token}`  // Token JWT dans l'entête Authorization
      }
    });
    if (!response.ok) throw new Error('Failed to fetch place details');  // Gestion d'erreur si statut non OK
    return await response.json();  // Retourner les données JSON de la réponse
  } catch (error) {
    console.error(error);  // Loguer l'erreur en console
    return null;  // Retourner null en cas d'erreur
  }
}

// Fonction pour afficher les détails du lieu dans la page HTML
export function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');  // Sélecteur de l'élément conteneur des détails
  container.innerHTML = `
    <h2>${place.title}</h2>
    <p>${place.description}</p>
    <p><strong>Price:</strong> $${place.price}</p>
    <h4>Amenities:</h4>
    <ul>${place.amenities.map(a => `<li>${a.name}</li>`).join('')}</ul>  <!-- Liste des commodités -->
  `;

  // Sélecteur de la liste des reviews
  const reviewList = document.getElementById('review-list');
  // Si des reviews existent, les afficher, sinon message "No reviews yet."
  reviewList.innerHTML = place.reviews?.length
    ? place.reviews.map(r => `
      <li>
        <strong>${r.user?.first_name || "Unknown"}:</strong>
        <div class="star-rating" style="--rating: ${r.rating};"></div>
        <p>${r.text}</p>
      </li>
    `).join('')
  : '<li>No reviews yet.</li>';
}

// Événement déclenché quand le DOM est entièrement chargé
document.addEventListener('DOMContentLoaded', async () => {
  if (!window.location.pathname.endsWith('place.html')) return;
  const placeId = getPlaceIdFromURL();  // Récupérer l'id du lieu depuis l'URL
  const token = getCookie('token');  // Récupérer le token JWT depuis les cookies

  // Gestion affichage du formulaire d'ajout de review selon si utilisateur est connecté
  const addReviewSection = document.getElementById('add-review-section');
  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';  // Affiche ou cache la section selon présence du token
  }

  // Récupérer les détails du lieu depuis l'API
  const place = await fetchPlaceDetails(token, placeId);
  if (place) displayPlaceDetails(place);  // Si données reçues, les afficher
  if (token) {
    const form = document.getElementById('review-form');
    if (form) form.addEventListener('submit', async (event) => {
      // Appeler la fonction importée
       try {
    await submitReview(event); // ← appel sécurisé
    const updatedPlace = await fetchPlaceDetails(token, placeId);
    if (updatedPlace) displayPlaceDetails(updatedPlace);
  } catch (error) {
    console.error('Erreur lors de la soumission de la review ou du rechargement :', error);
    alert('Une erreur est survenue lors de l\'envoi de votre avis.');
  }
});
  }
});

