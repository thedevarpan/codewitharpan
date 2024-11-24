document.getElementById('like-btn').addEventListener('click', function(e) {
    e.preventDefault();
    const slug = this.getAttribute('data-slug');
    fetch(`/blog/like-blog/${slug}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            document.getElementById('like-count').innerText = data.likes;
            document.getElementById('dislike-count').innerText = data.dislikes;
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('dislike-btn').addEventListener('click', function(e) {
    e.preventDefault();
    const slug = this.getAttribute('data-slug');
    fetch(`/blog/dislike-blog/${slug}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            document.getElementById('like-count').innerText = data.likes;
            document.getElementById('dislike-count').innerText = data.dislikes;
        }
    })
    .catch(error => console.error('Error:', error));
});

// Function to get CSRF token from cookie
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
