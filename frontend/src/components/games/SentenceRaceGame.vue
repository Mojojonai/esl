<template>
  <div class="card p-6">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">{{ game.title }}</h2>
      <p class="text-gray-600 mt-2">{{ game.description }}</p>
    </div>

    <div class="bg-slate-100 p-6 rounded-3xl space-y-4">
      <p class="text-lg font-medium text-gray-900">Arrange the sentence in the right order</p>
      <div class="grid grid-cols-2 gap-3">
        <button
          v-for="word in shuffledWords"
          :key="word.id"
          type="button"
          @click="selectWord(word)"
          class="px-4 py-3 rounded-lg border border-gray-300 bg-white hover:bg-blue-50 transition-colors"
          :class="selectedIds.includes(word.id) ? 'opacity-50 cursor-not-allowed' : ''"
          :disabled="selectedIds.includes(word.id)"
        >
          {{ word.text }}
        </button>
      </div>
    </div>

    <div class="bg-white p-6 rounded-3xl border border-gray-200 mt-6">
      <p class="text-sm text-gray-500 mb-3">Selected order:</p>
      <div class="min-h-[72px] p-4 bg-gray-50 rounded-lg border border-dashed border-gray-200 flex flex-wrap gap-2">
        <span
          v-for="(word, index) in selectedWords"
          :key="word.id"
          class="px-3 py-2 rounded-full bg-blue-50 text-blue-700"
        >
          {{ word.text }}
        </span>
      </div>
    </div>

    <div class="flex flex-col md:flex-row gap-3 mt-6">
      <button class="btn-primary flex-1" @click="checkAnswer" :disabled="selectedWords.length !== words.length">
        Submit Sentence
      </button>
      <button class="btn-secondary flex-1" type="button" @click="resetGame">
        Reset
      </button>
    </div>

    <div v-if="message" class="mt-4 p-4 rounded-lg" :class="messageType === 'success' ? 'bg-green-50 border border-green-200 text-green-700' : 'bg-red-50 border border-red-200 text-red-700'">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  game: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['complete'])
const selectedIds = ref([])
const selectedWords = ref([])
const message = ref('')
const messageType = ref('')

const words = computed(() => {
  const items = props.game.config?.sentence?.split(' ') || []
  return items.map((text, index) => ({ id: `${index}-${text}`, text }))
})

const shuffledWords = computed(() => {
  return words.value.slice().sort(() => Math.random() - 0.5)
})

const resetGame = () => {
  selectedIds.value = []
  selectedWords.value = []
  message.value = ''
}

const selectWord = (word) => {
  if (selectedIds.value.includes(word.id)) return
  selectedIds.value.push(word.id)
  selectedWords.value.push(word)
}

const checkAnswer = () => {
  const answer = selectedWords.value.map((item) => item.text).join(' ')
  const correct = props.game.config?.sentence || ''
  const isCorrect = answer.trim() === correct.trim()
  messageType.value = isCorrect ? 'success' : 'error'
  message.value = isCorrect ? 'Great job! You arranged it correctly.' : 'Not quite — try again or reset.'

  if (isCorrect) {
    emit('complete', { score: 100, timeSpent: Math.floor((Date.now() - startTime.value) / 1000) })
  }
}

const startTime = ref(Date.now())

onMounted(() => {
  resetGame()
  startTime.value = Date.now()
})
</script>

<style scoped>
.btn-primary {
  @apply bg-blue-600 text-white;
}
</style>
