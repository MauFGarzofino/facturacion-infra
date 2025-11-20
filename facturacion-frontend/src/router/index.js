import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

import LoginView from '../views/LoginView.vue';
import DashboardView from '../views/DashboardView.vue';
import EmpresasView from '../views/EmpresasView.vue';
import RecepcionView from '../views/RecepcionView.vue';
import NotificacionesView from '../views/NotificacionesView.vue';

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  {
    path: '/',
    component: DashboardView,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/empresas' },
      { path: 'empresas', name: 'empresas', component: EmpresasView },
      { path: 'recepcion', name: 'recepcion', component: RecepcionView },
      { path: 'notificaciones', name: 'notificaciones', component: NotificacionesView },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth) {
    if (!auth.isAuthenticated) {
      return next({ name: 'login' });
    }
    // Asegurar que axios tenga el token cuando recargas la página
    auth._applyTokenToClients();
  }

  if (to.name === 'login' && auth.isAuthenticated) {
    return next({ name: 'empresas' });
  }

  next();
});


export default router;
