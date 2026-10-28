import hmac

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from app.services.progress_service import ProgressService
from app.services.story_engine import StoryEngine
from app.models import Challenge, PlayerProgress, User, ChallengeAttempt

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    user = ProgressService.get_or_create_user()
    return render_template("index.html", user=user, stats=ProgressService.get_user_stats(user.id))

@main_bp.route("/intro")
def intro():
    return render_template("intro.html", user=ProgressService.get_or_create_user())

@main_bp.route("/grimoire")
def grimoire():
    user = ProgressService.get_or_create_user()
    return render_template("grimoire.html", user=user, progress=ProgressService.get_all_progress(user.id), stats=ProgressService.get_user_stats(user.id))

@main_bp.route("/chapter/<int:chapter_id>")
def chapter_story(chapter_id):
    user = ProgressService.get_or_create_user()
    if chapter_id < 1 or chapter_id > 12:
        return redirect(url_for("main.grimoire"))
    prog = PlayerProgress.query.filter_by(user_id=user.id, chapter_id=chapter_id).first()
    if not prog or prog.status == "sealed":
        flash("This chapter is sealed. Complete preceding chapters first.", "warning")
        return redirect(url_for("main.grimoire"))
    story = StoryEngine.get_chapter_story(chapter_id)
    return render_template("chapter.html", user=user, chapter_id=chapter_id, story=story, prog=prog)

@main_bp.route("/challenge/<int:chapter_id>")
def challenge_page(chapter_id):
    user = ProgressService.get_or_create_user()
    if chapter_id < 1 or chapter_id > 12:
        return redirect(url_for("main.grimoire"))
    prog = PlayerProgress.query.filter_by(user_id=user.id, chapter_id=chapter_id).first()
    if not prog or prog.status == "sealed":
        flash("Forbidden access. Seal is still intact.", "warning")
        return redirect(url_for("main.grimoire"))
    chal = Challenge.query.filter_by(chapter_id=chapter_id).first()
    story = StoryEngine.get_chapter_story(chapter_id)
    hints_used = ProgressService.get_hints_used(user.id, chal.id) if chal else []
    return render_template("challenge.html", user=user, chapter_id=chapter_id, challenge=chal, story=story, prog=prog, hints_used=hints_used)

@main_bp.route("/archive")
def archive():
    user = ProgressService.get_or_create_user()
    return render_template("archive.html", user=user, stats=ProgressService.get_user_stats(user.id), stories=StoryEngine.load_data())

@main_bp.route("/admin", methods=["GET", "POST"])
def admin():
    configured_pass = current_app.config.get("ADMIN_PASSCODE", "")
    supplied = request.args.get("passcode") or request.form.get("passcode")
    if not configured_pass or not supplied or not hmac.compare_digest(supplied, configured_pass):
        return render_template("admin_login.html")
    users = User.query.all()
    attempts = ChallengeAttempt.query.order_by(ChallengeAttempt.timestamp.desc()).limit(50).all()
    return render_template("admin.html", users=users, attempts=attempts)
