<!-- src/views/EmpresasView.vue -->
<template>
  <div class="empresas-container">

    <h2 class="section-title">Empresas registradas</h2>

    <!-- Loading -->
    <div v-if="loading" class="loader-box">
      <div class="loader"></div>
      <p>Cargando empresas...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-box">
      <span>⚠ {{ error }}</span>
    </div>

    <!-- Tabla -->
    <div v-else class="table-wrapper">
      <table class="modern-table">
        <thead>
          <tr>
            <th>NIT</th>
            <th>Razón Social</th>
            <th>Correo</th>
            <th>Estado</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="em in empresas" :key="em.nit">
            <td>{{ em.nit }}</td>
            <td>{{ em.razonSocial }}</td>
            <td>{{ em.correo || '—' }}</td>
            <td>
              <span :class="['badge', em.estado === 'activo' ? 'badge-active' : 'badge-inactive']">
                {{ em.estado }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchEmpresas } from "../api/empresasApi";

const empresas = ref([]);
const loading = ref(false);
const error = ref("");

onMounted(async () => {
  loading.value = true;
  try {
    empresas.value = await fetchEmpresas();
  } catch (e) {
    console.error(e);
    error.value = "No se pudieron cargar las empresas";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Contenedor */
.empresas-container {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

/* Título */
.section-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #e5e7eb;
  margin: 0 0 1rem;
}

/* Loader */
.loader-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 1rem;
  color: #9ca3af;
}

.loader {
  width: 28px;
  height: 28px;
  border: 4px solid rgba(148,163,184,0.3);
  border-top-color: #4f46e5;
  border-radius: 999px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error */
.error-box {
  padding: 1rem;
  background: rgba(239, 68, 68, 0.18);
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 8px;
  color: #fecaca;
}

/* Tabla moderna */
.table-wrapper {
  width: 100%;
  overflow: hidden;
  border-radius: 10px;
  border: 1px solid rgba(148,163,184,0.15);
  background: rgba(15,23,42,0.55);
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.35);
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  color: #e5e7eb;
  font-size: 0.92rem;
}

.modern-table thead {
  background: rgba(79,70,229,0.18);
}

.modern-table th {
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #c7d2fe;
  border-bottom: 1px solid rgba(148,163,184,0.2);
}

.modern-table td {
  padding: 0.75rem;
  border-bottom: 1px solid rgba(148,163,184,0.08);
}

.modern-table tbody tr:hover {
  background: rgba(148,163,184,0.08);
  transition: 0.15s ease-in-out;
}

/* Estado */
.badge {
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.badge-active {
  background: rgba(34,197,94,0.18);
  color: #4ade80;
}

.badge-inactive {
  background: rgba(239,68,68,0.15);
  color: #fca5a5;
}
</style>
