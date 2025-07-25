document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      if(!email || !password) {
        alert('Please fill in all required fields.');
        return;
      }
      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'

          },
          body: JSON.stringify({email, password})
        });
        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = `index.html`;
        } else {
          const error = await response.json();
          alert('Error connection : ' + (error.message || response.statusText));
        }
      }catch (err) {
        console.error('Error connection :', err);
        alert('Error during connection attempt.');
      }
    });
  }
  const loginButton = document.getElementById('login-button');
  const logoutButton = document.getElementById('logout-button');

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  const token = getCookie('token');

  if (token) {
    if (loginButton) loginButton.style.display = 'none';
    if (logoutButton) logoutButton.style.display = 'inline-block';
    if (window.location.pathname.endsWith('index.html')) {
      fetchPlaces(token);
    } else {
      if (loginButton) loginButton.style.display = 'block';
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
  // 💸 Filtre par prix
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
});



// 📦 Récupération des places depuis l'API
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

// 🧱 Affichage dynamique des places
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
    `;

    placesList.appendChild(placeDiv);
  });
}
