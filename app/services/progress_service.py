from datetime import datetime
import json
import uuid
from flask import session
from app.database import db
from app.models import User, PlayerProgress, ChallengeAttempt, HintUsage, UnlockedSpell, Achievement, Challenge

class ProgressService:
    @staticmethod
    def get_or_create_user(session_id=None):
        if not session_id:
            if 'user_session_id' not in session:
                session['user_session_id'] = str(uuid.uuid4())
            session_id = session['user_session_id']
        
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            user = User(
                username=f"MagicKnight_{session_id[:6]}",
                session_id=session_id,
                current_chapter=1
            )
            db.session.add(user)
            db.session.commit()
            
            # Initialize 12 chapters progress
            for ch in range(1, 13):
                status = 'unlocked' if ch == 1 else 'sealed'
                prog = PlayerProgress(
                    user_id=user.id,
                    chapter_id=ch,
                    status=status,
                    score=0
                )
                db.session.add(prog)
            db.session.commit()
            
            # Grant first achievement
            ProgressService.grant_achievement(user.id, 'JOURNEY_BEGINS', 'Black Bulls Recruit', 'Entered the Black Bulls Hideout and opened the Grimoire.')
            
        return user

    @staticmethod
    def get_all_progress(user_id):
        progs = PlayerProgress.query.filter_by(user_id=user_id).order_by(PlayerProgress.chapter_id).all()
        result = []
        for p in progs:
            result.append({
                'chapter_id': p.chapter_id,
                'status': p.status,
                'score': p.score,
                'solved_at': p.solved_at.isoformat() if p.solved_at else None
            })
        return result

    @staticmethod
    def get_hints_used(user_id, challenge_id):
        usages = HintUsage.query.filter_by(user_id=user_id, challenge_id=challenge_id).all()
        return [u.hint_index for u in usages]

    @staticmethod
    def unlock_hint(user_id, challenge_id, hint_index):
        existing = HintUsage.query.filter_by(user_id=user_id, challenge_id=challenge_id, hint_index=hint_index).first()
        if not existing:
            usage = HintUsage(user_id=user_id, challenge_id=challenge_id, hint_index=hint_index)
            db.session.add(usage)
            db.session.commit()
            
            # Achievement check: Curious Magic Knight
            total_hints = HintUsage.query.filter_by(user_id=user_id).count()
            if total_hints >= 3:
                ProgressService.grant_achievement(user_id, 'MAGIC_ANALYST', 'Magic Analyst', 'Used 3 investigation hints to decipher ancient runes.')
        return True

    @staticmethod
    def record_attempt(user_id, challenge_id, submitted_flag, is_correct):
        attempt = ChallengeAttempt(
            user_id=user_id,
            challenge_id=challenge_id,
            submitted_flag=submitted_flag,
            is_correct=is_correct
        )
        db.session.add(attempt)
        db.session.commit()

        if is_correct:
            # Find challenge to get chapter_id and spell info
            chal = Challenge.query.get(challenge_id)
            if chal:
                ch_id = chal.chapter_id
                prog = PlayerProgress.query.filter_by(user_id=user_id, chapter_id=ch_id).first()
                if prog and prog.status != 'solved':
                    prog.status = 'solved'
                    prog.solved_at = datetime.utcnow()
                    
                    # Compute score based on difficulty and hints used
                    base_points = 100 * ch_id
                    hints_used_count = HintUsage.query.filter_by(user_id=user_id, challenge_id=challenge_id).count()
                    penalty = hints_used_count * 15
                    prog.score = max(20, base_points - penalty)
                    
                    # Unlock next chapter if not at end
                    if ch_id < 12:
                        next_prog = PlayerProgress.query.filter_by(user_id=user_id, chapter_id=ch_id + 1).first()
                        if next_prog and next_prog.status == 'sealed':
                            next_prog.status = 'unlocked'
                        
                        user = User.query.get(user_id)
                        if user and user.current_chapter <= ch_id:
                            user.current_chapter = ch_id + 1
                            
                    # Unlock Spell
                    unlocked_sp = UnlockedSpell.query.filter_by(user_id=user_id, chapter_id=ch_id).first()
                    if not unlocked_sp:
                        unlocked_sp = UnlockedSpell(
                            user_id=user_id,
                            chapter_id=ch_id,
                            spell_name=chal.spell_name,
                            spell_desc=chal.spell_desc
                        )
                        db.session.add(unlocked_sp)
                        
                    db.session.commit()
                    
                    # Grant Achievements
                    if ch_id == 1:
                        ProgressService.grant_achievement(user_id, 'FIRST_SPELL', 'First Spell Awakened', 'Awakened Anti-Magic Slash from Asta\'s Grimoire.')
                    elif ch_id == 5:
                        ProgressService.grant_achievement(user_id, 'BLACK_BULL_MEMBER', 'Black Bull Squad Honor', 'Assembled all squad fragments in Chapter 5.')
                    elif ch_id == 12:
                        ProgressService.grant_achievement(user_id, 'GRIMOIRE_MASTER', 'Grimoire Master', 'Conquered the Final Grimoire and nullified the ultimate devil seal!')

    @staticmethod
    def grant_achievement(user_id, badge_key, title, description):
        existing = Achievement.query.filter_by(user_id=user_id, badge_key=badge_key).first()
        if not existing:
            ach = Achievement(
                user_id=user_id,
                badge_key=badge_key,
                title=title,
                description=description
            )
            db.session.add(ach)
            db.session.commit()

    @staticmethod
    def get_user_stats(user_id):
        user = User.query.get(user_id)
        progs = PlayerProgress.query.filter_by(user_id=user_id).all()
        solved_count = sum(1 for p in progs if p.status == 'solved')
        total_score = sum(p.score for p in progs if p.status == 'solved')
        spells = UnlockedSpell.query.filter_by(user_id=user_id).all()
        achievements = Achievement.query.filter_by(user_id=user_id).all()
        
        return {
            'username': user.username if user else 'BlackBullMember',
            'current_chapter': user.current_chapter if user else 1,
            'solved_count': solved_count,
            'total_score': total_score,
            'spells_count': len(spells),
            'achievements_count': len(achievements),
            'spells': [{'chapter': s.chapter_id, 'name': s.spell_name, 'desc': s.spell_desc} for s in spells],
            'achievements': [{'key': a.badge_key, 'title': a.title, 'desc': a.description} for a in achievements]
        }
