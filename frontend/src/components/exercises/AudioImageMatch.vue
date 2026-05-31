<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Audio Player (if audio_url) -->
    <div v-if="exercise.content.prompt_audio" class="bg-blue-50 p-6 rounded-lg text-center">
      <p class="text-sm text-gray-600 mb-4">Listen to the audio:</p>
      <button
        type="button"
        @click="playAudio"
        class="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
      >
        🔊 Play Audio
      </button>
      <audio ref="audioElement" :src="exercise.content.prompt_audio" class="hidden" />
    </div>

    <!-- Question -->
    <div class="bg-gray-50 p-4 rounded-lg">
      <p class="font-medium text-gray-900">{{ exercise.content.question }}</p>
    </div>

    <!-- Options with Images -->
    <div v-if="exercise.content.options" class="space-y-3">
      <label
        v-for="(option, index) in exercise.content.options"
        :key="option.id"
        class="flex items-center p-4 border-2 rounded-lg cursor-pointer transition-colors"
        :class="[
          answer === option.id
            ? 'border-blue-600 bg-blue-50'
            : 'border-gray-200 hover:border-gray-300'
        ]"
      >
        <input
          type="radio"
          :value="option.id"
          v-model="answer"
          class="mr-4"
        />
        <div class="flex-1">
          <p class="font-medium text-gray-900">{{ option.text }}</p>
          <img
            v-if="option.image"
            :src="option.image"
            class="mt-2 w-24 h-24 object-cover rounded"
            :alt="option.text"
          />
        </div>
      </label>
    </div>

    <!-- Submit Button -->
    <button
      type="submit"
      :disabled="!answer"
      class="btn-primary w-full"
    >
      Check Answer
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  exercise: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['submit'])

const answer = ref('')
const audioElement = ref(null)

const playAudio = () => {
  if (audioElement.value) {
    audioElement.value.play()
  }
}

const handleSubmit = () => {
  emit('submit', answer.value)
}
</script>
