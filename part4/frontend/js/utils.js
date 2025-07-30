// Exporte une fonction permettant d'extraire l'ID d'un lieu depuis l'URL actuelle
export function getPlaceIdFromURL() {
  // Crée un objet URLSearchParams à partir de la chaîne de requête (après le '?')
  const params = new URLSearchParams(window.location.search);
  // Retourne la valeur associée à la clé 'id' dans les paramètres de l'URL
  // Par exemple, si l'URL est 'place.html?id=123', la fonction renverra '123'
  return params.get('id');
}

// Exporte une fonction qui décode un token JWT (JSON Web Token)
// et retourne la charge utile (payload) sous forme d'objet JavaScript
export function parseJwt(token) {
  try {
    // Un token JWT est constitué de trois parties séparées par des points (.)
    // On récupère la deuxième partie (le payload), qui est encodée en base64url
    const base64 = token.split('.')[1];

    // atob décode une chaîne base64 en chaîne texte,
    // JSON.parse convertit la chaîne JSON en objet JavaScript
    return JSON.parse(atob(base64));
  } catch (e) {
    // En cas d'erreur (token mal formé ou décodage impossible),
    // on log l'erreur dans la console pour debug
    console.error("Failed to parse token:", e);
    // On retourne null pour indiquer l'échec du parsing
    return null;
  }
}
