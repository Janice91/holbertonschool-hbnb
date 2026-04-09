const API_URL = '';

function setCookie(name, value, days = 7) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}

function getCookie(name) {
    return document.cookie.split('; ').reduce((acc, part) => {
        const [key, val] = part.split('=');
        return key === name ? decodeURIComponent(val) : acc;
    }, null);
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

function authHeaders() {
    const token = getCookie('token');
    return token
        ? { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
        : { 'Content-Type': 'application/json' };
}

function initLoginPage() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email    = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const errorMsg = document.getElementById('error-message');
        errorMsg.style.display = 'none';
        try {
            const response = await fetch(`${API_URL}/api/v1/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = 'index.html';
            } else {
                errorMsg.textContent   = 'Login failed: ' + response.statusText;
                errorMsg.style.display = 'block';
            }
        } catch (err) {
            errorMsg.textContent   = 'Impossible de contacter le serveur.';
            errorMsg.style.display = 'block';
        }
    });
}

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_URL}/api/v1/places/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Erreur chargement places');
        const places = await response.json();
        displayPlaces(places);
    } catch (err) {
        document.getElementById('places-list').innerHTML =
            '<p>Erreur lors du chargement des places.</p>';
        console.error(err);
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';
    if (!places.length) {
        container.innerHTML = '<p>Aucune place disponible.</p>';
        return;
    }
    places.forEach(place => {
        const card = document.createElement('article');
        card.classList.add('place-card');
        card.dataset.price = place.price ?? place.price_by_night ?? 0;
        card.innerHTML = `
            <h2>${place.name || 'Sans titre'}</h2>
            <p>Price: ${place.price ?? place.price_by_night ?? '?'}€/night</p>
            <a href="place.html?id=${place.id}">
                <button class="details-button">View Details</button>
            </a>
        `;
        container.appendChild(card);
    });
}

function initIndexPage() {
    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
    document.getElementById('price-filter').addEventListener('change', (event) => {
        const selected = event.target.value;
        document.querySelectorAll('.place-card').forEach(card => {
            const price = parseFloat(card.dataset.price);
            if (selected === 'all' || price <= parseFloat(selected)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || params.get('place_id');
}

function initPlacePage() {
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }
    const token            = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        const link = document.getElementById('add-review-link');
        if (link) link.href = `add_review.html?place_id=${placeId}`;
    }
    fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = token
            ? { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
            : { 'Content-Type': 'application/json' };
        const [placeRes, reviewsRes] = await Promise.all([
            fetch(`${API_URL}/api/v1/places/${placeId}`, { headers }),
            fetch(`${API_URL}/api/v1/reviews/places/${placeId}`)
        ]);
        if (!placeRes.ok) throw new Error('Place introuvable');
        const place   = await placeRes.json();
        const reviews = reviewsRes.ok ? await reviewsRes.json() : [];
        displayPlaceDetails(place);
        displayReviews(reviews);
    } catch (err) {
        console.error(err);
        document.querySelector('main').innerHTML =
            '<p>Erreur lors du chargement de la place.</p>';
    }
}

function displayPlaceDetails(place) {
    document.getElementById('place-name').textContent        = place.name || 'Sans titre';
    document.getElementById('place-host').textContent        = place.host?.name || place.owner?.name || 'Inconnu';
    document.getElementById('place-price').textContent       = place.price ?? place.price_by_night ?? '?';
    document.getElementById('place-description').textContent = place.description || '';
    document.getElementById('place-amenities').textContent   =
        Array.isArray(place.amenities)
            ? place.amenities.map(a => a.name ?? a).join(', ')
            : (place.amenities || '');
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-container');
    if (!reviews.length) {
        container.innerHTML = '<p>Aucun avis pour le moment.</p>';
        return;
    }
    container.innerHTML = reviews.map(r => `
        <div class="review-card">
            <p>${r.text || r.comment || ''}</p>
            <p>User: ${r.user?.name || r.username || 'Anonyme'}</p>
            <p>Rating: ${'⭐'.repeat(Number(r.rating) || 0)}</p>
        </div>
    `).join('');
}

function initAddReviewPage() {
    const token   = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const reviewText = document.getElementById('comment').value.trim();
        const rating     = document.getElementById('rating').value;
        const response   = await submitReview(token, placeId, reviewText, rating);
        handleResponse(response, reviewForm, placeId);
    });
}

async function submitReview(token, placeId, reviewText, rating) {
    return await fetch(`${API_URL}/api/v1/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            place_id: placeId,
            rating:   parseInt(rating),
            text:     reviewText
        })
    });
}

function handleResponse(response, form, placeId) {
    if (response.ok) {
        alert('Review submitted successfully!');
        form.reset();
        window.location.href = `place.html?id=${placeId}`;
    } else {
        alert('Failed to submit review');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const page = window.location.pathname;
    if (page.includes('login.html'))                          initLoginPage();
    if (page.includes('index.html') || page.endsWith('/'))    initIndexPage();
    if (page.includes('place.html') && !page.includes('add')) initPlacePage();
    if (page.includes('add_review.html'))                     initAddReviewPage();
});
