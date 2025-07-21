// Attend que tout le contenu de la page HTML soit chargé avant d’exécuter le script
document.addEventListener('DOMContentLoaded', () => {
  // Récupère le formulaire de connexion par son ID
  const form = document.getElementById('login-form');
  // Si on ne trouve pas le formulaire, on quitte (peut-être qu’on n’est pas sur login.html)
  if (!form) {
    // On est probablement sur une autre page que login.html
    return;
  }
  // Ajoute un écouteur d’événement sur la soumission du formulaire
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Empêche l’envoi classique du formulaire (rechargement de la page)
    // Récupère les valeurs saisies par l’utilisateur
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      // Envoie une requête POST à l’API backend pour se connecter
      const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}, // Indique qu’on envoie des données JSON
        body: JSON.stringify({ email, password }) // Données à envoyer dans le corps de la requête
      });
      // On essaie de lire la réponse du serveur (normalement en JSON)
      const data = await response.json();
       // Si la réponse est un succès (code HTTP 2xx), on stocke le token dans un cookie
      if (response.ok) {
        document.cookie = `access_token=${data.access_token}; path=/;`;
        // Redirige l’utilisateur vers la page d’accueil après une connexion réussie
        window.location.href = 'index.html';
      } else {
        // En cas d’erreur (ex : mauvais mot de passe), on affiche un message dans la page
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
          errorMessage.textContent =
		   data?.error || data?.message || "Login failed.";
        }
      }
    } catch (error) {
      // Si la requête échoue complètement (ex : serveur non disponible)
      console.log('Error:', error);
    }
  });
});
