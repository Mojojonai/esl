<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="bg-blue-50 p-6 rounded-lg space-y-4">
      <p class="text-sm text-gray-500">Read the passage below:</p>
      <p class="text-lg leading-8 text-gray-900 whitespace-pre-line">{{ exercise.content.text }}</p>
    </div>

    <div v-if="exercise.content.question" class="bg-gray-50 p-6 rounded-lg">
      <p class="text-lg font-medium text-gray-900 mb-3">{{ exercise.content.question }}</p>
      <div class="space-y-3">
        <label
          v-for="(option, index) in exercise.content.options"
          :key="index"
          class="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-300 transition-colors"
          :class="answer === option ? 'border-blue-600 bg-blue-50' : ''"
        >
          <input type="radio" :value="option" v-model="answer" class="mr-3" />
          <span class="font-medium text-gray-900">{{ option }}</span>
        </label>
      </div>
    </div>

    <button type="submit" :disabled="exercise.content.question && !answer" class="btn-primary w-full">
      Mark Complete
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
const answer = ref('')

const handleSubmit = () => {
  emit('submit', answer.value || 'read')
}
</script>
