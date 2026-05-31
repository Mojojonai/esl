<template>
  <div
    class="card"
    :class="[
      feedback.is_correct
        ? 'border-l-4 border-l-green-500 bg-green-50'
        : 'border-l-4 border-l-red-500 bg-red-50'
    ]"
  >
    <!-- Result Header -->
    <div class="flex items-start justify-between mb-4">
      <div>
        <h2 v-if="feedback.is_correct" class="text-3xl font-bold text-green-700">
          🎉 Excellent!
        </h2>
        <h2 v-else class="text-3xl font-bold text-red-700">
          Try Again
        </h2>
        <p v-if="feedback.is_correct" class="text-green-600 mt-1">Great job! You got it right.</p>
        <p v-else class="text-red-600 mt-1">Don't worry, you can try again.</p>
      </div>

      <!-- XP Earned -->
      <div class="text-center">
        <div class="text-4xl font-bold text-orange-500">+{{ feedback.xp_earned }}</div>
        <div class="text-sm text-gray-600">XP Earned</div>
      </div>
    </div>

    <!-- Correct Answer (if wrong) -->
    <div v-if="!feedback.is_correct && feedback.correct_answer" class="bg-white p-4 rounded-lg mb-4">
      <p class="text-sm font-medium text-gray-700 mb-2">The correct answer was:</p>
      <p class="text-lg font-bold text-gray-900">{{ feedback.correct_answer }}</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 mb-4">
      <div class="bg-white p-3 rounded-lg text-center">
        <div class="text-sm text-gray-600">Score</div>
        <div class="text-2xl font-bold text-blue-600">{{ feedback.score }}%</div>
      </div>
      <div class="bg-white p-3 rounded-lg text-center">
        <div class="text-sm text-gray-600">Time</div>
        <div class="text-2xl font-bold text-blue-600">{{ timeSpent }}s</div>
      </div>
      <div class="bg-white p-3 rounded-lg text-center">
        <div class="text-sm text-gray-600">Status</div>
        <div class="text-2xl" v-if="feedback.is_correct">✅</div>
        <div class="text-2xl" v-else>❌</div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex gap-3">
      <button
        @click="$emit('next')"
        class="flex-1 btn-primary"
      >
        → Next Exercise
      </button>
      <button
        v-if="!feedback.is_correct"
        @click="$emit('retry')"
        class="flex-1 btn-secondary"
      >
        ↻ Try Again
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  feedback: {
    type: Object,
    required: true,
  },
})

defineEmits(['next', 'retry'])

const timeSpent = computed(() => {
  const time = props.feedback.time_spent_seconds || 0
  return Math.round(time)
})
</script>
