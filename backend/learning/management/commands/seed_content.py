from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from learning.models import Level, Unit, Lesson, SkillArea, VocabularyItem, Dialogue, DialogueLine, Exercise, Game
from tracking.models import Badge
from accounts.models import UserProfile
import json


class Command(BaseCommand):
    help = 'Seed the database with initial learning content for A1 MVP'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create skill areas
        self.stdout.write('Creating skill areas...')
        skill_areas = {}
        skill_data = [
            {'name': 'Listening', 'code': 'listening', 'icon': 'ear'},
            {'name': 'Comprehension', 'code': 'comprehension', 'icon': 'brain'},
            {'name': 'Reading', 'code': 'reading', 'icon': 'book'},
            {'name': 'Writing', 'code': 'writing', 'icon': 'pen'},
            {'name': 'Speaking', 'code': 'speaking', 'icon': 'microphone'},
        ]
        
        for skill in skill_data:
            obj, created = SkillArea.objects.get_or_create(
                code=skill['code'],
                defaults={
                    'name': skill['name'],
                    'description': f"{skill['name']} exercises",
                    'icon_name': skill['icon']
                }
            )
            skill_areas[skill['code']] = obj
        
        # Create A1 level
        self.stdout.write('Creating A1 level...')
        a1_level, _ = Level.objects.get_or_create(
            code='A1',
            defaults={
                'name': 'Beginner',
                'description': 'Learn basic English for everyday situations',
                'order': 1,
                'is_active': True
            }
        )
        
        # Create Unit 1: Introduction
        self.stdout.write('Creating Unit 1: Introduction to English...')
        unit1, _ = Unit.objects.get_or_create(
            level=a1_level,
            order=1,
            defaults={
                'title': 'Introduction to English',
                'description': 'Learn the alphabet, basic sounds, and introduce yourself',
                'theme': 'Introduction',
                'is_active': True
            }
        )
        
        # Create Unit 1 Lessons
        unit1_lesson1, _ = Lesson.objects.get_or_create(
            unit=unit1,
            order=1,
            defaults={
                'title': 'The Alphabet and Sounds',
                'objective': 'I can recognize letters and say my name.',
                'grammar_focus': 'Introduction sentence structures',
                'vocabulary_focus': 'Alphabet letters',
                'is_active': True
            }
        )
        
        unit1_lesson2, _ = Lesson.objects.get_or_create(
            unit=unit1,
            order=2,
            defaults={
                'title': 'Who Are You?',
                'objective': 'I can introduce myself with simple sentences.',
                'grammar_focus': 'My name is..., I am...',
                'vocabulary_focus': 'Names, pronouns',
                'is_active': True
            }
        )
        
        # Add vocabulary for Unit 1 Lesson 1
        self.stdout.write('Adding vocabulary for Unit 1...')
        vocab_items_u1_l1 = [
            {'word': 'A', 'pos': 'letter', 'sentence': 'A is the first letter of the alphabet.'},
            {'word': 'B', 'pos': 'letter', 'sentence': 'B is the second letter of the alphabet.'},
            {'word': 'C', 'pos': 'letter', 'sentence': 'C is the third letter of the alphabet.'},
            {'word': 'Hello', 'pos': 'interjection', 'sentence': 'Hello! My name is Ben.'},
            {'word': 'I', 'pos': 'pronoun', 'sentence': 'I am learning English.'},
            {'word': 'am', 'pos': 'verb', 'sentence': 'I am Ana.'},
        ]
        
        for item in vocab_items_u1_l1:
            VocabularyItem.objects.get_or_create(
                lesson=unit1_lesson1,
                word=item['word'],
                defaults={
                    'part_of_speech': item['pos'],
                    'example_sentence': item['sentence'],
                    'difficulty': 1,
                }
            )
        
        vocab_items_u1_l2 = [
            {'word': 'name', 'pos': 'noun', 'sentence': 'My name is Joshua.'},
            {'word': 'is', 'pos': 'verb', 'sentence': 'This is Ana.'},
            {'word': 'My', 'pos': 'determiner', 'sentence': 'My name is Ben.'},
            {'word': 'You', 'pos': 'pronoun', 'sentence': 'You are my friend.'},
            {'word': 'are', 'pos': 'verb', 'sentence': 'You are students.'},
            {'word': 'from', 'pos': 'preposition', 'sentence': 'I am from Brazil.'},
        ]
        
        for item in vocab_items_u1_l2:
            VocabularyItem.objects.get_or_create(
                lesson=unit1_lesson2,
                word=item['word'],
                defaults={
                    'part_of_speech': item['pos'],
                    'example_sentence': item['sentence'],
                    'difficulty': 1,
                }
            )
        
        # Create Exercises for Unit 1 Lesson 1
        self.stdout.write('Creating exercises for Unit 1...')
        
        # Listening: Audio-Image Match
        exercise_u1_l1_1, _ = Exercise.objects.get_or_create(
            lesson=unit1_lesson1,
            exercise_type='audio_image_match',
            order=1,
            defaults={
                'skill_area': skill_areas['listening'],
                'title': 'Listen and Choose the Letter',
                'instruction': 'Listen to the letter. Click the correct letter image.',
                'content': {
                    'prompt_audio': '/media/audio/a_letter.mp3',
                    'question': 'Which letter do you hear?',
                    'options': [
                        {'id': 'a', 'text': 'A', 'image': '/media/images/letter_a.png'},
                        {'id': 'b', 'text': 'B', 'image': '/media/images/letter_b.png'},
                        {'id': 'c', 'text': 'C', 'image': '/media/images/letter_c.png'},
                    ]
                },
                'correct_answer': 'a',
                'xp_reward': 10,
                'is_active': True
            }
        )
        
        # Reading: Word-Picture Match
        exercise_u1_l1_2, _ = Exercise.objects.get_or_create(
            lesson=unit1_lesson1,
            exercise_type='word_picture_match',
            order=2,
            defaults={
                'skill_area': skill_areas['reading'],
                'title': 'Match Letter to Picture',
                'instruction': 'Drag the letter to match the picture.',
                'content': {
                    'word': 'A',
                    'options': [
                        {'id': 'apple', 'text': 'Apple', 'image': '/media/images/apple.png'},
                        {'id': 'book', 'text': 'Book', 'image': '/media/images/book.png'},
                        {'id': 'cat', 'text': 'Cat', 'image': '/media/images/cat.png'},
                    ]
                },
                'correct_answer': 'apple',
                'xp_reward': 10,
                'is_active': True
            }
        )

        exercise_u1_l1_3, _ = Exercise.objects.get_or_create(
            lesson=unit1_lesson1,
            exercise_type='read_along',
            order=3,
            defaults={
                'skill_area': skill_areas['reading'],
                'title': 'Read Along Passage',
                'instruction': 'Read the short passage and answer the question.',
                'content': {
                    'text': 'Hello! My name is Ana. I am six years old. I like apples.',
                    'question': 'What does Ana like?',
                    'options': ['Bananas', 'Apples', 'Books']
                },
                'correct_answer': 'Apples',
                'xp_reward': 10,
                'is_active': True
            }
        )

        unit1_game1, _ = Game.objects.get_or_create(
            lesson=unit1_lesson1,
            game_type='memory_match',
            order=1,
            defaults={
                'title': 'Letter Memory Match',
                'description': 'Match the letters with the correct words to practice the alphabet.',
                'config': {
                    'cards': [
                        {'id': 'a', 'label': 'A'},
                        {'id': 'b', 'label': 'B'},
                        {'id': 'c', 'label': 'C'},
                        {'id': 'hello', 'label': 'Hello'},
                        {'id': 'name', 'label': 'Name'},
                        {'id': 'am', 'label': 'Am'},
                    ]
                },
                'xp_reward': 40,
                'is_active': True
            }
        )
        
        # Writing: Fill in the Blank
        exercise_u1_l2_1, _ = Exercise.objects.get_or_create(
            lesson=unit1_lesson2,
            exercise_type='fill_blank',
            order=1,
            defaults={
                'skill_area': skill_areas['writing'],
                'title': 'Complete the Sentence',
                'instruction': 'Fill in the blank with the correct word.',
                'content': {
                    'sentence': 'My name ___ Ana.',
                    'word_bank': ['is', 'are', 'am'],
                },
                'correct_answer': 'is',
                'hints': ['It goes with singular nouns like "name"'],
                'xp_reward': 15,
                'is_active': True
            }
        )
        
        # Comprehension: Dialogue Comprehension
        exercise_u1_l2_2, _ = Exercise.objects.get_or_create(
            lesson=unit1_lesson2,
            exercise_type='dialogue_comprehension',
            order=2,
            defaults={
                'skill_area': skill_areas['comprehension'],
                'title': 'Understand the Dialogue',
                'instruction': 'Read or listen to the dialogue. Answer the question.',
                'content': {
                    'dialogue': [
                        {'speaker': 'Ana', 'line': 'Hello!'},
                        {'speaker': 'Ben', 'line': 'Hi! My name is Ben.'},
                        {'speaker': 'Ana', 'line': 'I am Ana. Nice to meet you!'},
                    ],
                    'question': 'What is the boy\'s name?',
                    'options': ['Ana', 'Ben', 'Joshua']
                },
                'correct_answer': 'Ben',
                'xp_reward': 15,
                'is_active': True
            }
        )

        exercise_u1_l2_3, _ = Exercise.objects.get_or_create(
            lesson=unit1_lesson2,
            exercise_type='vocabulary_in_context',
            order=3,
            defaults={
                'skill_area': skill_areas['writing'],
                'title': 'Choose the Right Word',
                'instruction': 'Read the sentence and choose the correct word.',
                'content': {
                    'passage': 'My name is Ana and I am from Brazil.',
                    'question': 'What word completes the sentence? I am ___ Brazil.',
                    'options': ['from', 'am', 'is']
                },
                'correct_answer': 'from',
                'xp_reward': 10,
                'is_active': True
            }
        )
        
        # Create Unit 2: Greetings
        self.stdout.write('Creating Unit 2: Greetings...')
        unit2, _ = Unit.objects.get_or_create(
            level=a1_level,
            order=2,
            defaults={
                'title': 'Greetings and Politeness',
                'description': 'Learn how to greet people and respond politely',
                'theme': 'Greetings',
                'is_active': True
            }
        )
        
        unit2_lesson1, _ = Lesson.objects.get_or_create(
            unit=unit2,
            order=1,
            defaults={
                'title': 'Hello and Goodbye',
                'objective': 'I can greet people and say goodbye politely.',
                'grammar_focus': 'Simple greetings structures',
                'vocabulary_focus': 'Greetings: Hello, Hi, Good morning, Goodbye',
                'is_active': True
            }
        )
        
        unit2_lesson2, _ = Lesson.objects.get_or_create(
            unit=unit2,
            order=2,
            defaults={
                'title': 'How Are You?',
                'objective': 'I can ask how someone is and respond.',
                'grammar_focus': 'Question formation: How are you?',
                'vocabulary_focus': 'Fine, well, good, thank you',
                'is_active': True
            }
        )
        
        # Add vocabulary for Unit 2
        vocab_items_u2_l1 = [
            {'word': 'Hello', 'pos': 'interjection', 'sentence': 'Hello! Good morning.'},
            {'word': 'Hi', 'pos': 'interjection', 'sentence': 'Hi! How are you?'},
            {'word': 'Good morning', 'pos': 'phrase', 'sentence': 'Good morning. It is 7 AM.'},
            {'word': 'Good afternoon', 'pos': 'phrase', 'sentence': 'Good afternoon. It is 2 PM.'},
            {'word': 'Good evening', 'pos': 'phrase', 'sentence': 'Good evening. It is 6 PM.'},
            {'word': 'Goodbye', 'pos': 'interjection', 'sentence': 'Goodbye! See you tomorrow.'},
        ]
        
        for item in vocab_items_u2_l1:
            VocabularyItem.objects.get_or_create(
                lesson=unit2_lesson1,
                word=item['word'],
                defaults={
                    'part_of_speech': item['pos'],
                    'example_sentence': item['sentence'],
                    'difficulty': 1,
                }
            )
        
        vocab_items_u2_l2 = [
            {'word': 'How', 'pos': 'adverb', 'sentence': 'How are you today?'},
            {'word': 'are', 'pos': 'verb', 'sentence': 'How are you?'},
            {'word': 'you', 'pos': 'pronoun', 'sentence': 'How are you?'},
            {'word': 'fine', 'pos': 'adjective', 'sentence': 'I am fine, thank you.'},
            {'word': 'well', 'pos': 'adjective', 'sentence': 'I am well, thank you.'},
            {'word': 'thank you', 'pos': 'phrase', 'sentence': 'Thank you very much!'},
        ]
        
        for item in vocab_items_u2_l2:
            VocabularyItem.objects.get_or_create(
                lesson=unit2_lesson2,
                word=item['word'],
                defaults={
                    'part_of_speech': item['pos'],
                    'example_sentence': item['sentence'],
                    'difficulty': 1,
                }
            )
        
        # Create exercises for Unit 2 Lesson 1
        exercise_u2_l1_1, _ = Exercise.objects.get_or_create(
            lesson=unit2_lesson1,
            exercise_type='audio_multiple_choice',
            order=1,
            defaults={
                'skill_area': skill_areas['listening'],
                'title': 'Listen to the Greeting',
                'instruction': 'Listen and choose the correct greeting.',
                'content': {
                    'prompt_audio': '/media/audio/hello_greeting.mp3',
                    'question': 'What greeting do you hear?',
                    'options': [
                        {'id': 'a', 'text': 'Hello'},
                        {'id': 'b', 'text': 'Goodbye'},
                        {'id': 'c', 'text': 'Good morning'},
                    ]
                },
                'correct_answer': 'a',
                'xp_reward': 10,
                'is_active': True
            }
        )

        unit2_game1, _ = Game.objects.get_or_create(
            lesson=unit2_lesson1,
            game_type='memory_match',
            order=1,
            defaults={
                'title': 'Greeting Memory Match',
                'description': 'Match simple greetings and phrases to build listening memory.',
                'config': {
                    'cards': [
                        {'id': 'hello', 'label': 'Hello'},
                        {'id': 'goodbye', 'label': 'Goodbye'},
                        {'id': 'goodmorning', 'label': 'Good morning'},
                        {'id': 'hi', 'label': 'Hi'},
                        {'id': 'see_you', 'label': 'See you'},
                        {'id': 'thanks', 'label': 'Thank you'},
                    ]
                },
                'xp_reward': 40,
                'is_active': True
            }
        )

        unit2_game2, _ = Game.objects.get_or_create(
            lesson=unit2_lesson2,
            game_type='sentence_race',
            order=2,
            defaults={
                'title': 'Sentence Race',
                'description': 'Put the greeting sentence in the correct order quickly.',
                'config': {
                    'sentence': 'How are you today?'
                },
                'xp_reward': 40,
                'is_active': True
            }
        )
        
        # Create exercises for Unit 2 Lesson 2
        exercise_u2_l2_1, _ = Exercise.objects.get_or_create(
            lesson=unit2_lesson2,
            exercise_type='choose_best_response',
            order=1,
            defaults={
                'skill_area': skill_areas['comprehension'],
                'title': 'Choose the Best Response',
                'instruction': 'Choose the best response to the question.',
                'content': {
                    'dialogue': [
                        {'speaker': 'Person A', 'line': 'How are you?'},
                    ],
                    'question': 'What is a good response?',
                    'options': [
                        'Goodbye',
                        'I am fine, thank you.',
                        'My name is Ana.'
                    ]
                },
                'correct_answer': 'I am fine, thank you.',
                'xp_reward': 15,
                'is_active': True
            }
        )
        
        # Create Badges
        self.stdout.write('Creating badges...')
        badges_data = [
            {'code': 'first_steps', 'name': 'First Steps', 'desc': 'Complete your first exercise'},
            {'code': 'listening_hero', 'name': 'Listening Hero', 'desc': 'Complete 5 listening exercises'},
            {'code': 'word_builder', 'name': 'Word Builder', 'desc': 'Earn 50 XP'},
            {'code': 'sentence_master', 'name': 'Sentence Master', 'desc': 'Earn 100 XP'},
            {'code': 'comprehension_star', 'name': 'Comprehension Star', 'desc': 'Complete 5 comprehension exercises'},
            {'code': 'streak_keeper', 'name': 'Streak Keeper', 'desc': 'Maintain a 7-day streak'},
            {'code': 'unit_completer', 'name': 'Unit Completer', 'desc': 'Complete an entire unit'},
            {'code': 'skill_master', 'name': 'Skill Master', 'desc': 'Master one skill area'},
            {'code': 'memory_champion', 'name': 'Memory Champion', 'desc': 'Earn 200 XP'},
            {'code': 'brave_speaker', 'name': 'Brave Speaker', 'desc': 'Complete a speaking exercise'},
        ]
        
        for badge in badges_data:
            Badge.objects.get_or_create(
                code=badge['code'],
                defaults={
                    'name': badge['name'],
                    'description': badge['desc'],
                    'condition': {'type': 'xp_threshold', 'value': 0},
                }
            )
        
        # Create demo users
        self.stdout.write('Creating demo users...')
        
        # Admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eslapp.local',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        # Demo learner
        learner_user, created = User.objects.get_or_create(
            username='learner1',
            defaults={
                'email': 'learner@eslapp.local',
                'first_name': 'Ana',
                'last_name': 'Silva',
            }
        )
        if created:
            learner_user.set_password('learner123')
            learner_user.save()
            
            # Create profile for learner
            UserProfile.objects.get_or_create(
                user=learner_user,
                defaults={
                    'current_level': 'A1',
                    'current_unit': 1,
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
        self.stdout.write('\nDemocredentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Learner: learner1 / learner123')
