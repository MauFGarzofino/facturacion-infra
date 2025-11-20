import { notifHttp } from './http';

// Configurar canal de email para una empresa
// data: { enabled: boolean, to: ['correo@empresa.bo', ...] }
export async function actualizarCanalEmail(empresaId, data) {
  const res = await notifHttp.put(
    `/v1/companies/${empresaId}/channels/email`,
    data,
  );
  return res.data;
}

// Reenviar email para un evento de notificación (id = _id en Mongo)
export async function reenviarEmailNotificacion(id) {
  const res = await notifHttp.post(`/v1/notifications/${id}/resend/email`);
  return res.data;
}
