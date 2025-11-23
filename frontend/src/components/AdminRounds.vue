<template>
  <div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
    <h2 class="text-xl font-semibold mb-4 text-white">Active Rounds</h2>

    <div class="space-y-4">
      <div v-for="cls in ['regular', 'advanced', 'micro']" :key="cls" class="flex items-center justify-between">
        <span class="text-gray-300 capitalize w-24">{{ cls }}</span>
        <div class="flex items-center gap-2">
          <button
            @click="updateRound(cls, -1)"
            class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded"
          >-</button>
          <span class="text-xl font-bold text-white w-8 text-center">{{ getRound(cls) }}</span>
          <button
            @click="updateRound(cls, 1)"
            class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded"
          >+</button>
        </div>
        <button
          @click="generateResults(cls)"
          class="ml-4 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
        >
          Generate Results
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDataStore } from '../stores/data';
import api from '../api';

const dataStore = useDataStore();

const getRound = (cls: string) => {
  return (dataStore.currentRounds as any)[cls];
};

const updateRound = async (cls: string, change: number) => {
  const current = getRound(cls);
  const newRound = current + change;
  if (newRound < 1) return;

  try {
    await api.patch('/admin/current_battery_round', {
      class: cls,
      round_number: newRound
    });
    await dataStore.fetchAll();
  } catch (error) {
    console.error('Failed to update round:', error);
  }
};

const generateResults = async (cls: string) => {
  const current = getRound(cls);
  const defaultRound = current + 1;

  const roundStr = prompt(`Enter round number to generate results for ${cls} class:`, defaultRound.toString());
  if (roundStr === null) return; // User cancelled

  const roundNum = parseInt(roundStr);
  if (isNaN(roundNum) || roundNum < 1) {
    alert("Invalid round number.");
    return;
  }

  if (!confirm(`Are you sure you want to generate random results for ${cls} class, round ${roundNum}? This will overwrite any existing data for this round.`)) {
    return;
  }

  try {
    const response = await api.post('/admin/generate_battery_results', {
      class: cls,
      round_number: roundNum
    });

    if (response.data.status === 'no_teams') {
      alert(`No teams found in ${cls} class. Cannot generate results.`);
    } else {
      alert(response.data.message);
      await dataStore.fetchAll();
    }
  } catch (error) {
    console.error('Failed to generate results:', error);
    alert('Failed to generate results. See console for details.');
  }
};
</script>
