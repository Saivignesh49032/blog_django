document.addEventListener('DOMContentLoaded', function () {

    // --- CSRF Token Helper ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- Dark Mode Toggle ---
    const toggleBtn = document.getElementById('dark-mode-toggle');
    const body = document.body;

    // Check local storage
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
            } else {
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }

    // --- AJAX Like Button ---
    const likeForms = document.querySelectorAll('.like-form');
    likeForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = this.action;
            const btn = this.querySelector('.like-button');
            const countSpan = this.querySelector('.like-count');
            const icon = btn.querySelector('span');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.liked) {
                        icon.classList.remove('unliked');
                        icon.classList.add('liked');
                        icon.innerText = '❤️';
                    } else {
                        icon.classList.remove('liked');
                        icon.classList.add('unliked');
                        icon.innerText = '🤍';
                    }
                    countSpan.innerText = data.count + (data.count === 1 ? ' Like' : ' Likes');
                })
                .catch(error => console.error('Error:', error));
        });
    });

    // --- AJAX Comment Form ---
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = this.action;
            const formData = new FormData(this);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Append new comment
                        const commentsList = document.querySelector('.comments-list');
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = data.html;
                        commentsList.appendChild(tempDiv.firstElementChild);

                        // Clear form
                        this.reset();
                    } else {
                        alert('Error posting comment. Please try again.');
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    // --- AJAX Clear Likes Button ---
    const clearLikesBtn = document.getElementById('clear-likes-btn');
    if (clearLikesBtn) {
        clearLikesBtn.addEventListener('click', function () {
            console.log('Clear Likes button clicked');
            const postId = this.getAttribute('data-post-id');
            const url = `/blog/${postId}/clear-likes/`;
            console.log('Sending POST request to:', url);

            fetch(url, {
                method: 'POST', // Changed to POST to avoid potential PATCH issues
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    console.log('Response status:', response.status);
                    return response.json();
                })
                .then(data => {
                    console.log('Response data:', data);
                    if (data.success) {
                        alert('Likes cleared!');
                        // Reload the page to ensure the UI is correct
                        window.location.reload();
                    } else {
                        console.error('Clear likes failed:', data);
                        alert('Failed to clear likes. Please try again.');
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }
});
