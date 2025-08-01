import { fetchPlaceDetails } from './place.js';
import { getCookie } from './auth.js'; // Assurez-vous d'importer la fonction getCookie

document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const placeId = urlParams.get('id');

  if (!placeId) {
    console.error('No place ID provided in the URL.');
    alert('No place ID provided in the URL.');
    return;
  }

  try {
    const token = getCookie('token'); // Utilisez la fonction importée
    if (!token) {
      throw new Error('No token found');
    }

    const place = await fetchPlaceDetails(token, placeId);

    if (!place) {
      throw new Error('Failed to fetch place details');
    }

    populateEditForm(place);
  } catch (error) {
    console.error('Failed to fetch place details:', error);
    alert('Failed to fetch place details: ' + error.message);
  }

  const editForm = document.getElementById('edit-place-form');
  if (editForm) {
    editForm.addEventListener('submit', async (event) => {
      event.preventDefault();
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

function populateEditForm(place) {
  const titleInput = document.getElementById('title');
  const descriptionInput = document.getElementById('description');
  const priceInput = document.getElementById('price');

  if (!titleInput || !descriptionInput || !priceInput) {
    console.error('One or more form elements not found.');
    return;
  }

  titleInput.value = place.title;
  descriptionInput.value = place.description;
  priceInput.value = place.price;
}

async function updatePlace(token, placeId) {
  const titleInput = document.getElementById('title');
  const descriptionInput = document.getElementById('description');
  const priceInput = document.getElementById('price');

  if (!titleInput || !descriptionInput || !priceInput) {
    console.error('One or more form elements not found.');
    return;
  }

  const formData = {
    title: titleInput.value,
    description: descriptionInput.value,
    price: parseFloat(priceInput.value)
  };

  try {
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

    alert('Place updated successfully!');
    window.location.href = `place.html?id=${placeId}`;
  } catch (error) {
    console.error('Error updating place:', error);
    throw error;
  }
}
