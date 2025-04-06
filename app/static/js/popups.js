let selectedGameId = null;

// Leave
// При открытии модального окна сохраняем game-id
document.querySelectorAll('.open-leave-modal').forEach(button => {
    console.log("button pressed")
    button.addEventListener('click', function () {
        selectedGameId = this.getAttribute('data-game-id');
    });
});

// Обработка подтверждения выхода
document.getElementById('confirmLeaveBtn').addEventListener('click', function () {
    if (selectedGameId) {
        fetch(`/leave_game/${selectedGameId}`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'redirect') {
                window.location.href = data.url; // вручную редиректим
            } else if (data.status === 'success') {
                alert('Joined!');
            } else {
                alert(data.message);
            }
        });
    }
});

// Delete
// При открытии модального окна сохраняем game-id
document.querySelectorAll('.open-delete-modal').forEach(button => {
    console.log("button pressed")
    button.addEventListener('click', function () {
        selectedGameId = this.getAttribute('data-game-id');
    });
});

// Обработка подтверждения выхода
document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    if (selectedGameId) {
        fetch(`/delete_game/${selectedGameId}`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'redirect') {
                window.location.href = data.url; // вручную редиректим
            } else if (data.status === 'success') {
                alert('Joined!');
            } else {
                alert(data.message);
            }
        });
    }
});