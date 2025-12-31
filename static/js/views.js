// Listing users
async function loadUsers() {
    const API_URL = "http://localhost:5000";
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
async function loadWorkspaceMembers(workspace_id) {
    const API_URL = "http://localhost:5000";
    try {
        const response = await fetch(`${API_URL}/views/listing_workspace_members/${workspace_id}`);
        const data = await response.json()

        const select = document.getElementById("workspace_members_list");
        select.innerHTML = "";

        //Empty option
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Selecione um responsável";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        select.appendChild(defaultOption);

        data.forEach(item => {
            const option = document.createElement("option");
            option.value = item.member_id;
            option.textContent = item.username;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}

// Listing view workspace members
async function loadViewWorkspaceMembers(workspace_id) {
    const API_URL = "http://localhost:5000";
    try {
        const response = await fetch(`${API_URL}/views/listing_workspace_members/${workspace_id}`);
        const data = await response.json()

        const select = document.getElementById("workspace_members_list");
        select.innerHTML = "";

        data.forEach(item => {
            const p = document.createElement("p");
            p.value = item.member_id;
            p.textContent = item.username;
            select.appendChild(p);
        });
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro de conexão');
    }
}