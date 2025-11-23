<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold mb-8 text-center text-blue-400">Competition Results</h1>

    <div v-if="dataStore.loading && !dataStore.releasedResults.regular.length" class="text-center text-gray-400">Loading results...</div>

    <div v-else>
      <!-- Class Tabs -->
      <div class="flex justify-center mb-8 border-b border-gray-700">
        <button
          v-for="cls in ['regular', 'advanced', 'micro']"
          :key="cls"
          @click="selectClass(cls)"
          class="px-6 py-3 text-lg font-semibold capitalize transition-colors duration-200 border-b-2"
          :class="[
            selectedClass === cls
              ? 'text-blue-400 border-blue-400'
              : 'text-gray-400 border-transparent hover:text-gray-200 hover:border-gray-600'
          ]"
        >
          {{ cls }} Class
        </button>
      </div>

      <!-- Round Selection -->
      <div v-if="availableRounds.length > 0" class="flex flex-wrap justify-center gap-4 mb-8">
        <button
          v-for="round in availableRounds"
          :key="round"
          @click="selectedRound = round"
          class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200"
          :class="[
            selectedRound === round
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          ]"
        >
          Round {{ round }}
        </button>
      </div>

      <!-- Results Display -->
      <div v-if="currentResult" class="max-w-4xl mx-auto">
        <div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-2xl font-bold text-white capitalize">{{ selectedClass }} Class - Round {{ selectedRound }}</h3>
            <span class="text-sm text-gray-400">Total Teams: {{ currentResult.results.length }}</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="text-gray-400 border-b border-gray-600">
                  <th class="p-3 w-20">Rank</th>
                  <th class="p-3">Team</th>
                  <th class="p-3 text-right">Score</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="result in currentResult.results"
                  :key="result.team_id"
                  class="border-b border-gray-700 last:border-0 hover:bg-gray-750 transition-colors"
                >
                  <td class="p-3">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-8 h-8 flex items-center justify-center rounded-full font-bold shrink-0"
                        :class="[
                          result.placing === 1 ? 'bg-yellow-500 text-black' :
                          result.placing === 2 ? 'bg-gray-400 text-black' :
                          result.placing === 3 ? 'bg-orange-700 text-white' :
                          'text-gray-400'
                        ]"
                      >
                        {{ result.placing }}
                      </div>

                      <!-- Position Change Indicator -->
                      <div class="w-12 text-xs font-bold flex items-center">
                        <span v-if="getPositionChange(result.team_id, result.placing) !== null && getPositionChange(result.team_id, result.placing)! > 0" class="text-green-500 flex items-center">
                          ▲ {{ getPositionChange(result.team_id, result.placing) }}
                        </span>
                        <span v-else-if="getPositionChange(result.team_id, result.placing) !== null && getPositionChange(result.team_id, result.placing)! < 0" class="text-red-500 flex items-center">
                          ▼ {{ Math.abs(getPositionChange(result.team_id, result.placing)!) }}
                        </span>
                        <span v-else-if="getPositionChange(result.team_id, result.placing) === 0" class="text-gray-600 pl-1">
                          -
                        </span>
                      </div>
                    </div>
                  </td>
                  <td class="p-3">
                    <div class="font-semibold text-white">{{ getTeamName(result.team_id) }}</div>
                    <div class="text-xs text-gray-400">{{ getTeamUniversity(result.team_id) }}</div>
                  </td>
                  <td class="p-3 text-right font-mono text-xl font-bold text-green-400">
                    {{ result.score.toFixed(2) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-else-if="availableRounds.length === 0" class="text-center text-gray-500 italic mt-12">
        No results released for {{ selectedClass }} class yet.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useDataStore } from '../stores/data';
import type { Team } from '../types';

const dataStore = useDataStore();
const selectedClass = ref('regular');
const selectedRound = ref<number | null>(null);

onMounted(async () => {
  await dataStore.fetchAll();
  updateSelectedRound();
});

const availableRounds = computed(() => {
  const results = (dataStore.releasedResults as any)[selectedClass.value] || [];
  return results.map((r: any) => r.round_number).sort((a: number, b: number) => a - b);
});

const currentResult = computed(() => {
  if (!selectedRound.value) return null;
  const results = (dataStore.releasedResults as any)[selectedClass.value] || [];
  return results.find((r: any) => r.round_number === selectedRound.value);
});

const selectClass = (cls: string) => {
  selectedClass.value = cls;
  updateSelectedRound();
};

const updateSelectedRound = () => {
  const rounds = availableRounds.value;
  if (rounds.length > 0) {
    // Select the last round by default
    selectedRound.value = rounds[rounds.length - 1];
  } else {
    selectedRound.value = null;
  }
};

// Watch for data changes to update selected round if it wasn't set
watch(() => dataStore.releasedResults, () => {
  if (!selectedRound.value) {
    updateSelectedRound();
  }
}, { deep: true });

const getTeam = (teamId: string) => {
  return dataStore.teams.find((t: Team) => t.team_id === teamId);
};

const getTeamName = (teamId: string) => {
  const team = getTeam(teamId);
  return team ? team.name : 'Unknown Team';
};

const getTeamUniversity = (teamId: string) => {
  const team = getTeam(teamId);
  return team ? team.university : '';
};

const getPositionChange = (teamId: string, currentPlacing: number): number | null => {
  if (!selectedRound.value || selectedRound.value <= 1) return null;

  const cls = selectedClass.value;
  const results = (dataStore.releasedResults as any)[cls] || [];
  const prevRoundNum = selectedRound.value - 1;
  const prevRound = results.find((r: any) => r.round_number === prevRoundNum);

  if (!prevRound) return null;

  const prevResult = prevRound.results.find((r: any) => r.team_id === teamId);
  if (!prevResult) return null;

  return prevResult.placing - currentPlacing;
};
</script>
