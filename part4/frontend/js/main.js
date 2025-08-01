// Importation des fonctions nécessaires depuis les différents modules
import { getToken, updateAuthButtons, setupLogoutButton } from './auth.js';  // Gestion de l'authentification (token)
import { fetchPlaces, displayPlaces } from './index.js';  // Fonction pour récupérer et afficher la liste des places
import { getPlaceIdFromURL } from './utils.js';  // Extraction de l'ID d'une place depuis l'URL
import { fetchPlaceDetails, displayPlaceDetails } from './place.js';  // Fonction pour récupérer et afficher les détails d'une place
import { setupLoginForm } from './login.js';
import { setupReviewForm, submitReview } from './review.js';
// Attendre que le DOM soit complètement chargé avant d'exécuter le script
document.addEventListener('DOMContentLoaded', () => {
  // Récupération du chemin actuel de la page (ex: "/index.html")
  const path = window.location.pathname;
  updateAuthButtons();
  setupLogoutButton();

  // Si on est sur la page index.html (liste des places)
  if (path === '/' || path.endsWith('index.html')) {
    const token = getToken();
    if (token) {
  	  fetchPlaces(token).then(places => {
    	const priceFilter = document.getElementById('price-filter');

    // Affichage initial de tous les lieux
    	displayPlaces(places);

    // Filtrage dynamique
      if (priceFilter) {
        priceFilter.addEventListener('change', () => {
          const selected = priceFilter.value;
          let filteredPlaces;

          if (selected === 'all') {
          filteredPlaces = places;
          } else {
          const maxPrice = parseInt(selected);
          filteredPlaces = places.filter(p => p.price <= maxPrice);
          }

          displayPlaces(filteredPlaces);
        });
      }
    });
} else {
    const messageDiv = document.getElementById('auth-message');
    const placesList = document.getElementById('places-list');

    if (messageDiv) {
      messageDiv.textContent = 'Vous devez être connecté pour accéder à la liste des lieux.';
      messageDiv.style.color = 'red';
      messageDiv.style.margin = '10px 0';
      messageDiv.style.display = 'block';
    }

    if (placesList) {
      placesList.style.display = 'none';
    }
  }
}
  // Si on est sur la page place.html (détail d'une place)
  else if (path.endsWith('place.html')) {
    const token = getToken();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
      alert('No place specified');
      return;
    }

    const addReviewSection = document.getElementById('add-review-section');
    if (addReviewSection) {
      addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (placeId) {
      fetchPlaceDetails(token, placeId).then(place => {
        if (place) displayPlaceDetails(place);
      });
    }

    if (token) {
      const form = document.getElementById('review-form');
      if (form) {
        form.addEventListener('submit', async (event) => {
          try {
            await submitReview(event);
            const updatedPlace = await fetchPlaceDetails(token, placeId);
            if (updatedPlace) displayPlaceDetails(updatedPlace);
          } catch (error) {
            console.error('Erreur lors de la soumission de la review ou du rechargement :', error);
            alert('Une erreur est survenue lors de l\'envoi de votre avis.');
          }
        });
      }
    }
  }
  // Si on est sur la page add_review.html (formulaire d'ajout d'avis)
  else if (path.endsWith('add_review.html')) {
    setupReviewForm();
  }
  // Si on est sur la page login.html (formulaire de connexion)
  else if (path.endsWith('login.html')) {
    setupLoginForm();
  }
});
