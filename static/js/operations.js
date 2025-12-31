// Adding member into a workspace
async function addMember(event) {
    event.preventDefault();
    const workspace_id = document.getElementById('modalWorkspaceId').value
    const user_id = document.getElementById('users_list').value;
    const role = document.getElementById('roles_list').value;
    const API_URL = "http://localhost:5000"; 
    
    try {
        const response = await fetch(`${API_URL}/api/add_member`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                workspace_id: workspace_id,
                user_id: user_id,
                role: role
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            window.location.reload();
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}

// Adding new cards
async function addNewCard(event) {
    event.preventDefault();
    const column_id = document.getElementById('modalColumnId').value
    const title = document.getElementById('cardTitle').value;
    const description = document.getElementById('cardDescription').value;
    const responsible_id = document.getElementById('workspace_members_list').value;
    const deadline = document.getElementById('date').value;
    const API_URL = "http://localhost:5000"; 
    
    try {
        const response = await fetch(`${API_URL}/api/create_card`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                deadline: deadline,
                column_id : column_id,
                title: title,
                description: description,
                responsible_id: responsible_id
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}

// Removing cards
async function delCard(event) {
    event.preventDefault();
    const card_id = document.getElementById('modalCardId').value
    const API_URL = "http://localhost:5000"; 
    
    try {
        const response = await fetch(`${API_URL}/api/delete_card/${card_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            window.location.reload();
        } else {
            alert('Erro ao deletar o card');
            window.location.reload();
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}