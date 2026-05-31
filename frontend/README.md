# ESL Learning Platform - Frontend

Modern Vue.js 3 frontend for the ESL (English as Second Language) learning platform.

## Tech Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Vite** - Build tool
- **Phaser.js** - Mini-games framework (for future implementation)

## Project Structure

```
frontend/
├── src/
│   ├── main.js                  # App entry point
│   ├── App.vue                  # Root component
│   ├── style.css                # Global styles
│   ├── components/
│   │   ├── layout/              # Header, navigation, etc.
│   │   ├── exercises/           # Exercise component types
│   │   ├── games/               # Mini-game components
│   │   └── shared/              # Reusable components
│   ├── pages/                   # Page components
│   ├── router/
│   │   └── index.js             # Route configuration
│   ├── stores/
│   │   ├── authStore.js         # Authentication state
│   │   ├── exerciseStore.js     # Exercise/learning state
│   │   └── progressStore.js     # Progress/badges state
│   └── services/
│       └── api.js               # API client
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── README.md
```

## Installation

### 1. Install Dependencies

```bash
npm install
```

### 2. Development Server

```bash
npm run dev
```

App runs at `http://localhost:5175`

The Vite dev server proxies API requests to the backend (`http://localhost:8000/api`).

### 3. Build for Production

```bash
npm run build
```

Outputs to `dist/` directory ready for deployment.

### 4. Preview Production Build

```bash
npm run preview
```

## Key Features Implemented

### Authentication
- Login page with username/password
- First-time password change flow
- Logout functionality
- Protected routes with automatic redirects
- Token-based API authentication

### Dashboard
- Welcome message with user name
- Quick stats (Level, XP, Streak, Badges)
- Quick action cards
- Recent badges display
- Review item count

### Learning Flow
1. Select Level (A1, A2, B1, B2, C1)
2. Browse Units within level
3. View Lessons in each unit
4. Complete Exercises with instant feedback
5. Progress tracking and badges

### Exercise Types
- Fill in the Blank
- Audio-Image Matching
- Multiple Choice
- True/False
- Choose Best Response
- More (easily extensible with new types)

### Exercise Features
- Question display
- Multiple answer options
- Audio support
- Image support
- Hints system
- Instant feedback
- XP rewards
- Time tracking

### Progress Tracking
- Progress by skill area (Listening, Reading, etc.)
- Progress by unit
- Progress percentage bars
- Average scores
- Badge earning

### Spaced Repetition
- Review due items
- Mark correct/incorrect
- Strength tracking
- Schedule adjustments

## Pages

### `/login`
Login page for authentication.

### `/dashboard`
Main hub showing stats, recent activity, and quick actions.

### `/levels`
Select learning level (A1, A2, B1, B2, C1).

### `/level/:levelCode/units`
Browse units in selected level.

### `/unit/:unitId/lessons`
View lessons in selected unit.

### `/lesson/:lessonId/exercises`
Complete exercises from selected lesson.

### `/exercise/:exerciseId`
Individual exercise player.

### `/progress`
View detailed progress by skill and unit.

### `/review`
Spaced repetition review items.

## Components

### Layout
- **AppHeader** - Top navigation bar
- **BottomNav** - Mobile bottom navigation

### Exercises
- **ExerciseRenderer** - Routes to appropriate exercise type
- **FillBlank** - Fill in blank exercise
- **AudioImageMatch** - Match audio with images
- **TrueFalse** - True/False questions
- **ChooseResponse** - Choose best response
- **SimpleMultipleChoice** - Generic multiple choice

### Shared
- **FeedbackBox** - Show results after exercise

## State Management (Pinia Stores)

### authStore
- User authentication state
- Login/logout logic
- Password change
- Token management

### exerciseStore
- Levels, units, lessons
- Exercises, vocabulary, dialogues
- Games
- Exercise submission
- Game submission

### progressStore
- User progress by skill/unit
- Badges earned
- Review items
- Achievement checking

## API Integration

All API calls go through `/services/api.js` with token-based authentication.

## Styling

Uses Tailwind CSS for all styling with responsive mobile-first design.

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_content
python manage.py runserver

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5175` and login with:
- Username: `learner1`
- Password: `learner123`

## Resources

- [Vue.js Documentation](https://vuejs.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Pinia](https://pinia.vuejs.org)
- [Vue Router](https://router.vuejs.org)
- [Vite](https://vitejs.dev)
