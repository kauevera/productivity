// Showing the add form modal
function showAddForm(columnId, workspaceId) {
    document.getElementById('modalColumnId').value = columnId;
    document.getElementById('cardTitle').value = '';
    document.getElementById('cardDescription').value = '';
    document.getElementById('workspace_members_list').value = '';
    document.getElementById('date').value = '';
    document.getElementById('addModal').style.display = 'block';
    loadWorkspaceMembers(workspaceId);
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
        closeAddMembersModal();
    }
});

//Showing the view members modal
function showViewMembersModal(workspaceId) {
    document.getElementById('modalWorkspaceId').value = workspaceId;
    document.getElementById('viewMembersModal').style.display = 'block';
    loadViewWorkspaceMembers(workspaceId);
}

// Closing the view members modal
function closeViewMembersModal() {
    document.getElementById('viewMembersModal').style.display = 'none';
}

// Closing the view members modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('viewMembersModal');
    if (event.target === modal) {
        closeViewMembersModal();
    }
});