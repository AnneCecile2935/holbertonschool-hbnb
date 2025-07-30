// Importation des fonctions nécessaires depuis les différents modules
import { getToken, deleteToken, isAuthenticated } from './auth.js';  // Gestion de l'authentification (token)
import { fetchPlaces } from './index.js';  // Fonction pour récupérer et afficher la liste des places
import { getPlaceIdFromURL } from './utils.js';  // Extraction de l'ID d'une place depuis l'URL
import { fetchPlaceDetails } from './place.js';  // Fonction pour récupérer et afficher les détails d'une place
import { setupLoginForm } from './login.js';
import { updateAuthButtons, setupLogoutButton } from './auth.js';
import { setupReviewForm } from './review.js';
// Attendre que le DOM soit complètement chargé avant d'exécuter le script
document.addEventListener('DOMContentLoaded', () => {
  // Récupération du chemin actuel de la page (ex: "/index.html")
  updateAuthButtons();
  setupLogoutButton();
  const path = window.location.pathname;


  // Si on est sur la page index.html (liste des places)
  if (path === '/' || path.endsWith('index.html')) {
    const token = getToken();  // Récupérer le token d'authentification
    if (token) fetchPlaces(token);  // Appeler la fonction pour charger et afficher les places avec le token
  }

  // Si on est sur la page place.html (détail d'une place)
  if (path.endsWith('place.html')) {
    const token = getToken();  // Récupérer le token d'authentification (peut être null si pas connecté)
    const placeId = getPlaceIdFromURL();  // Extraire l'ID de la place depuis les paramètres URL
    if (placeId) fetchPlaceDetails(token, placeId);  // Charger les détails de la place (avec token si connecté)
  }

  // Si on est sur la page add_review.html (formulaire d'ajout d'avis)
  if (path.endsWith('add_review.html')) {
    setupReviewForm();  // Initialiser la gestion du formulaire d'ajout d'avis (validation, envoi, etc.)
  }

  // Si on est sur la page login.html (formulaire de connexion)
  if (path.endsWith('login.html')) {
    setupLoginForm();  // Initialiser la gestion du formulaire de connexion (non défini dans ce snippet)
  }
});
