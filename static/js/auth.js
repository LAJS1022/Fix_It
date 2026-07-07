const API_BASE = "/api/v1";

function saveSession(data) {
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user_id', data.user_id);
    localStorage.setItem('role', data.role);
    localStorage.setItem('is_admin', data.is_admin);
}

function getToken() {
    return localStorage.getItem('access_token');
}

function isLoggedIn() {
    return !!getToken();
}

function authHeader() {
    const token = getToken();
    return token ? { "Authorization": `Bearer ${token}` } : {};
}

function clearSession() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');
    localStorage.removeItem('is_admin');
}

function logout() {
    clearSession();
    window.location.href = 'index.html';
}

async function login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Error al iniciar sesión');
    saveSession(data);
    return data;
}

async function register({ first_name, last_name, email, password, phone, role, city }) {
    const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ first_name, last_name, email, password, phone, role, city })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Error al registrarse');
    return data;
}

// Toggles "Iniciar Sesión"/"Registrarse" buttons vs a profile icon,
// based on current login state. Expects these ids in the page:
//   #auth-buttons   -> wrapper around the login/register buttons
//   #profile-link   -> the profile icon link (hidden by default)
async function renderNavAuthState() {
    const authButtons = document.getElementById('auth-buttons');
    const profileLink = document.getElementById('profile-link');
    if (!authButtons || !profileLink) return;

    if (isLoggedIn()) {
        authButtons.classList.add('hidden');
        profileLink.classList.remove('hidden');
        profileLink.classList.add('flex');

        try {
            const res = await fetch(`${API_BASE}/auth/me`, { headers: authHeader() });
            if (res.ok) {
                const user = await res.json();
                const nameEl = document.getElementById('profile-name');
                if (nameEl) nameEl.textContent = `${user.first_name} ${user.last_name}`;
            } else {
                // Token expired or invalid: fall back to logged-out state
                clearSession();
                authButtons.classList.remove('hidden');
                profileLink.classList.add('hidden');
                profileLink.classList.remove('flex');
            }
        } catch (err) {
            console.error('Could not load user profile', err);
        }
    } else {
        authButtons.classList.remove('hidden');
        profileLink.classList.add('hidden');
        profileLink.classList.remove('flex');
    }
}

document.addEventListener('DOMContentLoaded', renderNavAuthState);