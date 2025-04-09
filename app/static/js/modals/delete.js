let deleteGameId = null;

// Delete
// При открытии модального окна сохраняем game-id
document.querySelectorAll('.open-delete-modal').forEach(button => {
    console.log("button pressed")
    button.addEventListener('click', function () {
        deleteGameId = this.getAttribute('data-game-id');
    });
});

// Обработка подтверждения удаления
document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    if (deleteGameId) {
        fetch(`/delete/${deleteGameId}`, {
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