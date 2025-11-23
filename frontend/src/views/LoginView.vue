<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg border border-gray-700 w-full max-w-md">
      <h1 class="text-3xl font-bold mb-6 text-center text-white">Admin Login</h1>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-gray-400 mb-2">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          >
        </div>

        <div>
          <label class="block text-gray-400 mb-2">Password</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full bg-gray-700 border border-gray-600 rounded px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          >
        </div>

        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors disabled:opacity-50"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const handleLogin = async () => {
  loading.value = true;
  error.value = '';

  const success = await authStore.login(email.value, password.value);
  if (!success) {
    error.value = 'Invalid credentials';
  }

  loading.value = false;
};
</script>
