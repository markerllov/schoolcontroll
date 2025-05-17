import json
import random
from pathlib import Path


class QuestionManager:
    def __init__(self):
        self.questions = self._load_questions()
        self.current_questions = []
        self.user_answers = []

    def _load_questions(self):
        """Загружает вопросы из JSON-файла"""
        try:
            config_path = Path(__file__).parent.parent / 'config' / 'questions.json'
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def generate_questions(self, count=2):
        """Генерирует новые вопросы"""
        if len(self.questions) < count:
            count = len(self.questions)

        self.current_questions = random.sample(self.questions, count)
        self.user_answers = [""] * count
        return self.current_questions

    def update_answer(self, index, answer):
        """Обновляет ответ пользователя"""
        if 0 <= index < len(self.user_answers):
            self.user_answers[index] = answer

    def check_answers(self):
        """Проверяет правильность ответов"""
        return all(
            user_answer.strip().lower() == q["answer"].lower()
            for q, user_answer in zip(self.current_questions, self.user_answers)
        )