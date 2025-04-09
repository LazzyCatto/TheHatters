document.addEventListener('DOMContentLoaded', function() {
    const joinBtn = document.getElementById('modal-join-button');
    if (joinBtn) {
        joinBtn.addEventListener('click', function() {
            const gameId = this.getAttribute('data-game-id');
            fetch(`/join/${gameId}`, {
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
        });
    }
});
