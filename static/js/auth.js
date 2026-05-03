// Authentication utilities.
const API_BASE = '/api/auth';
let currentUser = null;

function getToken() {
    return localStorage.getItem('jwt_token');
}

function setToken(token) {
    localStorage.setItem('jwt_token', token);
}

function removeToken() {
    localStorage.removeItem('jwt_token');
}

function getAuthHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

async function fetchUser() {
    try {
        const response = await fetch(`${API_BASE}/user`, {
            headers: getAuthHeaders()
        });
        
        if (response.ok) {
            currentUser = await response.json();
            if (document.getElementById('current-user')) {
                document.getElementById('current-user').textContent = currentUser.username;
            }
            return currentUser;
        } else if (response.status === 401) {
            // Token invalid, redirect to login.
            window.location.href = '/login.html';
        }
    } catch (error) {
        console.error('Помилка отримання користувача:', error);
    }
    return null;
}

async function logout() {
    try {
        await fetch(`${API_BASE}/logout`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
    } catch (error) {
        console.error('Помилка виходу:', error);
    }
    removeToken();
    window.location.href = '/login.html';
}

// Check auth on page load.
document.addEventListener('DOMContentLoaded', () => {
    if (!getToken()) {
        window.location.href = '/login.html';
        return;
    }
    
    fetchUser();
    
    // Set up logout button.
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});

