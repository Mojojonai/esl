<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="bg-gray-50 p-6 rounded-lg">
      <p class="text-lg font-medium text-gray-900">{{ exercise.content.question || exercise.instruction }}</p>
    </div>

    <div class="grid grid-cols-2 gap-4">
      <label
        class="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-300 transition-colors"
        :class="answer === true && 'border-blue-600 bg-blue-50'"
      >
        <input type="radio" :value="true" v-model="answer" class="mr-3" />
        <span class="font-bold text-lg text-green-600">True</span>
      </label>

      <label
        class="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-red-300 transition-colors"
        :class="answer === false && 'border-red-600 bg-red-50'"
      >
        <input type="radio" :value="false" v-model="answer" class="mr-3" />
        <span class="font-bold text-lg text-red-600">False</span>
      </label>
    </div>

    <button type="submit" :disabled="answer === null" class="btn-primary w-full">
      Check Answer
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  exercise: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['submit'])
const answer = ref(null)

const handleSubmit = () => {
  emit('submit', answer.value)
}
</script>
