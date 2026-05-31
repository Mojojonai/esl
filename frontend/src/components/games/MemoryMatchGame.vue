<template>
  <div class="card p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">{{ game.title }}</h2>
        <p class="text-gray-600 mt-1">{{ game.description }}</p>
      </div>
      <div class="text-right">
        <div class="text-sm text-gray-500">Score: <strong>{{ score }}</strong></div>
        <div class="text-sm text-gray-500">Attempts: <strong>{{ attempts }}</strong></div>
      </div>
    </div>

    <div ref="gameContainer" class="w-full h-[520px] rounded-3xl overflow-hidden bg-slate-100" />

    <div class="mt-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <button class="btn-primary" @click="restartGame">Restart Game</button>
      <button
        class="btn-secondary"
        :disabled="!isComplete"
        @click="finishGame"
      >
        {{ isComplete ? 'Submit score' : 'Finish after matching all cards' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Phaser from 'phaser'

const props = defineProps({
  game: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['complete'])
const gameContainer = ref(null)
const phaserGame = ref(null)
const score = ref(0)
const attempts = ref(0)
const isComplete = ref(false)
const startTime = ref(Date.now())
let cardObjects = []
let openCards = []
let matchedPairs = 0

const normalizeCardData = () => {
  const rawCards = props.game.config?.cards || props.game.config?.items || []
  if (rawCards.length > 0) {
    return rawCards.slice(0, 6).map((item, index) => ({
      id: item.id || item.key || `card-${index}`,
      label: item.label || item.text || item.display || item.word || item.term || String(item),
    }))
  }

  return [
    { id: 'cat', label: 'Cat' },
    { id: 'dog', label: 'Dog' },
    { id: 'sun', label: 'Sun' },
    { id: 'book', label: 'Book' },
    { id: 'cup', label: 'Cup' },
    { id: 'hat', label: 'Hat' },
  ]
}

const shuffle = (array) => {
  const copy = array.slice()
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

const buildCardDeck = () => {
  const cards = normalizeCardData()
  const deck = cards.flatMap((item) => [
    { pairId: item.id, label: item.label, uid: `${item.id}-a` },
    { pairId: item.id, label: item.label, uid: `${item.id}-b` },
  ])
  return shuffle(deck)
}

const createPhaserScene = () => {
  const cardDeck = buildCardDeck()
  const columns = 4
  const rows = Math.ceil(cardDeck.length / columns)
  const cardWidth = 140
  const cardHeight = 130
  const spacing = 24
  let revealTimer = null

  class MemoryScene extends Phaser.Scene {
    constructor() {
      super({ key: 'MemoryScene' })
    }

    create() {
      const startX = (this.scale.width - (columns * cardWidth + (columns - 1) * spacing)) / 2
      const startY = (this.scale.height - (rows * cardHeight + (rows - 1) * spacing)) / 2

      cardDeck.forEach((cardData, index) => {
        const col = index % columns
        const row = Math.floor(index / columns)
        const x = startX + col * (cardWidth + spacing) + cardWidth / 2
        const y = startY + row * (cardHeight + spacing) + cardHeight / 2

        const cardBack = this.add.rectangle(0, 0, cardWidth, cardHeight, 0x3b82f6)
          .setStrokeStyle(3, 0x1d4ed8)
        const cardFront = this.add.rectangle(0, 0, cardWidth - 8, cardHeight - 8, 0xf8fafc)
          .setStrokeStyle(2, 0x64748b)
          .setVisible(false)
        const cardText = this.add.text(0, 0, cardData.label, {
          fontFamily: 'Inter, sans-serif',
          fontSize: '20px',
          color: '#0f172a',
          align: 'center',
          wordWrap: { width: cardWidth - 24 },
        }).setOrigin(0.5).setVisible(false)

        const container = this.add.container(x, y, [cardBack, cardFront, cardText])
          .setSize(cardWidth, cardHeight)
          .setInteractive(new Phaser.Geom.Rectangle(-cardWidth / 2, -cardHeight / 2, cardWidth, cardHeight), Phaser.Geom.Rectangle.Contains)

        container.on('pointerdown', () => {
          if (revealTimer || isComplete.value) return
          const cardItem = cardObjects.find((item) => item.uid === cardData.uid)
          if (!cardItem || cardItem.matched || cardItem.flipped) return

          flipCard(cardItem)
          openCards.push(cardItem)

          if (openCards.length === 2) {
            attempts.value += 1
            if (openCards[0].pairId === openCards[1].pairId) {
              openCards.forEach((item) => {
                item.matched = true
              })
              score.value += 25
              matchedPairs += 1
              openCards = []

              if (matchedPairs === cardDeck.length / 2) {
                completeGame()
              }
            } else {
              revealTimer = this.time.delayedCall(700, () => {
                openCards.forEach(hideCard)
                openCards = []
                revealTimer = null
              })
            }
          }
        })

        cardObjects.push({
          uid: cardData.uid,
          pairId: cardData.pairId,
          container,
          cardBack,
          cardFront,
          cardText,
          flipped: false,
          matched: false,
        })
      })
    }
  }

  return MemoryScene
}

const flipCard = (cardItem) => {
  if (!cardItem || cardItem.flipped || cardItem.matched) return
  cardItem.cardBack.setVisible(false)
  cardItem.cardFront.setVisible(true)
  cardItem.cardText.setVisible(true)
  cardItem.flipped = true
}

const hideCard = (cardItem) => {
  if (!cardItem || cardItem.matched) return
  cardItem.cardBack.setVisible(true)
  cardItem.cardFront.setVisible(false)
  cardItem.cardText.setVisible(false)
  cardItem.flipped = false
}

const completeGame = () => {
  isComplete.value = true
  score.value = Math.min(100, Math.max(score.value, 50))
}

const finishGame = () => {
  if (!isComplete.value) return
  const timeSpent = Math.floor((Date.now() - startTime.value) / 1000)
  emit('complete', { score: score.value, timeSpent })
}

const destroyPhaserGame = () => {
  if (phaserGame.value) {
    phaserGame.value.destroy(true)
    phaserGame.value = null
  }
}

const initializeGame = () => {
  destroyPhaserGame()
  attempts.value = 0
  score.value = 0
  isComplete.value = false
  matchedPairs = 0
  openCards = []
  cardObjects = []
  startTime.value = Date.now()

  const scene = createPhaserScene()
  phaserGame.value = new Phaser.Game({
    type: Phaser.AUTO,
    width: 760,
    height: 520,
    backgroundColor: '#eff6ff',
    parent: gameContainer.value,
    scene,
    scale: {
      mode: Phaser.Scale.FIT,
      autoCenter: Phaser.Scale.CENTER_BOTH,
    },
  })
}

const restartGame = () => {
  initializeGame()
}

onMounted(() => {
  initializeGame()
})

onBeforeUnmount(() => {
  destroyPhaserGame()
})
</script>

<style scoped>
.card {
  min-height: 120px;
}
</style>
