<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <nav class="bg-gray-800 border-b border-gray-700">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-blue-400">Aerostats</router-link>
            <div class="ml-10 flex items-baseline space-x-4">
              <router-link to="/" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Live Status</router-link>
              <router-link to="/results" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Results</router-link>
            </div>
          </div>
          <div>
            <router-link v-if="!authStore.isAuthenticated" to="/login" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Admin Login</router-link>
            <router-link v-else to="/admin" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Dashboard</router-link>
          </div>
        </div>
      </div>
    </nav>

    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth';
const authStore = useAuthStore();
</script>

<style>
/* Global styles if needed */
</style>
