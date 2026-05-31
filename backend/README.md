# ESL Learning Platform - Backend

Django REST API for the ESL (English as Second Language) learning platform.

## Project Structure

```
backend/
├── eslapp/              # Main Django project settings
├── accounts/            # User authentication and profiles
├── learning/            # Core learning content (levels, units, lessons, exercises)
├── tracking/            # Progress tracking, badges, spaced repetition
├── games/               # Mini-games configuration
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env File

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Initial Content

```bash
python manage.py seed_content
```

This creates:
- A1 Level with Unit 1 and Unit 2
- Demo users (admin / admin123, learner1 / learner123)
- Sample exercises and vocabulary
- Badge definitions

### 6. Create Superuser (if not using seed)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server runs at `http://localhost:8000`

Admin panel: `http://localhost:8000/admin`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/users/me/` - Get current user

### Learning Content
- `GET /api/levels/` - Get all levels
- `GET /api/units/?level=A1` - Get units by level
- `GET /api/lessons/?unit=1` - Get lessons by unit
- `GET /api/exercises/?lesson=1&skill=listening` - Get exercises
- `GET /api/vocabulary/?lesson=1` - Get vocabulary
- `GET /api/dialogues/?lesson=1` - Get dialogues

### Exercises & Games
- `POST /api/exercises/{id}/submit/` - Submit exercise answer
- `POST /api/games/{id}/submit/` - Submit game score

### Progress & Achievements
- `GET /api/progress/my_progress/` - Get user progress
- `GET /api/badges/my_badges/` - Get user badges
- `POST /api/badges/check_achievements/` - Check for badge achievements
- `GET /api/review/due_for_review/` - Get exercises due for review

## Database Models

### Accounts
- **User** - Django built-in user model
- **UserProfile** - Extended user info (level, XP, streak, etc.)

### Learning
- **Level** - CEFR levels (A1, A2, B1, B2, C1)
- **Unit** - Learning units within levels
- **Lesson** - Individual lessons within units
- **SkillArea** - Learning skills (Listening, Reading, Writing, etc.)
- **VocabularyItem** - Vocabulary for lessons
- **Dialogue** - Dialogues for listening/comprehension
- **Exercise** - Individual exercises with flexible JSON content
- **Game** - Mini-games
- **UserExerciseAttempt** - Track exercise submissions
- **UserGameAttempt** - Track game submissions

### Tracking
- **UserProgress** - Progress tracking by level/unit/skill
- **Badge** - Badge definitions
- **UserBadge** - User's earned badges
- **ReviewItem** - Spaced repetition items

## Admin Panel

Access at `/admin` with superuser credentials.

Manage:
- Levels and Units
- Lessons and Exercises
- Vocabulary and Dialogues
- User attempts and progress
- Badges and achievements

## Content Structure

### Exercise Types

**Listening:**
- audio_image_match
- audio_multiple_choice
- dictation
- dialogue_comprehension

**Comprehension:**
- picture_situation_match
- dialogue_meaning_question
- true_false
- choose_best_response

**Reading:**
- word_picture_match
- sentence_picture_match
- read_along
- vocabulary_in_context

**Writing:**
- fill_blank
- word_bank_completion
- drag_drop_sentence
- type_missing_word
- correct_sentence
- picture_prompt_writing

### Exercise JSON Format

Each exercise has flexible `content` and `correct_answer` fields:

```json
{
  "exercise_type": "fill_blank",
  "content": {
    "sentence": "My name ___ Ana.",
    "word_bank": ["is", "are", "am"]
  },
  "correct_answer": "is"
}
```

## Key Features

### Spaced Repetition
- Track exercise attempts
- Schedule reviews based on performance
- Strengthen weak areas

### Gamification
- XP points for correct answers
- Streak tracking
- Badge achievements
- Level progression

### Flexible Content
- JSON-based exercise content
- Support for multiple exercise types
- Easy to extend with new exercise types

### User Progress Tracking
- Per-level, per-unit, per-skill progress
- Average scores
- Completion tracking

## Security

- JWT/Token-based authentication
- CORS headers for frontend integration
- Admin-only content management
- User permission checks on progress endpoints

## Next Steps

### Phase 2
- Add speech-to-text for speaking exercises
- Implement more mini-games
- Full spaced repetition review system
- More content for A1 units

### Phase 3
- Add A2, B1, B2 levels
- AI tutor integration
- Teacher/classroom mode
- PWA offline support

## Development Notes

### Creating Custom Migrations
```bash
python manage.py makemigrations app_name
python manage.py migrate
```

### Loading/Dumping Data
```bash
python manage.py dumpdata > db_backup.json
python manage.py loaddata db_backup.json
```

### Running Tests
```bash
python manage.py test
```

## Environment Variables

See `.env.example` for all available options.

Key variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Allowed hostnames
- `DATABASE_URL` - Database connection string
- `CORS_ALLOWED_ORIGINS` - Frontend URLs

## Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database locked
```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_content
```

### Missing migrations
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```
