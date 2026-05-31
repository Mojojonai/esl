<template>
  <div class="card">
    <!-- Exercise Content based on Type -->
    <component
      :is="getExerciseComponent(exercise.exercise_type)"
      :exercise="exercise"
      @submit="$emit('submit', $event)"
    />
  </div>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

defineProps({
  exercise: {
    type: Object,
    required: true,
  },
})

defineEmits(['submit', 'skip'])

// Lazy load exercise components
const FillBlank = defineAsyncComponent(() => import('./FillBlank.vue'))
const AudioImageMatch = defineAsyncComponent(() => import('./AudioImageMatch.vue'))
const AudioMultipleChoice = defineAsyncComponent(() => import('./AudioMultipleChoice.vue'))
const TrueFalse = defineAsyncComponent(() => import('./TrueFalse.vue'))
const ChooseResponse = defineAsyncComponent(() => import('./ChooseResponse.vue'))
const SimpleMultipleChoice = defineAsyncComponent(() => import('./SimpleMultipleChoice.vue'))
const ReadAlong = defineAsyncComponent(() => import('./ReadAlong.vue'))
const VocabularyInContext = defineAsyncComponent(() => import('./VocabularyInContext.vue'))

const getExerciseComponent = (exerciseType) => {
  const components = {
    'fill_blank': FillBlank,
    'audio_image_match': AudioImageMatch,
    'audio_multiple_choice': AudioMultipleChoice,
    'true_false': TrueFalse,
    'choose_best_response': ChooseResponse,
    'dialogue_comprehension': ChooseResponse,
    'word_picture_match': SimpleMultipleChoice,
    'sentence_picture_match': SimpleMultipleChoice,
    'read_along': ReadAlong,
    'vocabulary_in_context': VocabularyInContext,
  }
  return components[exerciseType] || SimpleMultipleChoice
}
</script>
