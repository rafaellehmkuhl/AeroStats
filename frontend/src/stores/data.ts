import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '../api';
import type { Team, CurrentFlight, BatteryRounds, ReleasedBatteries } from '../types';
import { CurrentFlightStatus } from '../types';

export const useDataStore = defineStore('data', () => {
    const teams = ref<Team[]>([]);
    const currentFlight = ref<CurrentFlight>({ team: null, status: CurrentFlightStatus.CompetitionPaused });
    const currentRounds = ref<BatteryRounds>({ regular: 1, advanced: 1, micro: 1 });
    const lastReleasedRounds = ref<BatteryRounds>({ regular: 0, advanced: 0, micro: 0 });
    const releasedResults = ref<ReleasedBatteries>({ regular: [], advanced: [], micro: [] });
    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchAll = async () => {
        loading.value = true;
        try {
            const [teamsRes, flightRes, roundsRes, lastReleasedRes, resultsRes] = await Promise.all([
                api.get('/team_battery_status'),
                api.get('/current_flight_status'),
                api.get('/current_battery_round'),
                api.get('/last_released_battery_round'),
                api.get('/data_released_batteries')
            ]);

            teams.value = teamsRes.data;
            currentFlight.value = flightRes.data;
            currentRounds.value = roundsRes.data;
            lastReleasedRounds.value = lastReleasedRes.data;
            releasedResults.value = resultsRes.data;
            error.value = null;
        } catch (err: any) {
            console.error('Error fetching data:', err);
            error.value = 'Failed to fetch data';
        } finally {
            loading.value = false;
        }
    };

    const startPolling = (intervalMs = 5000) => {
        fetchAll();
        setInterval(() => {
            fetchAll();
        }, intervalMs);
    };

    return {
        teams,
        currentFlight,
        currentRounds,
        lastReleasedRounds,
        releasedResults,
        loading,
        error,
        fetchAll,
        startPolling
    };
});
