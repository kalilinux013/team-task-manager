const API = '/api';

const api = {
  token: () => localStorage.getItem('token'),
  setToken: (t) => localStorage.setItem('token', t),
  user: () => JSON.parse(localStorage.getItem('user') || 'null'),
  setUser: (u) => localStorage.setItem('user', JSON.stringify(u)),

  async req(method, path, body) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (this.token()) opts.headers['Authorization'] = `Bearer ${this.token()}`;
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(API + path, opts);
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || 'Request failed');
    return data;
  },
  get(p) { return this.req('GET', p); },
  post(p, b) { return this.req('POST', p, b); },
  patch(p, b) { return this.req('PATCH', p, b); },
  del(p) { return this.req('DELETE', p); },
};

function toast(msg, type = 'success') {
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.classList.add('show'), 50);
  setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 3000);
}

function logout() {
  localStorage.clear();
  window.location.href = '/';
}

// Login form handler
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = e.target.email.value;
  const password = e.target.password.value;
  try {
    const data = await api.post('/auth/login', { email, password });
    api.setToken(data.token); api.setUser(data.user);
    toast('Welcome back! 🎉');
    setTimeout(() => window.location.href = '/dashboard', 600);
  } catch (err) { toast(err.message, 'error'); }
});

// Signup form handler
document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const body = {
    name: e.target.name.value,
    email: e.target.email.value,
    password: e.target.password.value,
    role: e.target.role.value,
  };
  try {
    const data = await api.post('/auth/signup', body);
    api.setToken(data.token); api.setUser(data.user);
    toast('Account created! 🚀');
    setTimeout(() => window.location.href = '/dashboard', 600);
  } catch (err) { toast(err.message, 'error'); }
});