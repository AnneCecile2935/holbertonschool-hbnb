// Import des fonctions nécessaires
import { fetchPlaceDetails } from './place.js';
import { getCookie } from './auth.js'; //

// Lorsque la page est complètement chargée
document.addEventListener('DOMContentLoaded', async () => {
  // Récupère l'ID du lieu à partir de l'URL (ex: ?id=123)
  const urlParams = new URLSearchParams(window.location.search);
  const placeId = urlParams.get('id');

  // Si aucun ID n'est fourni, afficher une erreur et interrompre l'exécution
  if (!placeId) {
    console.error('No place ID provided in the URL.');
    alert('No place ID provided in the URL.');
    return;
  }

  try {
    // Récupère le token JWT depuis les cookies
    const token = getCookie('token');
    if (!token) {
      throw new Error('No token found');
    }
    // Appelle l'API pour obtenir les détails du lieu avec le token et l'ID
    const place = await fetchPlaceDetails(token, placeId);

    // Si aucun lieu n'est retourné, afficher une erreur
    if (!place) {
      throw new Error('Failed to fetch place details');
    }
    // Pré-remplit le formulaire d'édition avec les données du lieu
    populateEditForm(place);
  } catch (error) {
    console.error('Failed to fetch place details:', error);
    alert('Failed to fetch place details: ' + error.message);
  }

  // Ajoute un écouteur d'événement sur le formulaire pour la soumission
  const editForm = document.getElementById('edit-place-form');
  if (editForm) {
    editForm.addEventListener('submit', async (event) => {
      event.preventDefault(); // Empêche le rechargement de la page
      try {
        const token = getCookie('token');
        await updatePlace(token, placeId);
      } catch (error) {
        console.error('Failed to update place:', error);
        alert('Failed to update place: ' + error.message);
      }
    });
  }
});
// Remplit le formulaire avec les données du lieu
function populateEditForm(place) {
  const titleInput = document.getElementById('title');
  const descriptionInput = document.getElementById('description');
  const priceInput = document.getElementById('price');

  // Vérifie que tous les éléments du formulaire sont présents
  if (!titleInput || !descriptionInput || !priceInput) {
    console.error('One or more form elements not found.');
    return;
  }
  // Assigne les valeurs du lieu aux champs du formulaire
  titleInput.value = place.title;
  descriptionInput.value = place.description;
  priceInput.value = place.price;
}

// Envoie une requête PUT à l’API pour mettre à jour le lieu
async function updatePlace(token, placeId) {
  const titleInput = document.getElementById('title');
  const descriptionInput = document.getElementById('description');
  const priceInput = document.getElementById('price');

  // Vérifie que tous les champs nécessaires sont présents
  if (!titleInput || !descriptionInput || !priceInput) {
    console.error('One or more form elements not found.');
    return;
  }
   // Prépare les données à envoyer au serveur
  const formData = {
    title: titleInput.value,
    description: descriptionInput.value,
    price: parseFloat(priceInput.value)
  };

  try {
    // Effectue une requête PUT avec le token pour authentification
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(formData)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update place');
    }

    // Notifie l'utilisateur et redirige vers la page de détail
    alert('Place updated successfully!');
    window.location.href = `place.html?id=${placeId}`;
  } catch (error) {
    console.error('Error updating place:', error);
    throw error;
  }
}
