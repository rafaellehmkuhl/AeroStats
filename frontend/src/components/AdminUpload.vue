<template>
  <div class="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
    <h2 class="text-xl font-semibold mb-4 text-white">Upload Results</h2>

    <div class="space-y-4">
      <div>
        <label class="block text-gray-400 mb-1">Class</label>
        <select v-model="selectedClass" class="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white">
          <option value="regular">Regular</option>
          <option value="advanced">Advanced</option>
          <option value="micro">Micro</option>
        </select>
      </div>

      <div>
        <label class="block text-gray-400 mb-1">Round Number</label>
        <input
          v-model.number="roundNumber"
          type="number"
          min="1"
          class="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
        >
      </div>

      <div>
        <label class="block text-gray-400 mb-1">CSV File</label>
        <input
          type="file"
          accept=".csv"
          @change="handleFileChange"
          class="w-full text-gray-300"
        >
      </div>

      <button
        @click="upload"
        :disabled="uploading || !file"
        class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition-colors disabled:opacity-50"
      >
        {{ uploading ? 'Uploading...' : 'Upload Results' }}
      </button>

      <div v-if="message" :class="['text-sm mt-2', isError ? 'text-red-400' : 'text-green-400']">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import api from '../api';

const selectedClass = ref('regular');
const roundNumber = ref(1);
const file = ref<File | null>(null);
const uploading = ref(false);
const message = ref('');
const isError = ref(false);

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    file.value = target.files[0]!;
  } else {
    file.value = null;
  }
};

const upload = async () => {
  if (!file.value) return;

  uploading.value = true;
  message.value = '';
  isError.value = false;

  const formData = new FormData();
  formData.append('file', file.value);

  try {
    await api.post('/admin/battery_placing_upload', formData, {
      params: {
        class: selectedClass.value,
        round_number: roundNumber.value
      },
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    message.value = 'Results uploaded successfully!';
    file.value = null; // Clear file input? Hard to clear input element programmatically without ref
  } catch (error: any) {
    console.error('Upload failed:', error);
    isError.value = true;
    message.value = error.response?.data?.detail || 'Upload failed';
  } finally {
    uploading.value = false;
  }
};
</script>
