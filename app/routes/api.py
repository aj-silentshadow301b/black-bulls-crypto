from flask import Blueprint, jsonify, request
from app.database import db
from app.services.progress_service import ProgressService
from app.services.crypto_engine import CryptoEngine
from app.models import Challenge, PlayerProgress

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/progress", methods=["GET"])
def get_progress():
    user = ProgressService.get_or_create_user()
    return jsonify({
        "status": "success",
        "user": {"username": user.username, "current_chapter": user.current_chapter},
        "progress": ProgressService.get_all_progress(user.id),
        "stats": ProgressService.get_user_stats(user.id),
    })

@api_bp.route("/challenge/<int:chapter_id>", methods=["GET"])
def get_challenge_data(chapter_id):
    user = ProgressService.get_or_create_user()
    prog = PlayerProgress.query.filter_by(user_id=user.id, chapter_id=chapter_id).first()
    if not prog or prog.status == "sealed":
        return jsonify({"status": "error", "message": "This Grimoire page is sealed. Complete preceding chapters first."}), 403
    chal = Challenge.query.filter_by(chapter_id=chapter_id).first()
    if not chal:
        return jsonify({"status": "error", "message": "Challenge not found."}), 404
    used = ProgressService.get_hints_used(user.id, chal.id)
    hints = chal.get_hints()
    unlocked = [{"index": i, "text": hints[i - 1] if i <= len(hints) else "No further hint available."} for i in range(1, 4) if i in used]
    return jsonify({"status": "success", "challenge": {
        "id": chal.id, "chapter_id": chal.chapter_id, "title": chal.title,
        "crypto_type": chal.crypto_type, "difficulty": chal.difficulty,
        "prompt": chal.prompt, "ciphertext": chal.ciphertext,
        "public_data": chal.get_public_data(), "spell_name": chal.spell_name,
        "spell_desc": chal.spell_desc, "is_solved": prog.status == "solved",
        "unlocked_hints": unlocked, "total_hints_count": len(hints),
    }})

@api_bp.route("/submit", methods=["POST"])
def submit_flag():
    user = ProgressService.get_or_create_user()
    data = request.get_json() or {}
    chapter_id = data.get("chapter_id")
    submitted = data.get("flag", "").strip()
    if not chapter_id or not submitted:
        return jsonify({"status": "error", "message": "Missing chapter_id or flag submission."}), 400
    chal = Challenge.query.filter_by(chapter_id=int(chapter_id)).first()
    if not chal:
        return jsonify({"status": "error", "message": "Challenge not found."}), 404

    # The repository stores challenge digests, never the plaintext answer list.
    correct = CryptoEngine.verify_flag(submitted, chal.flag_hash)
    ProgressService.record_attempt(user.id, chal.id, submitted, correct)
    if correct:
        next_chapter = int(chapter_id) + 1 if int(chapter_id) < 12 else 12
        return jsonify({
            "status": "success", "is_correct": True,
            "message": f"SPELL ACTIVATED! You have broken the seal on Chapter {chapter_id}!",
            "spell_unlocked": {"name": chal.spell_name, "description": chal.spell_desc},
            "next_chapter": next_chapter, "is_final_victory": int(chapter_id) == 12,
        })
    return jsonify({"status": "error", "is_correct": False, "message": "THE SPELL REJECTS YOU. Verify your decryption and try again!"})

@api_bp.route("/hint", methods=["POST"])
def get_hint():
    user = ProgressService.get_or_create_user()
    data = request.get_json() or {}
    chapter_id, hint_index = data.get("chapter_id"), data.get("hint_index")
    if not chapter_id or not hint_index:
        return jsonify({"status": "error", "message": "Missing parameters."}), 400
    chal = Challenge.query.filter_by(chapter_id=int(chapter_id)).first()
    if not chal:
        return jsonify({"status": "error", "message": "Challenge not found."}), 404
    hints = chal.get_hints()
    index = int(hint_index)
    if index < 1 or index > len(hints):
        return jsonify({"status": "error", "message": "Invalid hint index."}), 400
    ProgressService.unlock_hint(user.id, chal.id, index)
    return jsonify({"status": "success", "hint": {"index": index, "text": hints[index - 1]}})

@api_bp.route("/reset", methods=["POST"])
def reset_progress():
    user = ProgressService.get_or_create_user()
    for prog in PlayerProgress.query.filter_by(user_id=user.id).all():
        prog.status = "unlocked" if prog.chapter_id == 1 else "sealed"
        prog.score = 0
        prog.solved_at = None
    user.current_chapter = 1
    db.session.commit()
    return jsonify({"status": "success", "message": "Progress has been reset."})
