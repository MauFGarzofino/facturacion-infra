import { authHttp } from './http';

// Login → POST /auth/token (FastAPI OAuth2)
export async function loginUser(username, password) {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  const res = await authHttp.post('/token', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

  return res.data; // { access_token, token_type }
}

// Usuario actual → GET /auth/users/me
export async function getCurrentUser() {
  const res = await authHttp.get('/users/me');
  return res.data; // UserResponse
}

// (opcional) Registro de usuario → POST /auth/users
export async function createUser(userData) {
  // userData: { username, email, full_name?, disabled?, password }
  const res = await authHttp.post('/users', userData);
  return res.data;
}
