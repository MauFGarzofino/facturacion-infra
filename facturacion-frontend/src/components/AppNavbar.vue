<template>
  <header class="navbar">
    <div class="navbar-left">
      <span class="logo">Facturación SIAT</span>
    </div>

    <nav class="navbar-right">
      <RouterLink to="/dashboard">Dashboard</RouterLink>
      <RouterLink to="/empresas">Empresas</RouterLink>
      <RouterLink to="/recepcion">Facturación</RouterLink>
      <RouterLink to="/notificaciones">Notificaciones</RouterLink>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.navbar {
  height: 56px;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #111827;
  color: white;
}
.logo {
  font-weight: 600;
}
.navbar-right {
  display: flex;
  gap: 1rem;
}
.navbar-right a {
  color: #e5e7eb;
  text-decoration: none;
  font-size: 0.9rem;
}
.navbar-right a.router-link-active {
  color: #fff;
  font-weight: 600;
}
</style>
