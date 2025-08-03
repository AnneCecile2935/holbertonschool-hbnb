// Importation des fonctions nécessaires depuis les différents modules
import { getToken, updateAuthButtons, setupLogoutButton } from './auth.js';
// Gestion de l'authentification (token)
import { fetchPlaces, displayPlaces } from './index.js';
// Fonction pour récupérer et afficher la liste des places
import { getPlaceIdFromURL } from './utils.js';
// Extraction de l'ID d'une place depuis l'URL
import { fetchPlaceDetails, displayPlaceDetails } from './place.js';
// Fonction pour récupérer et afficher les détails d'une place
import { setupLoginForm } from './login.js';
import { setupReviewForm, submitReview } from './review.js';


// Attendre que le DOM soit complètement chargé avant d'exécuter le script
document.addEventListener('DOMContentLoaded', () => {
  // Récupération du chemin actuel de la page (ex: "/index.html")
  const path = window.location.pathname;

  // Met à jour l'affichage des boutons en fonction de l'état de connexion
  updateAuthButtons();
  setupLogoutButton();

  // === PAGE D'ACCUEIL : Liste des lieux (index.html) ===
  if (path === '/' || path.endsWith('index.html')) {
    const token = getToken();

    if (token) {
	  // Récupère tous les lieux depuis l'API, puis les affiche
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

          // Mise à jour de l'affichage après filtrage
          displayPlaces(filteredPlaces);
        });
      }
    });
} else {
    // Si l'utilisateur n'est pas connecté, afficher un message d'alerte
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
  // === PAGE DE DÉTAIL D'UN LIEU (place.html) ===
  else if (path.endsWith('place.html')) {
    const token = getToken();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
      alert('No place specified');
      return;
    }

    // Affiche ou masque la section "ajouter un avis" en fonction de l'authentification
    const addReviewSection = document.getElementById('add-review-section');
    if (addReviewSection) {
      addReviewSection.style.display = token ? 'block' : 'none';
    }

    // Récupère et affiche les détails du lieu
    if (placeId) {
      fetchPlaceDetails(token, placeId).then(place => {
        if (place) displayPlaceDetails(place);
      });
    }

    // Si l'utilisateur est connecté, on initialise le formulaire d'avis
    if (token) {
       setupReviewForm();
    }
  }
  // === PAGE D'AJOUT D'AVIS (add_review.html) ===
  else if (path.endsWith('add_review.html')) {
    setupReviewForm();
  }
  // === PAGE DE CONNEXION (login.html) ===
  else if (path.endsWith('login.html')) {
    setupLoginForm();
  }
});
