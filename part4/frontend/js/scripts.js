document.addEventListener('DOMContentLoaded', () => {
  console.log("URL search params:", window.location.search);
  console.log("Place ID:", new URLSearchParams(window.location.search).get('id'));
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      if (!email || !password) {
        alert('Please fill in all required fields.');
        return;
      }
      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = `index.html`;
        } else {
          const error = await response.json();
          alert('Error connection : ' + (error.message || response.statusText));
        }
      } catch (err) {
        console.error('Error connection :', err);
        alert('Error during connection attempt.');
      }
    });
  }

  const loginButton = document.getElementById('login-button');
  const logoutButton = document.getElementById('logout-button');

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  const token = getCookie('token');

  if (token) {
    if (loginButton) loginButton.style.display = 'none';
    if (logoutButton) logoutButton.style.display = 'inline-block';

    if (window.location.pathname.endsWith('index.html')) {
      fetchPlaces(token);
    }

    if (window.location.pathname.endsWith('place.html')) {
      const placeId = getPlaceIdFromURL();
      if (placeId) fetchPlaceDetails(token, placeId);
    }
  } else {
    if (loginButton) loginButton.style.display = 'inline-block';
    if (logoutButton) logoutButton.style.display = 'none';

    if (window.location.pathname.endsWith('add_review.html')) {
      window.location.href = 'index.html';
    }
  }

  if (logoutButton) {
    logoutButton.addEventListener('click', (e) => {
      e.preventDefault();
      const confirmLogout = confirm("Are you sure you want to log out?");
      if (confirmLogout) {
        document.cookie = 'token=; Max-Age=0; path=/';
        window.location.href = 'login.html';
      }
    });
  }

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const maxPrice = event.target.value;
      const places = document.querySelectorAll('#places-list .place-item');

      places.forEach(place => {
        const price = parseFloat(place.dataset.price);
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
          place.style.display = 'block';
        } else {
          place.style.display = 'none';
        }
      });
    });
  }

  if (window.location.pathname.endsWith('add_review.html')) {
    if (!token) {
      window.location.href = 'index.html';
      return;
    }
    const placeId = getPlaceIdFromURL();
    if (placeId) fetchPlaceDetails(token, placeId);

    const reviewForm = document.getElementById('review-form');
    const messageBox = document.getElementById('message');

    if (!placeId) {
      alert("No place ID found in the URL.");
      return;
    }

    if (reviewForm) {
      reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const content = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('review-rating').value;

        if (!content || !rating) {
          alert("Please fill in all fields.");
          return;
        }

        try {
          const reviewPayload = {
            place_id: placeId,
            user_id: null, // si tu n’as pas besoin de l’envoyer (backend récupère user_id via JWT)
            text: content,
            rating: parseInt(rating)
          };

          const response = await fetch('http://localhost:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reviewPayload)
          });

          const result = await response.json();

          if (response.ok) {
            if (messageBox) messageBox.innerText = 'Review submitted successfully!';
            reviewForm.reset();
          } else {
            if (messageBox) messageBox.innerText = result.message || 'Failed to submit review.';
          }
        } catch (err) {
          console.error('Error submitting review:', err);
          alert("Error while submitting review.");
        }
      });
    }
  }

  if (window.location.pathname.endsWith('place.html')) {
    const placeId = getPlaceIdFromURL();
    const reviewSection = document.getElementById('add-review-section');
    const reviewForm = document.getElementById('review-form');

    if (!placeId) {
      alert("No place ID found in the URL.");
      return;
    }

    if (token) {
      if (reviewSection) reviewSection.style.display = 'block';
      if (reviewForm) reviewForm.style.display = 'block';
    } else {
      if (reviewSection) reviewSection.style.display = 'none';
      if (reviewForm) reviewForm.style.display = 'none';
    }

    fetchPlaceDetails(token, placeId);

    if (reviewForm) {
      reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const placeId = getPlaceIdFromURL();
        console.log("Submit handler - Place ID:", placeId); // Ajouté

        if (!placeId) {
          alert("Place ID is missing!");
          return;
      }

        const content = document.getElementById('review-text').value.trim();
        const rating = document.getElementById('review-rating').value;
        console.log("Submitting review for placeId:", placeId, "content:", content, "rating:", rating);
        if (!content || !rating) {
          alert("Please fill in all fields.");
          return;
        }

        try {
          const reviewPayload = {
            place_id: placeId,
            text: content,
            rating: parseInt(rating)
          };

          console.log("Payload:", reviewPayload);
          const response = await fetch(`http://localhost:5000/api/v1/reviews`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reviewPayload)
          });

          const result = await response.json();
          const messageBox = document.getElementById('message');

          if (response.ok) {
            if (messageBox) messageBox.innerText = 'Review submitted successfully!';
            fetchPlaceDetails(token, placeId);
            reviewForm.reset();
          } else {
            if (messageBox) messageBox.innerText = result.message || 'Failed to submit review.';
          }
        } catch (err) {
          console.error('Error submitting review:', err);
          alert("Error while submitting review.");
        }
      });
    }
  }
});

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/places/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      console.error('Erreur API places:', response.statusText);
    }
  } catch (error) {
    console.error('Erreur fetch places:', error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  placesList.innerHTML = '';

  places.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.classList.add('place-item');
    placeDiv.dataset.price = place.price;

    placeDiv.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description}</p>
      <p><strong>Price:</strong> $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(placeDiv);
  });
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    });

    if (!response.ok) {
      throw new Error("Failed to fetch place details");
    }

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (error) {
    console.error("Error fetching place details:", error);
    alert("Could not load place details.");
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  container.innerHTML = `
    <h2>${place.title}</h2>
    <p>${place.description}</p>
    <p><strong>Price:</strong> $${place.price}</p>
    <h4>Amenities:</h4>
    <ul>
      ${place.amenities.map(a => `<li>${a.name}</li>`).join('')}
    </ul>
  `;

  const reviewList = document.getElementById('review-list');
  if (reviewList) {
    reviewList.innerHTML = place.reviews && place.reviews.length > 0
      ? place.reviews.map(r => `<li><strong>${r.user?.first_name}:</strong> ${r.comment} (${r.rating}/5)</li>`).join('')
      : '<li>No reviews yet.</li>';
  }
}
