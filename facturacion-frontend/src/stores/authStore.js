// src/stores/authStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { loginUser, getCurrentUser } from '../api/authApi';
import { authHttp, empresasHttp, rfactHttp, notifHttp } from '../api/http';

export const useAuthStore = defineStore('auth', () => {
  // --- state ---
  const token = ref(
    typeof localStorage !== 'undefined'
      ? localStorage.getItem('access_token')
      : null
  );
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);

  // --- helpers internos ---
  function _applyTokenToClients() {
    const authHeader = token.value ? `Bearer ${token.value}` : '';

    [authHttp, empresasHttp, rfactHttp, notifHttp].forEach((client) => {
      if (!client) return;
      if (authHeader) {
        client.defaults.headers.common['Authorization'] = authHeader;
      } else {
        delete client.defaults.headers.common['Authorization'];
      }
    });
  }

  function _setToken(newToken) {
    token.value = newToken;

    if (typeof localStorage !== 'undefined') {
      if (newToken) {
        localStorage.setItem('access_token', newToken);
      } else {
        localStorage.removeItem('access_token');
      }
    }

    _applyTokenToClients();
  }

  // --- acciones públicas ---
  async function login(username, password) {
    // 1. pedir token al microservicio de auth
    const data = await loginUser(username, password); // { access_token, token_type }
    _setToken(data.access_token);

    // 2. obtener los datos del usuario actual
    try {
      const me = await getCurrentUser();
      user.value = me;
    } catch (e) {
      console.error('Error obteniendo /users/me', e);
      user.value = null;
    }
  }

  function logout() {
    user.value = null;
    _setToken(null);
  }

  // 👈 MUY IMPORTANTE: devolver login en el return
  return {
    // state
    token,
    user,
    // getters
    isAuthenticated,
    // acciones
    login,
    logout,
    // helper para usar en el router
    _applyTokenToClients,
  };
});
