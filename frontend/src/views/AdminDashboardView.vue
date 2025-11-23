<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-white">Admin Dashboard</h1>
      <button @click="authStore.logout()" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">
        Logout
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left Column -->
      <div class="space-y-8">
        <AdminCurrentFlight />
        <AdminRounds />
        <AdminUpload />
      </div>

      <!-- Right Column -->
      <div>
        <AdminTeamStatus />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useDataStore } from '../stores/data';
import AdminCurrentFlight from '../components/AdminCurrentFlight.vue';
import AdminRounds from '../components/AdminRounds.vue';
import AdminUpload from '../components/AdminUpload.vue';
import AdminTeamStatus from '../components/AdminTeamStatus.vue';

const authStore = useAuthStore();
const dataStore = useDataStore();

onMounted(() => {
  dataStore.fetchAll();
});
</script>
