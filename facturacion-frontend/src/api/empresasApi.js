// src/api/empresasApi.js
import { empresasHttp } from './http';
import { getAuthHeaders } from './authHeaders';

// Obtener todas las empresas
export async function fetchEmpresas() {
  const res = await empresasHttp.get('/', {
    headers: getAuthHeaders(),
  });
  return res.data; // array de empresas
}

// Obtener una empresa por NIT
export async function fetchEmpresaByNit(nit) {
  const res = await empresasHttp.get(`/${nit}`, {
    headers: getAuthHeaders(),
  });
  return res.data; // empresa
}

// Crear empresa (para rol admin)
export async function createEmpresa(payload) {
  const res = await empresasHttp.post('/', payload, {
    headers: {
      ...getAuthHeaders(),
      'Content-Type': 'application/json',
    },
  });
  return res.data;
}

// Actualizar empresa
export async function updateEmpresa(nit, payload) {
  const res = await empresasHttp.patch(`/${nit}`, payload, {
    headers: {
      ...getAuthHeaders(),
      'Content-Type': 'application/json',
    },
  });
  return res.data;
}

// Eliminar empresa
export async function deleteEmpresa(nit) {
  const res = await empresasHttp.delete(`/${nit}`, {
    headers: getAuthHeaders(),
  });
  return res.data;
}
