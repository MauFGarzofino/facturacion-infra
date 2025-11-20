export function getAuthHeaders() {
  const token = localStorage.getItem('access_token'); // o como lo estés guardando
  return token ? { Authorization: `Bearer ${token}` } : {};
}
