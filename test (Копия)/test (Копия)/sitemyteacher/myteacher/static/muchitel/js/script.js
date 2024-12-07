document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.comments__form'); // Форма отправки
    const commentsList = document.querySelector('.comments__teacher'); // Список комментариев
    const textarea = document.querySelector('.chat-input'); // Поле ввода

    if (!form || !commentsList || !textarea) {
        console.error('Не найдены необходимые элементы на странице.');
        return;
    }

    // Функция прокрутки вниз
    function scrollToBottom() {
        commentsList.scrollTop = commentsList.scrollHeight;
    }

    // Прокрутка вниз при загрузке страницы
    scrollToBottom();

    // Обработчик отправки формы
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form); // Собираем данные формы

        try {
            const response = await fetch(form.action || window.location.href, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(), // Добавляем CSRF-токен
                },
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                // Если всё успешно, добавляем новый комментарий
                textarea.value = ''; // Очищаем поле ввода
                adjustTextareaHeight(); // Сбрасываем высоту текстового поля

                // Добавляем новый комментарий в список
                const newComment = document.createElement('li');
                newComment.classList.add('comment');
                newComment.innerHTML = `
                    ${data.content}
                    <button class="menu-btn">...</button>
                    <div class="dropdown">
                        <ul>
                            <li><a href="#" class="report-link">Пожаловаться</a></li>
                        </ul>
                    </div>
                `;
                commentsList.appendChild(newComment);

                // Обновляем обработчики для новых кнопок меню и ссылок
                updateMenuButtons();
                updateReportLinks();

                // Прокрутка вниз
                scrollToBottom();
            } else {
                // Если сервер вернул ошибку, показываем alert
                alert(data.error || 'Произошла ошибка.');
            }
        } catch (error) {
            console.error('Ошибка при отправке:', error);
            alert('Не удалось отправить сообщение. Попробуйте снова.');
        }
    });

    // Функция для автоматической регулировки высоты текстового поля
    function adjustTextareaHeight() {
        textarea.style.height = '50px'; // Минимальная высота
        if (textarea.value.trim() !== '') {
            textarea.style.height = `${textarea.scrollHeight}px`; // Динамическая высота
        }
    }

    // Обновляем высоту при вводе текста
    textarea.addEventListener('input', adjustTextareaHeight);

    // Функция для получения CSRF-токена
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    // Обрабатываем раскрытие меню "..."
    function updateMenuButtons() {
        const menuButtons = document.querySelectorAll('.menu-btn'); // Кнопки меню
        menuButtons.forEach(button => {
            button.addEventListener('click', function (event) {
                const parentLi = event.target.closest('.comment'); // Родительский <li>

                // Переключаем класс для показа/скрытия меню
                parentLi.classList.toggle('show-dropdown');

                // Закрыть все другие открытые меню
                const allComments = document.querySelectorAll('.comment');
                allComments.forEach(comment => {
                    if (comment !== parentLi) {
                        comment.classList.remove('show-dropdown');
                    }
                });
            });
        });
    }

    // Обрабатываем нажатие на "Пожаловаться"
    function updateReportLinks() {
        const reportLinks = document.querySelectorAll('.report-link'); // Ссылки "Пожаловаться"
        reportLinks.forEach(link => {
            link.addEventListener('click', async (e) => {
                e.preventDefault();
                try {
                    const response = await fetch('responce_error/', { // Укажите URL обработки жалоб
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCSRFToken(), // Добавляем CSRF-токен
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: 'Есть плохое сообщение в чате' }),
                    });

                    if (response.ok) {
                        alert('Ваша жалоба успешно отправлена.');
                    } else {
                        alert('Не удалось отправить жалобу. Попробуйте позже.');
                    }
                } catch (error) {
                    console.error('Ошибка при отправке жалобы:', error);
                    alert('Произошла ошибка при отправке жалобы.');
                }
            });
        });
    }

    // Инициализируем обработчики при загрузке страницы
    updateMenuButtons();
    updateReportLinks();
});