<!-- src/views/DashboardView.vue -->
<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">⚡</div>
        <div>
          <h2 class="sidebar-title">Facturación</h2>
          <p class="sidebar-subtitle">Panel general</p>
        </div>
      </div>

      <nav class="menu">
        <ul>
          <li>
            <RouterLink
              to="/empresas"
              class="menu-link"
              active-class="menu-link-active"
            >
              <span class="menu-icon">🏢</span>
              <span>Empresas</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/recepcion"
              class="menu-link"
              active-class="menu-link-active"
            >
              <span class="menu-icon">📄</span>
              <span>Recepción de facturas</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/notificaciones"
              class="menu-link"
              active-class="menu-link-active"
            >
              <span class="menu-icon">📬</span>
              <span>Notificaciones</span>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <div class="sidebar-footer">
        <button class="logout-btn" @click="handleLogout">
          <span class="logout-icon">⏏</span>
          <span>Cerrar sesión</span>
        </button>
      </div>
    </aside>

    <!-- Contenido principal -->
    <main class="content">
      <header class="topbar">
        <div>
          <h1>Dashboard de Facturación</h1>
          <p v-if="username" class="user-text">
            Sesión iniciada como <strong>{{ username }}</strong>
          </p>
        </div>

        <div v-if="username" class="user-chip">
          <span class="user-avatar">
            {{ username.charAt(0).toUpperCase() }}
          </span>
          <span class="user-name">{{ username }}</span>
        </div>
      </header>

      <!-- Aquí se dibujan EmpresasView / RecepcionView / NotificacionesView -->
      <section class="view-container">
        <div class="view-card">
          <RouterView />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { computed } from 'vue';
import { useAuthStore } from '../stores/authStore';

const router = useRouter();
const auth = useAuthStore();

const username = computed(
  () => auth.user?.username || auth.user?.email || ''
);

function handleLogout() {
  if (typeof auth.logout === 'function') {
    auth.logout();
  } else {
    auth.token = null;
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  }

  router.push({ name: 'login' });
}
</script>

<style scoped>
:root {
  --bg: #0f172a;
  --bg-soft: #0b1120;
  --primary: #4f46e5;
  --primary-soft: rgba(79, 70, 229, 0.12);
  --accent: #22c55e;
  --text-main: #e5e7eb;
  --text-muted: #9ca3af;
  --border-soft: rgba(148, 163, 184, 0.2);
}

/* Layout general */
.layout {
  display: flex;
  min-height: 100vh;
  background: radial-gradient(circle at top left, #1d283a 0, #020617 45%, #020617 100%);
  color: var(--text-main);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Sidebar */
.sidebar {
  width: 260px;
  padding: 1.5rem 1.25rem;
  background: linear-gradient(180deg, #020617 0%, #020617 45%, #030712 100%);
  border-right: 1px solid var(--border-soft);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.25rem;
}

.sidebar-logo {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 30% 0, #4f46e5, #22c55e);
  font-size: 1.4rem;
}

.sidebar-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.sidebar-subtitle {
  margin: 0.15rem 0 0;
  font-size: 0.78rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* Menú */
.menu ul {
  list-style: none;
  padding: 0;
  margin: 0.75rem 0 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.55rem 0.7rem;
  border-radius: 0.55rem;
  text-decoration: none;
  color: var(--text-muted);
  font-size: 0.92rem;
  transition:
    background 0.18s ease,
    color 0.18s ease,
    transform 0.12s ease;
}

.menu-link:hover {
  background: rgba(148, 163, 184, 0.08);
  color: #e5e7eb;
  transform: translateX(2px);
}

.menu-link-active {
  background: var(--primary-soft);
  color: #e5e7eb;
  font-weight: 500;
  box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.4);
}

.menu-link-active .menu-icon {
  background: rgba(79, 70, 229, 0.2);
}

.menu-icon {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  background: rgba(15, 23, 42, 0.8);
}

/* Footer sidebar */
.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid rgba(31, 41, 55, 0.9);
}

.logout-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.6rem 0.7rem;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  background: rgba(239, 68, 68, 0.14);
  color: #fecaca;
  transition:
    background 0.15s ease,
    transform 0.1s ease,
    box-shadow 0.15s ease;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.22);
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35);
}

.logout-icon {
  font-size: 1rem;
}

/* Contenido */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(20px);
}

/* Topbar */
.topbar {
  padding: 1rem 1.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(51, 65, 85, 0.9);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.8);
}

.topbar h1 {
  margin: 0;
  font-size: 1.25rem;
  letter-spacing: 0.01em;
}

.user-text {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* Chip de usuario */
.user-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.4);
  background: rgba(15, 23, 42, 0.75);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: #e5e7eb;
  background: linear-gradient(135deg, #4f46e5, #22c55e);
}

.user-name {
  font-size: 0.85rem;
}

/* Contenedor de vistas */
.view-container {
  padding: 1.6rem 1.75rem 1.8rem;
  flex: 1;
  overflow: auto;
}

.view-card {
  width: 100%;
  min-height: calc(100vh - 120px);
  border-radius: 1rem;
  padding: 1.5rem;
  background: radial-gradient(circle at top left, rgba(15, 23, 42, 0.95), #020617);
  border: 1px solid rgba(51, 65, 85, 0.9);
  box-shadow:
    0 30px 80px rgba(15, 23, 42, 0.9),
    0 0 0 1px rgba(148, 163, 184, 0.1);
}

/* Responsive */
@media (max-width: 900px) {
  .layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    flex-direction: row;
    align-items: center;
    padding: 0.75rem 1rem;
    gap: 0.75rem;
  }

  .sidebar-header {
    flex: 0 0 auto;
  }

  .menu ul {
    flex-direction: row;
  }

  .sidebar-footer {
    margin-top: 0;
    margin-left: auto;
    border-top: none;
  }

  .view-card {
    min-height: auto;
  }
}
</style>
