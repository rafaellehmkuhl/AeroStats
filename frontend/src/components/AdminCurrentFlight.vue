<template>
  <div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
    <h2 class="text-xl font-semibold mb-4 text-white">Current Flight Control</h2>

    <div class="space-y-4">
      <div>
        <label class="block text-gray-400 mb-1">Team</label>
        <select v-model="selectedTeamId" class="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white">
          <option :value="null">None (Paused)</option>
          <option v-for="team in dataStore.teams" :key="team.team_id" :value="team.team_id">
            {{ team.name }} ({{ team.class }})
          </option>
        </select>
      </div>

      <div>
        <label class="block text-gray-400 mb-1">Status</label>
        <select v-model="selectedStatus" class="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white">
          <option v-for="status in Object.values(CurrentFlightStatus)" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </div>

      <button
        @click="updateFlight"
        :disabled="updating"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors disabled:opacity-50"
      >
        {{ updating ? 'Updating...' : 'Update Flight Status' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useDataStore } from '../stores/data';
import api from '../api';
import { CurrentFlightStatus } from '../types';

const dataStore = useDataStore();
const selectedTeamId = ref<string | null>(null);
const selectedStatus = ref<CurrentFlightStatus>(CurrentFlightStatus.CompetitionPaused);
const updating = ref(false);

// Sync with current state on load
watch(() => dataStore.currentFlight, (newVal) => {
  if (newVal) {
    selectedTeamId.value = newVal.team ? newVal.team.team_id : null;
    selectedStatus.value = newVal.status;
  }
}, { immediate: true });

const updateFlight = async () => {
  updating.value = true;
  try {
    await api.patch('/admin/current_flight', {
      team_id: selectedTeamId.value,
      status: selectedStatus.value
    });
    await dataStore.fetchAll(); // Refresh data
  } catch (error) {
    console.error('Failed to update flight:', error);
    alert('Failed to update flight');
  } finally {
    updating.value = false;
  }
};
</script>
