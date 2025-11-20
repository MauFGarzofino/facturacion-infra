<template>
  <section>
    <h1>Recepción de facturación</h1>

    <form @submit.prevent="enviar" class="form">
      <div class="grid">
        <label>
          CUF
          <input v-model="form.cuf" type="text" required />
        </label>

        <label>
          CUFD
          <input v-model="form.cufd" type="text" required />
        </label>
      </div>

      <div class="grid">
        <label>
          NIT Emisor
          <input v-model="form.nitEmisor" type="text" required />
        </label>

        <label>
          NIT Empresa
          <input v-model="form.nitEmpresa" type="text" required />
        </label>
      </div>

      <div class="grid">
        <label>
          Código Sucursal
          <input v-model="form.codigoSucursal" type="text" required />
        </label>

        <label>
          Código Punto Venta
          <input v-model="form.codigoPuntoVenta" type="text" required />
        </label>
      </div>

      <label>
        Razón Social Emisor
        <input v-model="form.razonSocialEmisor" type="text" required />
      </label>

      <label>
        Código de Control (opcional)
        <input v-model="form.codigoControl" type="text" />
      </label>

      <h2>Detalle (único ítem para demo)</h2>

      <label>
        Descripción
        <input v-model="form.detalleDescripcion" type="text" required />
      </label>

      <div class="grid">
        <label>
          Cantidad
          <input v-model.number="form.detalleCantidad" type="number" min="1" required />
        </label>

        <label>
          Precio Unitario
          <input v-model.number="form.detallePrecioUnitario" type="number" min="0.01" step="0.01" required />
        </label>
      </div>

      <p><strong>Monto total calculado:</strong> {{ montoTotal.toFixed(2) }} Bs</p>

      <button :disabled="loading">
        {{ loading ? 'Enviando...' : 'Enviar factura' }}
      </button>

      <p v-if="ok" class="ok">Factura registrada correctamente ✅</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <h2>Últimas facturas</h2>
    <button @click="cargarFacturas" :disabled="loadingLista">
      {{ loadingLista ? 'Cargando...' : 'Actualizar lista' }}
    </button>

    <ul v-if="facturas.length" class="lista">
      <li v-for="f in facturas" :key="f.id || f.cuf || f.CUF">
        CUF: {{ f.cuf || f.CUF }} — NIT Empresa: {{ f.nitEmpresa || f.nit_empresa }} — 
        Monto: {{ f.montoTotal || f.monto_total }} Bs — Estado: {{ f.estado }}
      </li>
    </ul>

    <p v-else-if="!loadingLista">No hay facturas registradas.</p>
  </section>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue';
import { enviarFactura, listarFacturas } from '../api/rfactApi';

const form = reactive({
  cuf: '',
  cufd: '',
  nitEmisor: '',
  nitEmpresa: '',
  codigoSucursal: '',
  codigoPuntoVenta: '',
  razonSocialEmisor: '',
  codigoControl: '',
  detalleDescripcion: '',
  detalleCantidad: 1,
  detallePrecioUnitario: 0,
});

const montoTotal = computed(
  () => (form.detalleCantidad || 0) * (form.detallePrecioUnitario || 0),
);

const loading = ref(false);
const loadingLista = ref(false);
const error = ref('');
const ok = ref(false);
const facturas = ref([]);

const enviar = async () => {
  loading.value = true;
  error.value = '';
  ok.value = false;

  try {
    const payload = {
      cuf: form.cuf,
      cufd: form.cufd,
      nit_emisor: form.nitEmisor,
      codigo_sucursal: form.codigoSucursal,
      codigo_pv: form.codigoPuntoVenta,
      razon_social_emisor: form.razonSocialEmisor,
      fecha_emision: new Date().toISOString(), // time.Time compatible
      nit_empresa: form.nitEmpresa,
      monto_total: montoTotal.value,
      codigo_control: form.codigoControl || undefined,
      detalles: [
        {
          descripcion: form.detalleDescripcion,
          cantidad: form.detalleCantidad,
          precio_unitario: form.detallePrecioUnitario,
        },
      ],
    };

    await enviarFactura(payload);
    ok.value = true;
    await cargarFacturas();
  } catch (e) {
    console.error(e);
    error.value = e.response?.data?.error || e.response?.data?.message || 'Error al enviar factura';
  } finally {
    loading.value = false;
  }
};

const cargarFacturas = async () => {
  loadingLista.value = true;
  error.value = '';
  try {
    facturas.value = await listarFacturas();
  } catch (e) {
    console.error(e);
    error.value = e.response?.data?.error || e.response?.data?.message || 'Error al obtener facturas';
  } finally {
    loadingLista.value = false;
  }
};

onMounted(cargarFacturas);
</script>

<style scoped>
h1 {
  margin-top: 0;
}
.form {
  max-width: 550px;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-bottom: 2rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.8rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}
button {
  align-self: flex-start;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  border: none;
  background: #10b981;
  color: white;
  cursor: pointer;
}
.ok {
  color: #16a34a;
}
.error {
  color: #dc2626;
}
.lista {
  margin-top: 1rem;
  padding-left: 1.2rem;
}
</style>
