document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('editProfileBtn');
    const cancelBtn = document.getElementById('cancelEdit');
    const saveButtons = document.getElementById('editButtons');

    // Поля и отображение
    const nameDisplay = document.getElementById('nameDisplay');
    const nameInput = document.getElementById('nameInput');
    const aboutDisplay = document.getElementById('aboutDisplay');
    const aboutInput = document.getElementById('aboutInput');
    const profileForm = document.getElementById('profileForm');

    // Перевод в режим редактирования
    editBtn.addEventListener('click', () => {
        let originalName = nameDisplay.textContent;
        let originalAbout = aboutDisplay.textContent;
        if (aboutDisplay.classList.contains('text-muted')) {
            originalAbout = ''
        }

        nameInput.value = originalName;
        aboutInput.value = originalAbout;

        nameDisplay.classList.add('d-none');
        nameInput.classList.remove('d-none');
        aboutDisplay.classList.add('d-none');
        aboutInput.classList.remove('d-none');
        saveButtons.classList.remove('d-none');
    });

    // Отмена редактирования
    cancelBtn.addEventListener('click', () => {
        nameDisplay.classList.remove('d-none');
        nameInput.classList.add('d-none');
        aboutDisplay.classList.remove('d-none');
        aboutInput.classList.add('d-none');
        saveButtons.classList.add('d-none');
    });

    // Отправка данных через AJAX
    profileForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        const formData = new FormData(profileForm);

        fetch("/update_profile", {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновление информации на странице
                document.getElementById('nameDisplay').textContent = data.updated_name;
                if (data.updated_about) {
                    document.getElementById('aboutDisplay').textContent = data.updated_about;
                    aboutDisplay.classList.remove('text-muted');
                } else {
                    document.getElementById('aboutDisplay').textContent = 'You have not written about yourself yet';
                    aboutDisplay.classList.add('text-muted');
                }

                // Переключаем обратно на параграфы
                nameDisplay.classList.remove('d-none');
                nameInput.classList.add('d-none');
                aboutDisplay.classList.remove('d-none');
                aboutInput.classList.add('d-none');
                saveButtons.classList.add('d-none');
            } else {
                alert("Failed to update profile!");
            }
        })
        .catch(error => {
            console.error("Error updating profile:", error);
            alert("Something went wrong!");
        });
    });
});

// Обработчик для выбора нового файла
function previewAvatar(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatarImage').src = e.target.result; // Обновляем аватарку
        };
        reader.readAsDataURL(file);

        const formData = new FormData();
        formData.append('avatar', file);

        fetch('/update_avatar', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Upload failed');
            return response.json();
        })
        .then(data => {
            console.log('Avatar updated:', data);
        })
        .catch(error => {
            console.error('Error uploading avatar:', error);
        });
    }
}
