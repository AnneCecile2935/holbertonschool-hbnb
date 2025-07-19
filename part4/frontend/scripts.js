/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password })
      });

      const data = await response.json(); // On lit une fois la réponse JSON

      if (response.ok) {
        document.cookie = `access_token=${data.access_token}; path=/;`;
        window.location.href = 'index.html';
      } else {
        // Afficher l’erreur retournée par l’API dans ta page
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
          errorMessage.textContent = data.error || "Login failed.";
        }
      }
    } catch (error) {
      console.log('Error:', error);
    }
  });
});
