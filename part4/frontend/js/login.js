// Importation de la fonction setToken pour stocker le token JWT après connexion réussie
import { setToken } from './auth.js';

// Fonction principale pour configurer le formulaire de connexion
export function setupLoginForm() {
  // Récupération de l'élément formulaire avec l'ID 'login-form'
  const loginForm = document.getElementById('login-form');
  // Récupération de l'élément où afficher les messages d'erreur, ID 'error-message'
  const messageBox = document.getElementById('error-message');

  // Si le formulaire n'existe pas sur la page, on quitte la fonction (sécurité)
  if (!loginForm) return;

  // Ajout d'un écouteur d'événement sur la soumission du formulaire
  loginForm.addEventListener('submit', async (event) => {
    // Empêche le comportement par défaut du formulaire (rechargement de la page)
    event.preventDefault();

    // Récupération des valeurs saisies dans les champs email et mot de passe
    // .trim() enlève les espaces avant et après dans l'email
    let email;

    const emailInput = document.getElementById('email');

    if (emailInput !== null) {
      email = emailInput.value.trim();
    } else {
      email = undefined;
    }
    let password;

    const passwordInput = document.getElementById('password');

    if (passwordInput !== null) {
      password = passwordInput.value;
    } else {
      password = undefined;
    }

    // Vérification simple que les deux champs sont remplis
    if (!email || !password) {
      alert('Please fill in all required fields.');
      return;  // Arrêt de la fonction si un champ est vide
    }

    try {
      // Envoi d'une requête POST vers l'API d'authentification
      const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',  // Méthode HTTP POST
        headers: { 'Content-Type': 'application/json' },  // En-tête pour indiquer que les données sont en JSON
        body: JSON.stringify({ email, password })  // Corps de la requête : email et mot de passe encodés en JSON
      });

      // Extraction des données JSON reçues en réponse
      const data = await response.json();

      // Si la connexion est réussie (code HTTP 200 OK)
      if (response.ok) {
		console.log('Token reçu :', data.access_token);
        // Stocker le token JWT reçu via la fonction setToken
        setToken(data.access_token);
        // Redirection vers la page principale (index.html)
		window.location.href = 'index.html';
      } else {
        // Si la connexion échoue, afficher un message d'erreur dans le messageBox
        if (messageBox) messageBox.innerText = data.message || 'Login failed.';
      }
    } catch (err) {
      // En cas d'erreur réseau ou autre exception
      console.error('Error during login:', err);
      // Affichage d'un message d'erreur générique dans la zone prévue à cet effet
      if (messageBox) messageBox.innerText = 'Server error. Please try again.';
    }
  });
}
