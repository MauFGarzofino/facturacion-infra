<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Sistema de Facturación</h1>
      <p>Inicia sesión para continuar</p>

      <form @submit.prevent="handleSubmit">
        <label>
          Usuario
          <input v-model="username" type="text" required />
        </label>

        <label>
          Contraseña
          <input v-model="password" type="password" required />
        </label>

        <button :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const router = useRouter();
const auth = useAuthStore();

onMounted(() => {
  if (auth.isAuthenticated) {
    router.push({ name: 'empresas' });
  }
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  try {
    await auth.login(username.value, password.value);
    router.push({ name: 'empresas' });
  } catch (e) {
    console.error(e);
    error.value =
      e.response?.data?.detail ||
      e.response?.data?.message ||
      'Error al iniciar sesión';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e5e7eb;
}
.login-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 380px;
}
h1 {
  margin: 0 0 0.5rem;
}
p {
  margin: 0 0 1.5rem;
}
label {
  display: block;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
input {
  width: 100%;
  padding: 0.6rem;
  margin-top: 0.3rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}
button {
  width: 100%;
  padding: 0.7rem;
  margin-top: 0.5rem;
  border-radius: 999px;
  border: none;
  background: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
}
button:disabled {
  opacity: 0.7;
  cursor: default;
}
.error {
  margin-top: 0.75rem;
  color: #dc2626;
  font-size: 0.85rem;
}
</style>
