// Showing the add form
function showAddForm(columnId) {
    document.getElementById('modalColumnId').value = columnId;
    document.getElementById('cardTitle').value = '';
    document.getElementById('cardDescription').value = '';
    document.getElementById('workspace_members_list').value = '';
    document.getElementById('date').value = '';
    document.getElementById('addModal').style.display = 'block';
}

// Closing the add form modal
function closeModal() {
    document.getElementById('addModal').style.display = 'none';
}

// Closing the add form modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('addModal');
    if (event.target === modal) {
        closeModal();
    }
});

//Showing the delete card modal
function showDelCardModal(cardId) {
    document.getElementById('modalCardId').value = cardId;
    document.getElementById('delModal').style.display = 'block';
}

// Closing the delete card modal
function closeDelModal() {
    document.getElementById('delModal').style.display = 'none';
}

// Closing the delete card modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('delModal');
    if (event.target === modal) {
        closeDelModal();
    }
});

//Showing the add members modal
function showAddMembersModal(workspaceId) {
    document.getElementById('modalWorkspaceId').value = workspaceId;
    document.getElementById('addMembersModal').style.display = 'block';
    loadUsers();
}

// Closing the add members modal
function closeAddMembersModal() {
    document.getElementById('addMembersModal').style.display = 'none';
}

// Closing the add members modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('addMembersModal');
    if (event.target === modal) {
        closeDelModal();
    }
});

// Adding member into a workspace
async function addMember(event) {
    event.preventDefault();
    const workspace_id = document.getElementById('modalWorkspaceId').value
    const user_id = document.getElementById('users_list').value;
    const role = document.getElementById('roles_list').value;
    const API_URL = "http://127.0.0.1:5000"; 
    
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
        
        if (response.ok) {
            alert('Membro adicionado com sucecsso');
            window.location.reload();
        } else {
            alert('Erro ao adicionar membro');
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
    const API_URL = "http://127.0.0.1:5000"; 
    
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
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Erro ao criar card');
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
    const API_URL = "http://127.0.0.1:5000"; 
    
    try {
        const response = await fetch(`${API_URL}/api/delete_card/${card_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            });
        if (response.ok) {
            alert('Card deletado com sucesso');
            window.location.reload();
        } else {
            alert('Erro ao deletar o card');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}

// Listing users
async function loadUsers() {
    const API_URL = "http://127.0.0.1:5000";
    try {
        const response = await fetch(`${API_URL}/views/listing_users`);
        const data = await response.json()

        const select = document.getElementById("users_list");
        select.innerHTML = "";

        //Empty option
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Selecione um usuário";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        select.appendChild(defaultOption);

        data.forEach(item => {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.username;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}

// Listing workspace members
async function loadWorkspaceMembers(board_id) {
    const API_URL = "http://127.0.0.1:5000";
    try {
        const response = await fetch(`${API_URL}/views/listing_workspace_members/${board_id}`);
        const data = await response.json()

        const select = document.getElementById("workspace_members_list");
        select.innerHTML = "";

        data.forEach(item => {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.username;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}

