<template>
  <div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700 h-full">
    <h2 class="text-xl font-semibold mb-4 text-white">Team Status Management</h2>

    <!-- Class Tabs -->
    <div class="flex justify-center mb-4 border-b border-gray-700">
      <button
        v-for="cls in ['regular', 'advanced', 'micro']"
        :key="cls"
        @click="filterClass = cls"
        class="px-6 py-3 text-lg font-semibold capitalize transition-colors duration-200 border-b-2"
        :class="[
          filterClass === cls
            ? 'text-blue-400 border-blue-400'
            : 'text-gray-400 border-transparent hover:text-gray-200 hover:border-gray-600'
        ]"
      >
        {{ cls }} Class
      </button>
    </div>

    <div class="mb-4">
      <input
        v-model="search"
        placeholder="Search team..."
        class="bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white w-full"
      >
    </div>

    <div class="overflow-y-auto max-h-[800px] space-y-2">
      <div v-for="team in filteredTeams" :key="team.team_id" class="bg-gray-750 p-3 rounded border border-gray-700 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <div class="font-bold text-white">{{ team.name }}</div>
          <div class="text-xs text-gray-400">{{ team.university }} ({{ team.class }})</div>
        </div>

        <div class="flex items-center gap-2 w-full sm:w-auto bg-gray-900/50 p-1 rounded-lg">
          <button
            @click="moveStatus(team, 'prev')"
            :disabled="orderedStatuses.indexOf(team.battery_status) === 0"
            class="p-2 rounded-md bg-gray-700 hover:bg-blue-600 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-gray-700 text-white transition-colors"
            title="Previous Status"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          </button>

          <span class="text-sm text-white min-w-[200px] text-center font-medium select-none">
            {{ formatStatus(team.battery_status) }}
          </span>

          <button
            @click="moveStatus(team, 'next')"
            :disabled="orderedStatuses.indexOf(team.battery_status) === orderedStatuses.length - 1"
            class="p-2 rounded-md bg-gray-700 hover:bg-blue-600 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-gray-700 text-white transition-colors"
            title="Next Status"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useDataStore } from '../stores/data';
import api from '../api';
import { TeamBatteryStatus } from '../types';

const dataStore = useDataStore();
const search = ref('');
const filterClass = ref('regular');

const orderedStatuses: TeamBatteryStatus[] = [
  TeamBatteryStatus.NotClassified,
  TeamBatteryStatus.WaitingForInspectionCall,
  TeamBatteryStatus.CalledForInspection,
  TeamBatteryStatus.InInspection,
  TeamBatteryStatus.InFlightQueue,
  TeamBatteryStatus.Flying,
  TeamBatteryStatus.PostFlightInspection,
  TeamBatteryStatus.Flown
];

const formatStatus = (status: string) => {
  return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};

const filteredTeams = computed(() => {
  return dataStore.teams.filter(team => {
    const matchesSearch = team.name.toLowerCase().includes(search.value.toLowerCase()) ||
                          team.university.toLowerCase().includes(search.value.toLowerCase());
    const matchesClass = team.class === filterClass.value;
    return matchesSearch && matchesClass;
  });
});

const updateStatus = async (teamId: string, newStatus: string) => {
  try {
    // Optimistic update
    const team = dataStore.teams.find(t => t.team_id === teamId);
    if (team) team.battery_status = newStatus as TeamBatteryStatus;

    await api.patch(`/admin/team/${teamId}/battery_status`, {
      battery_status: newStatus
    });
  } catch (error) {
    console.error('Failed to update team status:', error);
    alert('Failed to update status');
    dataStore.fetchAll(); // Revert on error
  }
};

const moveStatus = (team: any, direction: 'prev' | 'next') => {
  const currentIndex = orderedStatuses.indexOf(team.battery_status);
  if (currentIndex === -1) return;

  let newIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;

  // Clamp index
  if (newIndex < 0) newIndex = 0;
  if (newIndex >= orderedStatuses.length) newIndex = orderedStatuses.length - 1;

  if (newIndex !== currentIndex) {
    const nextStatus = orderedStatuses[newIndex];
    if (nextStatus) {
      updateStatus(team.team_id, nextStatus);
    }
  }
};
</script>
