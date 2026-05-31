<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="bg-gray-50 p-6 rounded-lg">
      <p class="text-lg font-medium text-gray-900">{{ exercise.content.question || exercise.instruction }}</p>
      <button
        v-if="exercise.content.prompt_audio"
        type="button"
        @click="playAudio"
        class="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
      >
        ▶ Play Audio
      </button>
    </div>

    <div class="space-y-3">
      <label
        v-for="(option, index) in exercise.content.options"
        :key="index"
        class="flex items-center p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-300 transition-colors"
        :class="answer === (option.id || option) ? 'border-blue-600 bg-blue-50' : ''"
      >
        <input type="radio" :value="option.id || option" v-model="answer" class="mr-3" />
        <div class="flex-1">
          <span class="font-medium text-gray-900">{{ option.text || option }}</span>
        </div>
      </label>
    </div>

    <button type="submit" :disabled="!answer" class="btn-primary w-full">
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
const answer = ref('')

const playAudio = () => {
  const url = exercise.content.prompt_audio
  if (!url) return
  const audio = new Audio(url)
  audio.play()
}

const handleSubmit = () => {
  emit('submit', answer.value)
}
</script>
