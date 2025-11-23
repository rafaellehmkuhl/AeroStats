<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold mb-8 text-center text-blue-400">Aerostats Live</h1>

    <!-- Current Flight -->
    <div class="bg-gray-800 rounded-lg p-6 mb-8 shadow-lg border border-gray-700">
      <h2 class="text-2xl font-semibold mb-4 text-white">Current Flight</h2>
      <div v-if="dataStore.currentFlight.status === 'competition_paused'" class="text-yellow-400 text-xl">
        Competition Paused
      </div>
      <div v-else class="flex flex-col md:flex-row items-center justify-between">
        <div class="mb-4 md:mb-0">
          <div class="text-gray-400 text-sm">Status</div>
          <div class="text-3xl font-bold text-green-400 uppercase">{{ formatStatus(dataStore.currentFlight.status) }}</div>
        </div>
        <div v-if="dataStore.currentFlight.team" class="text-center md:text-right">
          <div class="text-2xl font-bold text-white">{{ dataStore.currentFlight.team.name }}</div>
          <div class="text-gray-400">{{ dataStore.currentFlight.team.university }}</div>
          <div class="text-sm text-blue-300 mt-1">{{ dataStore.currentFlight.team.class.toUpperCase() }} Class</div>
        </div>
      </div>
    </div>

    <!-- Current Rounds -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div class="bg-gray-800 p-4 rounded-lg border border-gray-700 text-center">
        <div class="text-gray-400 mb-1">Regular Class</div>
        <div class="text-3xl font-bold text-white">Round {{ dataStore.currentRounds.regular }}</div>
      </div>
      <div class="bg-gray-800 p-4 rounded-lg border border-gray-700 text-center">
        <div class="text-gray-400 mb-1">Advanced Class</div>
        <div class="text-3xl font-bold text-white">Round {{ dataStore.currentRounds.advanced }}</div>
      </div>
      <div class="bg-gray-800 p-4 rounded-lg border border-gray-700 text-center">
        <div class="text-gray-400 mb-1">Micro Class</div>
        <div class="text-3xl font-bold text-white">Round {{ dataStore.currentRounds.micro }}</div>
      </div>
    </div>

    <!-- Team Status List -->
    <div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
      <h2 class="text-2xl font-semibold mb-4 text-white">Team Status</h2>

      <div class="mb-4 flex gap-2 overflow-x-auto pb-2">
        <button
          v-for="cls in ['all', 'regular', 'advanced', 'micro']"
          :key="cls"
          @click="filterClass = cls"
          :class="['px-4 py-2 rounded-full text-sm font-medium transition-colors',
            filterClass === cls ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600']"
        >
          {{ cls.charAt(0).toUpperCase() + cls.slice(1) }}
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="text-gray-400 border-b border-gray-700">
              <th class="p-3">Team</th>
              <th class="p-3">Class</th>
              <th class="p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="team in filteredTeams" :key="team.team_id" class="border-b border-gray-700 hover:bg-gray-750">
              <td class="p-3">
                <div class="font-bold text-white">{{ team.name }}</div>
                <div class="text-xs text-gray-400">{{ team.university }}</div>
              </td>
              <td class="p-3">
                <span :class="['px-2 py-1 rounded text-xs font-bold', getClassColor(team.class)]">
                  {{ team.class.toUpperCase() }}
                </span>
              </td>
              <td class="p-3">
                <span :class="['px-2 py-1 rounded text-xs font-bold', getStatusColor(team.battery_status)]">
                  {{ formatStatus(team.battery_status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useDataStore } from '../stores/data';
import { ClassType, TeamBatteryStatus, type Team } from '../types';

const dataStore = useDataStore();
const filterClass = ref('all');
let pollInterval: number;

onMounted(() => {
  dataStore.fetchAll();
  pollInterval = setInterval(() => dataStore.fetchAll(), 5000);
});

onUnmounted(() => {
  clearInterval(pollInterval);
});

const filteredTeams = computed(() => {
  if (filterClass.value === 'all') return dataStore.teams;
  return dataStore.teams.filter((t: Team) => t.class === filterClass.value);
});

const formatStatus = (status: string) => {
  return status.replace(/_/g, ' ');
};

const getClassColor = (cls: ClassType) => {
  switch (cls) {
    case ClassType.Regular: return 'bg-blue-900 text-blue-200';
    case ClassType.Advanced: return 'bg-purple-900 text-purple-200';
    case ClassType.Micro: return 'bg-yellow-900 text-yellow-200';
    default: return 'bg-gray-700 text-gray-300';
  }
};

const getStatusColor = (status: TeamBatteryStatus) => {
  switch (status) {
    case TeamBatteryStatus.Flying: return 'bg-green-600 text-white animate-pulse';
    case TeamBatteryStatus.InFlightQueue: return 'bg-blue-800 text-blue-100';
    case TeamBatteryStatus.InInspection: return 'bg-orange-800 text-orange-100';
    case TeamBatteryStatus.Flown: return 'bg-gray-600 text-gray-300';
    default: return 'bg-gray-700 text-gray-400';
  }
};
</script>
