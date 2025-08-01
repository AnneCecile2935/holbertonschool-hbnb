import { getCookie } from './auth.js';
import { parseJwt } from './utils.js';

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}
export function setupReviewForm() {
  const form = document.getElementById('review-form');
  if (!form) return;

  // Empêche d'ajouter plusieurs fois le même listener
  if (form.dataset.listenerAttached === 'true') return;

  form.addEventListener('submit', submitReview);
  form.dataset.listenerAttached = 'true';
}
// Fonction qui gère la soumission de la review
export async function submitReview(event) {
  event.preventDefault();
  console.trace('submit triggered');

  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  if (submitBtn) submitBtn.disabled = true;  // Désactive le bouton pour éviter double clic

  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const placeId = getPlaceIdFromURL();
  const reviewText = document.getElementById('review-text').value.trim();
  const rating = document.getElementById('review-rating').value;

  if (!reviewText || !rating) {
    alert('Veuillez remplir tous les champs');
    if (submitBtn) submitBtn.disabled = false;
    return;
  }

  const decoded = parseJwt(token);
  const userId = decoded?.sub;

  if (!userId) {
    alert('Utilisateur non reconnu');
    if (submitBtn) submitBtn.disabled = false;
    return;
  }

  try {
    const bodyData = {
      place_id: placeId,
      user_id: userId,
      text: reviewText,
      rating: Number(rating)
    };
    console.log('Envoi de la review:', bodyData);

    const response = await fetch(`http://localhost:5000/api/v1/reviews/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bodyData),
    });

    if (!response.ok) {
  const errorData = await response.json();
  console.error('Erreur API:', errorData);

  if (errorData.error === 'You have already reviewed this place') {
    alert('Vous avez déjà laissé un avis pour ce lieu.');
    return;
  }

  throw new Error(errorData.message || errorData.error || 'Échec de l\'envoi de la review.');
}

    alert('Avis soumis avec succès !');
    form.reset();

  } catch (error) {
    console.error('Détail de l\'erreur:', error.message || error);
    alert(`Erreur : ${error.message || error}`);
  } finally {
    if (submitBtn) submitBtn.disabled = false;  // Réactive le bouton après traitement
  }
}
