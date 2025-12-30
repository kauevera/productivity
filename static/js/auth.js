const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const nickname = document.getElementById('nickname').value;
        const password = document.getElementById('password').value;
        const API_URL = "http://localhost:5000";

        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nickname: nickname,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                window.location.href = data.redirect;
            } else {
                alert(data.message); 
            }

        } catch (error) {
            console.error(error);
            alert('Erro de conexão');
        }
    });
}

const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const nickname = document.getElementById('nickname').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const gender = document.querySelector('input[name="gender"]:checked')?.value;
        if (!gender) {
            alert('Selecione um gênero');
            return;
        }
        const age = document.getElementById('age').value;
        const API_URL = "http://localhost:5000";

        try {
            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    nickname: nickname,
                    email: email,
                    password: password,
                    gender: gender,
                    age: age
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                window.location.href = data.redirect;
            } else {
                alert(data.message); 
                window.location.href = data.redirect;
            }

        } catch (error) {
            console.error(error);
            alert('Erro de conexão');
        }
    });
}
