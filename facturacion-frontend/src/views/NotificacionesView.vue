<template>
  <section>
    <h1>Notificaciones por correo</h1>

    <h2>Configurar canal de email de empresa</h2>
    <form @submit.prevent="guardarEmail" class="form">
      <label>
        ID de empresa (empresaId / NIT empresa)
        <input v-model="empresaId" type="text" required />
      </label>

      <label>
        Correo(s) destino (separados por coma)
        <input v-model="emailsTexto" type="text" required />
      </label>

      <label class="checkbox">
        <input v-model="enabled" type="checkbox" />
        Habilitar canal de email
      </label>

      <button :disabled="loadingConfig">
        {{ loadingConfig ? 'Guardando...' : 'Guardar configuración' }}
      </button>

      <p v-if="okConfig" class="ok">Configuración guardada ✅</p>
      <p v-if="errorConfig" class="error">{{ errorConfig }}</p>
    </form>

    <h2>Reenviar correo de notificación</h2>
    <form @submit.prevent="reenviar" class="form">
      <label>
        ID de evento de notificación (NotificationEvent._id)
        <input v-model="notificationId" type="text" required />
      </label>

      <button :disabled="loadingResend">
        {{ loadingResend ? 'Reenviando...' : 'Reenviar correo' }}
      </button>

      <p v-if="okResend" class="ok">Correo reenviado ✅</p>
      <p v-if="errorResend" class="error">{{ errorResend }}</p>
    </form>

    <p class="hint">
      Los correos enviados se pueden ver en Mailhog:
      <strong>http://localhost:8025</strong>
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import {
  actualizarCanalEmail,
  reenviarEmailNotificacion,
} from '../api/notifApi';

const empresaId = ref('');
const emailsTexto = ref('');
const enabled = ref(true);

const loadingConfig = ref(false);
const errorConfig = ref('');
const okConfig = ref(false);

const notificationId = ref('');
const loadingResend = ref(false);
const errorResend = ref('');
const okResend = ref(false);

const guardarEmail = async () => {
  loadingConfig.value = true;
  errorConfig.value = '';
  okConfig.value = false;

  try {
    const to = emailsTexto.value
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);

    await actualizarCanalEmail(empresaId.value, {
      enabled: enabled.value,
      to,
    });

    okConfig.value = true;
  } catch (e) {
    console.error(e);
    errorConfig.value = e.response?.data?.message || 'Error al guardar configuración';
  } finally {
    loadingConfig.value = false;
  }
};

const reenviar = async () => {
  loadingResend.value = true;
  errorResend.value = '';
  okResend.value = false;

  try {
    await reenviarEmailNotificacion(notificationId.value);
    okResend.value = true;
  } catch (e) {
    console.error(e);
    errorResend.value = e.response?.data?.message || 'Error al reenviar correo';
  } finally {
    loadingResend.value = false;
  }
};
</script>

<style scoped>
.form {
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-bottom: 2rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}
button {
  align-self: flex-start;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  border: none;
  background: #2563eb;
  color: white;
  cursor: pointer;
}
.checkbox {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.ok {
  color: #16a34a;
}
.error {
  color: #dc2626;
}
.hint {
  font-size: 0.9rem;
  color: #4b5563;
}
</style>
