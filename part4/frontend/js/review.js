import { getCookie } from './auth.js';
import { parseJwt } from './utils.js';

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}
export function setupReviewForm() {
  const form = document.getElementById('review-form');
  if (!form) return;

  form.addEventListener('submit', submitReview);
}
export async function submitReview(event) {
  event.preventDefault();

  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const placeId = getPlaceIdFromURL();
  const reviewText = document.getElementById('review-text').value.trim();
  const rating = document.getElementById('review-rating').value;

  if (!reviewText || !rating) {
    alert('Please fill in all fields');
    return;
  }
  const decoded = parseJwt(token);
  console.log('Payload JWT:', decoded);
  const userId = decoded.sub;  // ou decoded?.sub selon la structure de ton JWT

  if (!userId) {
    alert('Utilisateur non reconnu');
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
      throw new Error(errorData.message || errorData.error || 'Failed to submit review.');
    }

    alert('Review submitted successfully!');
    document.getElementById('review-form').reset();

  } catch (error) {
	console.error('Détail de l\'erreur:', error.message || error);
    throw error;

  }
}
