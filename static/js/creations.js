const creationWorkspaceForm = document.getElementById('createWorkspaceForm');

if (creationWorkspaceForm) {
    creationWorkspaceForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const API_URL = "http://localhost:5000";

        try {
            const response = await fetch(`${API_URL}/api/create_workspace`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title: title,
                    description: description
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