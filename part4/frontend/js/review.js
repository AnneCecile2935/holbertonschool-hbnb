import { getCookie } from './auth.js';
import { parseJwt } from './utils.js';


// === UTILITAIRE ===

// Fonction pour extraire l'ID d'un lieu depuis l'URL (ex: ?id=123)
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// === INITIALISATION DU FORMULAIRE D'AVIS ===

// Fonction qui ajoute un listener au formulaire d’avis (si présent)
// Elle évite d'ajouter plusieurs fois le même listener
export function setupReviewForm() {
  const form = document.getElementById('review-form');
  // Si le formulaire n'existe pas dans le DOM, on ne fait rien
  if (!form) return;

  // Vérifie si un listener a déjà été attaché (via dataset HTML personnalisé)
  if (form.dataset.listenerAttached === 'true') return;

  // Ajout de l'écouteur de soumission du formulaire
  form.addEventListener('submit', submitReview);
  // Marque le formulaire comme ayant un listener attaché
  form.dataset.listenerAttached = 'true';
}

// === GESTION DE LA SOUMISSION D’AVIS ===

// Fonction déclenchée lors de la soumission du formulaire d’avis
export async function submitReview(event) {
  event.preventDefault();

  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  if (submitBtn) submitBtn.disabled = true;  // Désactive le bouton pour éviter double clic

  const token = getCookie('token');
  if (!token) {
	// Si l'utilisateur n'est pas connecté, on le redirige vers la page d'accueil
    window.location.href = 'index.html';
    return;
  }

  // Récupération des données du formulaire
  const placeId = getPlaceIdFromURL();
  const reviewText = document.getElementById('review-text').value.trim();
  const rating = document.getElementById('review-rating').value;

  // Vérifie que tous les champs sont remplis
  if (!reviewText || !rating) {
    alert('Veuillez remplir tous les champs');
    if (submitBtn) submitBtn.disabled = false;
    return;
  }

  // Décodage du token pour extraire l'ID utilisateur
  const decoded = parseJwt(token);
  const userId = decoded?.sub;

  if (!userId) {
    alert('Utilisateur non reconnu');
    if (submitBtn) submitBtn.disabled = false;
    return;
  }

  try {
	// Construction des données à envoyer au backend
    const bodyData = {
      place_id: placeId,
      user_id: userId,
      text: reviewText,
      rating: Number(rating)
    };
    console.log('Envoi de la review:', bodyData);

	// Envoi de la requête POST vers l’API
    const response = await fetch(`http://localhost:5000/api/v1/reviews/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bodyData),
    });

	 // Vérifie si la réponse est une erreur
    if (!response.ok) {
  		const errorData = await response.json();

      // Cas particulier : l'utilisateur a déjà laissé un avis pour ce lieu
      if (errorData.error === 'You have already reviewed this place') {
        alert('Vous avez déjà laissé un avis pour ce lieu.');
        return;
      }

      // Lève une erreur générique ou personnalisée
      throw new Error(errorData.message || errorData.error || 'Échec de l\'envoi de la review.');
    }

    // Si tout s’est bien passé
    alert('Avis soumis avec succès !');
    form.reset();  // Réinitialise les champs du formulaire

  } catch (error) {
    console.error('Détail de l\'erreur:', error.message || error);
    alert(`Erreur : ${error.message || error}`);
  } finally {
    // Réactive le bouton de soumission, qu’il y ait eu erreur ou succès
    if (submitBtn) submitBtn.disabled = false;
  }
}
