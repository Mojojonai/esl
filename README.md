# EnglishNow - ESL Learning Platform

A modern, web-first English-learning application for non-English speakers. Learn English through interactive lessons, mini-games, and spaced repetition memory techniques.

## 🎯 Project Vision

EnglishNow combines classroom curriculum, game-based learning, and cognitive memory techniques to help beginners and intermediate English learners improve through:

- **Listening** - Audio exercises and comprehension
- **Comprehension** - Dialogue understanding and meaning matching
- **Reading** - Text-based exercises and read-along activities
- **Writing** - Fill-in-the-blank, sentence building, and typing
- **Speaking** - Pronunciation and dialogue practice (future)
- **Gamification** - XP, streaks, badges, and mini-games
- **Memory Training** - Spaced repetition and cognitive connection

## 📱 Features

### For Learners
- Modern, mobile-first responsive design
- A1-C1 CEFR level progression
- Original content inspired by Interchange English
- Instant feedback and hints
- XP rewards and achievement badges
- Spaced repetition review system
- Progress tracking by skill and unit
- Dashboard with stats (Level, XP, Streak, Badges)

### For Admins
- Django admin interface for content management
- Manage users, levels, units, lessons, exercises
- Upload images and audio
- View user progress and reports
- Badge configuration

### For Future
- AI tutor with explanations
- Speech-to-text recognition
- Personalized learning paths
- Teacher/classroom mode
- PWA offline support
- Native mobile apps

## 🏗️ Project Structure

```
EnglishLearningApp/
├── backend/                 # Django REST API
│   ├── eslapp/             # Django project settings
│   ├── accounts/           # User authentication
│   ├── learning/           # Core learning content
│   ├── tracking/           # Progress and badges
│   ├── games/              # Mini-games
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
├── frontend/               # Vue.js 3 application
│   ├── src/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── README.md
├── assets/
│   ├── images/
│   └── audio/
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (choose based on OS)
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Seed initial content
python manage.py seed_content

# Start development server
python manage.py runserver
```

Backend runs at `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

### Frontend Setup (new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at `http://localhost:5173`

### Demo Credentials

After running `seed_content` command:

**Learner Account:**
- Username: `learner1`
- Password: `learner123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## 📚 Learning Curriculum (MVP)

### A1 Level - Beginner

#### Unit 1: Introduction to English
- Alphabet and basic sounds
- Introduce yourself: "My name is...", "I am..."
- Personal pronouns
- **Exercise types:** Listening, Comprehension, Reading, Writing

#### Unit 2: Greetings and Politeness
- Hello, Hi, Good morning/afternoon/evening
- Goodbye and see you
- "How are you?" responses
- Basic politeness phrases
- **Exercise types:** All skills

*Future:* Units 3-15 expanding to cover numbers, family, daily routines, food, places, shopping, weather, abilities, past tense, etc.

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 4.2
- **API:** Django REST Framework
- **Database:** SQLite (MVP), PostgreSQL (production)
- **Authentication:** Token-based
- **Admin:** Django Admin

### Frontend
- **Framework:** Vue.js 3
- **Routing:** Vue Router 4
- **State Management:** Pinia
- **Styling:** Tailwind CSS
- **HTTP:** Axios
- **Build:** Vite
- **Games:** Phaser.js (future)

## 📋 API Endpoints

All endpoints require authentication with Bearer token.

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/change-password/` - Change password

### Learning Content
- `GET /api/levels/` - Get all levels
- `GET /api/units/?level=A1` - Get units by level
- `GET /api/lessons/?unit=1` - Get lessons
- `GET /api/exercises/?lesson=1&skill=listening` - Get exercises
- `GET /api/vocabulary/?lesson=1` - Get vocabulary
- `GET /api/dialogues/?lesson=1` - Get dialogues

### Exercises & Games
- `POST /api/exercises/{id}/submit/` - Submit exercise answer
- `POST /api/games/{id}/submit/` - Submit game score

### Progress & Achievements
- `GET /api/progress/my_progress/` - Get user progress
- `GET /api/badges/my_badges/` - Get earned badges
- `POST /api/badges/check_achievements/` - Check for new badges
- `GET /api/review/due_for_review/` - Get review items
- `POST /api/review/{id}/mark_correct/` - Mark review item correct
- `POST /api/review/{id}/mark_incorrect/` - Mark review item incorrect

## 🎓 Content Structure

### Curriculum Design
- Inspired by Interchange English books
- **All content is original** - No copyrighted text
- Communicative approach
- Real-life scenarios
- Grammar progression
- Vocabulary categories
- Speaking situations

