import axios from 'axios';

export const authHttp = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL,      // http://localhost:8080/auth
});

export const empresasHttp = axios.create({
  baseURL: import.meta.env.VITE_EMPRESAS_API_URL,  // http://localhost:8080/empresas
});

export const rfactHttp = axios.create({
  baseURL: import.meta.env.VITE_RFACT_API_URL,     // http://localhost:8080/recepcion
});

export const notifHttp = axios.create({
  baseURL: import.meta.env.VITE_NOTIF_API_URL,     // http://localhost:8080/notificaciones
});
