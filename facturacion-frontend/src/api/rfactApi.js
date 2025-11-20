import { rfactHttp } from './http';

// Listar facturas
export async function listarFacturas() {
  const res = await rfactHttp.get('/facturacion/facturas');
  return res.data;
}

// Obtener factura por CUF
export async function obtenerFacturaPorCuf(cuf) {
  const res = await rfactHttp.get(`/facturacion/facturas/${cuf}`);
  return res.data;
}

// Enviar factura (payload debe seguir FacturaRequest)
export async function enviarFactura(facturaPayload) {
  const res = await rfactHttp.post('/facturacion/facturas', facturaPayload);
  return res.data;
}
