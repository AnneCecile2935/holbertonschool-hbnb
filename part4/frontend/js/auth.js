// Fonction pour récupérer la valeur d'un cookie par son nom
export function getCookie(name) {
  // Ajoute un point-virgule et un espace avant les cookies pour faciliter la recherche
  const value = `; ${document.cookie}`;
  // Sépare la chaîne des cookies en deux parties, en cherchant le cookie avec le nom donné
  const parts = value.split(`; ${name}=`);
  // Si on trouve bien une partie correspondant au cookie demandé
  // on retourne sa valeur (jusqu'au prochain point-virgule)
  // sinon on retourne null
  if (parts.length === 2) {
    const cookiePart = parts.pop(); // récupère la partie contenant la valeur
    const cookieValue = cookiePart.split(';').shift(); // isole la valeur
    return cookieValue;
  } else {
    return null;
  }
}

// Fonction pour récupérer le token JWT stocké dans le cookie 'token'
export function getToken() {
  return getCookie('token');
}

// Fonction pour enregistrer un token JWT dans un cookie nommé 'token'
// Le cookie est accessible sur tout le site (path=/)
export function setToken(token) {
  console.log("Setting token cookie:", token);
  document.cookie = `token=${token}; path=/`;
  console.log("Cookie after setting:", document.cookie);
}

// Fonction pour supprimer le cookie 'token' en le rendant expiré immédiatement
export function deleteToken() {
  document.cookie = 'token=; Max-Age=0; path=/';
}

// Fonction pour vérifier si l'utilisateur est authentifié
// Elle retourne true si un token est présent (converti en booléen), false sinon
export function isAuthenticated() {
  const token = getToken();
  return token !== null && token !== undefined && token !== '';
}

// Fonction pour rediriger l'utilisateur vers la page index.html
// s'il n'est pas authentifié (pas de token)
export function redirectIfNotAuthenticated() {
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
  }
}
export function updateAuthButtons() {
  const loginButton = document.getElementById('login-button');
  const logoutButton = document.getElementById('logout-button');

  if (isAuthenticated()) {
    if (loginButton) loginButton.style.display = 'none';
    if (logoutButton) logoutButton.style.display = 'inline-block';
  } else {
    if (loginButton) loginButton.style.display = 'inline-block';
    if (logoutButton) logoutButton.style.display = 'none';
  }
}

export function setupLogoutButton() {
  const logoutButton = document.getElementById('logout-button');
  if (logoutButton) {
    logoutButton.addEventListener('click', () => {
      if (confirm('Are you sure you want to log out?')) {
        deleteToken();
        window.location.href = 'login.html';
      }
    });
  }
}
