// Showing the add form
function showAddForm(columnId) {
    document.getElementById('modalColumnId').value = columnId;
    document.getElementById('cardTitle').value = '';
    document.getElementById('cardDescription').value = '';
    document.getElementById('responsibleId').value = '';
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
    document.getElementById('modalCardnId').value = cardId;
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

// Adding new cards
async function addNewCard(event) {
    event.preventDefault();
    const column_id = document.getElementById('modalColumnId').value
    const title = document.getElementById('cardTitle').value;
    const description = document.getElementById('cardDescription').value;
    const responsible_id = document.getElementById('responsibleId').value;
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
    const card_id = document.getElementById('modalCardnId').value
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