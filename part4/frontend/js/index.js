// Fonction asynchrone pour récupérer la liste des lieux depuis l’API
// Prend en paramètre un token JWT pour l’authentification (peut être null ou undefined)
export async function fetchPlaces(token) {
  try {
    // Effectue une requête GET vers l’API des lieux
    // Inclut le token dans l’en-tête Authorization si disponible
    const response = await fetch('http://localhost:5000/api/v1/places/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    // Vérifie que la réponse est OK (status HTTP 200–299)
    if (response.ok) {
      // Parse la réponse JSON contenant la liste des lieux
      return await response.json();

      // Appelle la fonction d’affichage des lieux dans la page
    } else {
      // En cas d’erreur côté serveur, affiche un message d’erreur dans la console
      console.error('Erreur API places:', response.statusText);
	  return [];
    }
  } catch (error) {
    // En cas d’erreur réseau ou autre problème, affiche un message d’erreur dans la console
    console.error('Erreur fetch places:', error);
	return [];
  }
}

// Fonction pour afficher la liste des lieux dans le DOM
// Prend en paramètre un tableau d’objets "place"
export function displayPlaces(places) {
  // Récupère l’élément HTML qui contiendra la liste des lieux
  const placesList = document.getElementById('places-list');

  // Si l’élément n’existe pas dans la page, on quitte la fonction
  if (!placesList) return;

  // Vide le contenu actuel pour éviter les doublons à chaque appel
  placesList.innerHTML = '';

  // Parcourt chaque lieu dans le tableau
  places.forEach(place => {
    // Crée un nouvel élément <div> pour afficher les détails du lieu
    const placeDiv = document.createElement('div');
    // Ajoute une classe CSS pour le style
    placeDiv.classList.add('place-item');
    // Ajoute un attribut data-price avec le prix, utile pour filtrer ou trier
    placeDiv.dataset.price = place.price;

    // Remplit le contenu HTML de ce div avec les infos du lieu
    placeDiv.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description}</p>
      <p><strong>Price:</strong> $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    // Ajoute ce div dans la liste des lieux dans la page
    placesList.appendChild(placeDiv);
  });
}
