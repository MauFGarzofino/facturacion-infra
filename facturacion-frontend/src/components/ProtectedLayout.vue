<template>
  <div class="layout">
    <AppNavbar />

    <div class="content-wrapper">
      <aside class="sidebar">
        <h2>Menú</h2>
        <ul>
          <li><RouterLink to="/dashboard">Dashboard</RouterLink></li>
          <li><RouterLink to="/empresas">Empresas</RouterLink></li>
          <li><RouterLink to="/recepcion">Recepción de facturas</RouterLink></li>
          <li><RouterLink to="/notificaciones">Notificaciones</RouterLink></li>
        </ul>
      </aside>

      <main class="main">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import AppNavbar from './AppNavbar.vue';
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  flex: 1;
  display: grid;
  grid-template-columns: 220px 1fr;
}

.sidebar {
  background: #f3f4f6;
  padding: 1rem;
  border-right: 1px solid #e5e7eb;
}

.sidebar h2 {
  margin-top: 0;
  font-size: 1rem;
  margin-bottom: 0.75rem;
}

.sidebar ul {
  list-style: none;
  padding-left: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.sidebar a {
  text-decoration: none;
  color: #374151;
  font-size: 0.9rem;
}

.sidebar a.router-link-active {
  font-weight: 600;
  color: #111827;
}

.main {
  padding: 1.5rem;
  background: #ffffff;
}
</style>
