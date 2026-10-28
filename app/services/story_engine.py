import json
import os
from flask import current_app

class StoryEngine:
    _story_data = None

    @classmethod
    def load_data(cls):
        if cls._story_data is None:
            data_path = os.path.join(current_app.root_path, '..', 'data', 'story_chapters.json')
            if not os.path.exists(data_path):
                data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'story_chapters.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                cls._story_data = json.load(f)
        return cls._story_data

    @classmethod
    def get_chapter_story(cls, chapter_id: int):
        data = cls.load_data()
        for ch in data:
            if ch.get('chapter') == chapter_id:
                return ch
        return None
