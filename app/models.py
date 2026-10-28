from datetime import datetime
import json
from app.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, default='BlackBullMember')
    session_id = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_chapter = db.Column(db.Integer, default=1)
    
    progress = db.relationship('PlayerProgress', backref='user', lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship('ChallengeAttempt', backref='user', lazy=True, cascade="all, delete-orphan")
    hints_used = db.relationship('HintUsage', backref='user', lazy=True, cascade="all, delete-orphan")
    spells = db.relationship('UnlockedSpell', backref='user', lazy=True, cascade="all, delete-orphan")
    achievements = db.relationship('Achievement', backref='user', lazy=True, cascade="all, delete-orphan")

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True) # 1 to 12
    title = db.Column(db.String(128), nullable=False)
    character = db.Column(db.String(64), nullable=False)
    crypto_type = db.Column(db.String(64), nullable=False)
    difficulty = db.Column(db.String(32), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    
    challenges = db.relationship('Challenge', backref='chapter', lazy=True)

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.String(64), primary_key=True) # e.g. "chapter-01"
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    crypto_type = db.Column(db.String(64), nullable=False)
    difficulty = db.Column(db.String(32), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    ciphertext = db.Column(db.Text, nullable=False)
    public_data_json = db.Column(db.Text, default='{}')
    hints_json = db.Column(db.Text, default='[]')
    flag_hash = db.Column(db.String(128), nullable=False) # SHA256 of flag
    spell_name = db.Column(db.String(128), nullable=False)
    spell_desc = db.Column(db.Text, nullable=False)

    def get_public_data(self):
        try:
            return json.loads(self.public_data_json or '{}')
        except Exception:
            return {}

    def get_hints(self):
        try:
            return json.loads(self.hints_json or '[]')
        except Exception:
            return []

class ChallengeAttempt(db.Model):
    __tablename__ = 'challenge_attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.String(64), db.ForeignKey('challenges.id'), nullable=False)
    submitted_flag = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class HintUsage(db.Model):
    __tablename__ = 'hint_usages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.String(64), db.ForeignKey('challenges.id'), nullable=False)
    hint_index = db.Column(db.Integer, nullable=False) # 1, 2, or 3
    used_at = db.Column(db.DateTime, default=datetime.utcnow)

class PlayerProgress(db.Model):
    __tablename__ = 'player_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(32), default='sealed') # sealed, discovered, unlocked, solved, mastered
    score = db.Column(db.Integer, default=0)
    solved_at = db.Column(db.DateTime, nullable=True)

class UnlockedSpell(db.Model):
    __tablename__ = 'unlocked_spells'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)
    spell_name = db.Column(db.String(128), nullable=False)
    spell_desc = db.Column(db.Text, nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_key = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
