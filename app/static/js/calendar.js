var calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
    initialView: 'dayGridMonth',
    events: EVENTS,
    eventClick: function(info) {
        // Получаем данные события
        var event = info.event;

        // Обновляем содержимое модального окна
        document.getElementById('modal-event-title').innerText = event.title;
        document.getElementById('modal-organizer-name').innerText = event.extendedProps.organizerName;
        document.getElementById('modal-player-count').innerText = event.extendedProps.playerCount;
        document.getElementById('modal-start-time').innerText = event.start.toLocaleString();
        document.getElementById('modal-end-time').innerText = event.end.toLocaleString();

        // Добавляем описание, если есть
        var description = event.extendedProps.description;
        if (description) {
            document.getElementById('modal-about-section').style.display = 'block';
            document.getElementById('modal-about-text').innerText = description;
        } else {
            document.getElementById('modal-about-section').style.display = 'none';
        }

        // Если пользователь может присоединиться
        var show = 'modal-join'
        if (event.extendedProps.registered) {
            if (event.extendedProps.joined) {
                show = 'modal-joined'
            }
            if (event.extendedProps.isAuthor) {
                show = 'modal-organizer'
            }
        } else {
            show = 'modal-register'
        }

        document.getElementById('modal-join').style.display = 'none';
        document.getElementById('modal-register').style.display = 'none';
        document.getElementById('modal-joined').style.display = 'none';
        document.getElementById('modal-organizer').style.display = 'none';

        document.getElementById(show).style.display = 'block';

        if (show == 'modal-join') {
            var joinButton = document.getElementById('modal-join-button');
            joinButton.setAttribute('data-game-id', event.id);
            if (event.extendedProps.userCanJoin) {
                joinButton.style.display = 'block'; // Показать кнопку "Join"
            } else {
                joinButton.style.display = 'none'; // Скрыть кнопку "Join"
            }
        }

        document.getElementById('modal-delete-button').setAttribute('data-game-id', event.id);
        document.getElementById('modal-leave-button').setAttribute('data-game-id', event.id);

        // Показываем модальное окно
        var modal = new bootstrap.Modal(document.getElementById('eventModal'));
        modal.show();
    }
});

calendar.render();
