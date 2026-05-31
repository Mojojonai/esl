<template>
  <div class="container-main">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ levelCode }} Units</h1>
    
    <div v-if="exerciseStore.isLoading" class="text-center py-12">
      <p class="text-gray-600">Loading units...</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <router-link
        v-for="unit in exerciseStore.units"
        :key="unit.id"
        :to="`/unit/${unit.id}/lessons`"
        class="card hover:shadow-xl cursor-pointer group"
      >
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-bold text-gray-900">Unit {{ unit.order }}</h3>
            <p class="text-lg text-gray-700 mt-2">{{ unit.title }}</p>
            <p class="text-gray-600 text-sm mt-1">Theme: {{ unit.theme }}</p>
          </div>
          <div class="text-4xl group-hover:scale-125 transition-transform">→</div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useExerciseStore } from '../stores/exerciseStore'

const route = useRoute()
const exerciseStore = useExerciseStore()
const levelCode = ref(route.params.levelCode)

onMounted(() => {
  exerciseStore.fetchUnits(levelCode.value)
})
</script>