### Exercise Types Supported

**Listening:**
- Audio-image matching
- Audio multiple choice
- Dictation
- Dialogue comprehension

**Comprehension:**
- Picture-situation matching
- Dialogue meaning questions
- True/False
- Choose best response

**Reading:**
- Word-picture matching
- Sentence-picture matching
- Read-along with highlighting
- Vocabulary in context

**Writing:**
- Fill in the blank
- Word bank completion
- Drag-drop sentence builder
- Correct the sentence
- Picture prompt writing

**Speaking (Future):**
- Repeat word/sentence
- Describe image
- Answer questions
- Dialogue role-play

## 🎮 Gamification

### XP System
- 10 XP for basic exercises
- 15 XP for advanced exercises
- 50 XP for mini-games (70%+ score)
- Accumulated for level progression

### Achievements (Badges)
- 🏅 First Steps - Complete first exercise
- 👂 Listening Hero - 5 listening exercises
- 📝 Word Builder - 50 XP earned
- 🔤 Sentence Master - 100 XP earned
- 🧠 Comprehension Star - 5 comprehension exercises
- 🔥 Streak Keeper - 7-day learning streak
- 🎓 Unit Completer - Complete entire unit
- ⭐ Skill Master - Master one skill area
- 💎 Memory Champion - 200 XP earned
- 🎤 Brave Speaker - Complete speaking exercise

### Progress Tracking
- Per-unit progress percentage
- Per-skill progress percentage
- Average score tracking
- Completed exercise count
- Time spent tracking

## 🧠 Spaced Repetition

### Memory Strengthening System
- **Mistake triggers review** - Exercise goes to review queue after mistake
- **Review schedule:**
  - First mistake: Review tomorrow
  - Correct 1x: Review in 2 days
  - Correct 2x: Review in 5 days
  - Correct 3x: Review in 10 days
- **Strength scoring:** 0 (weak) to 3 (strong)
- **Error tracking:** Mistakes counted for each item

## 🛡️ Security

- Password hashing with Django's auth
- Token-based API authentication
- CORS configured for frontend
- Admin-only content management
- User permission checks
- Secure session handling

## 📱 Responsive Design

- **Mobile First** - Optimized for small screens
- **Tablet** - Grid layouts for medium screens
- **Desktop** - Full-featured interface
- Bottom navigation on mobile
- Top navigation on desktop/tablet
- Touch-friendly buttons and spacing
- Works on iOS Safari, Chrome, Firefox

## 🔄 Development Workflow

### Adding New Content

1. **Through Django Admin:**
   - Create Levels
   - Add Units to Levels
   - Create Lessons in Units
   - Add Exercises to Lessons
   - Configure Games

2. **Via Management Command:**
   - Extend `seed_content` command
   - Load data from JSON/CSV

### Adding New Exercise Type

1. Create Vue component in `frontend/src/components/exercises/`
2. Export in `ExerciseRenderer.vue`
3. Add mapping in exercise type switch
4. Django automatically supports via JSON content

### Extending API

1. Django REST Framework viewsets in `views.py`
2. Serializers in `serializers.py`
3. Models in `models.py`
4. Register routes in `urls.py`

## 📈 Roadmap

### MVP (Phase 1) - Current
- ✅ Auth & user profiles
- ✅ A1 Unit 1 & 2
- ✅ 5 exercise types
- ✅ Basic gamification
- ✅ Progress tracking
- ✅ Dashboard
- ⏳ Memory game (Phaser.js)

### Phase 2
- Add complete A1 level (Units 3-15)
- Speech recognition for speaking
- More mini-games (5+ types)
- Vocabulary cards
- Dialogue role-play
- Full spaced repetition UI

### Phase 3
- A2, B1, B2 levels
- AI tutor chatbot
- Teacher dashboard
- Classroom management
- Reports & analytics
- PWA offline mode
- Mobile app wrappers

## 🤝 Contributing

Guidelines for contributing original content:

1. **All content must be original** - Inspired by pedagogy, not copied
2. **Realistic scenarios** - Daily life, work, travel, education
3. **Character consistency** - Recurring characters and stories
4. **Progressive difficulty** - Clear level progression
5. **Cultural sensitivity** - Inclusive and respectful

## 📄 License

[Add your license here]

## 🙋 Support

For issues or questions:
1. Check existing documentation
2. Review API endpoints
3. Check Django logs: `http://localhost:8000/admin`
4. Review browser console for frontend errors

## 📞 Contact

[Add contact information]

---

**Start learning English today with EnglishNow! 🚀**

Login at `http://localhost:5173` with credentials provided after running `seed_content`.
