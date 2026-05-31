<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Question Display -->
    <div class="bg-blue-50 p-6 rounded-lg">
      <p class="text-gray-600 text-sm mb-2">Fill in the blank:</p>
      <div class="flex items-center gap-2 flex-wrap">
        <span v-for="(part, index) in sentenceParts" :key="index" class="text-lg">
          <span v-if="part === '___'" class="text-blue-600 font-bold">{{ answer || '___' }}</span>
          <span v-else>{{ part }}</span>
        </span>
      </div>
    </div>

    <!-- Word Bank -->
    <div v-if="exercise.content.word_bank" class="space-y-3">
      <p class="text-sm font-medium text-gray-700">Choose the correct word:</p>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
        <button
          v-for="(word, index) in exercise.content.word_bank"
          :key="index"
          type="button"
          @click="answer = word"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            answer === word
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-900 hover:bg-gray-300'
          ]"
        >
          {{ word }}
        </button>
      </div>
    </div>

    <!-- Input Field (if no word bank) -->
    <div v-else>
      <input
        v-model="answer"
        type="text"
        class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
        placeholder="Type your answer"
      />
    </div>

    <!-- Hints -->
    <div v-if="exercise.hints && exercise.hints.length > 0 && !showHint" class="text-center">
      <button
        type="button"
        @click="showHint = true"
        class="text-sm text-blue-600 hover:text-blue-700 font-medium"
      >
        💡 Show Hint
      </button>
    </div>

    <div v-if="showHint && exercise.hints && exercise.hints.length > 0" class="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
      <p class="text-sm text-yellow-800">{{ exercise.hints[0] }}</p>
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
import { ref, computed } from 'vue'

const props = defineProps({
  exercise: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['submit'])

const answer = ref('')
const showHint = ref(false)

const sentenceParts = computed(() => {
  return props.exercise.content.sentence.split(' ')
})

const handleSubmit = () => {
  emit('submit', answer.value)
}
</script>
