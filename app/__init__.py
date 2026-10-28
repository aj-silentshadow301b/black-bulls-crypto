import json
import os
from flask import Flask
from config import Config
from app.database import db, init_db
from app.models import Chapter, Challenge

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    # Initialize Database
    init_db(app)

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # Seed Database on initialization
    with app.app_context():
        seed_database(app)

    return app

def seed_database(app):
    """Seed initial chapters and challenges from JSON data if DB is empty."""
    try:
        if Chapter.query.count() == 0:
            challenges_file = os.path.join(app.root_path, '..', 'data', 'challenges.json')
            if not os.path.exists(challenges_file):
                challenges_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'challenges.json')
                
            with open(challenges_file, 'r', encoding='utf-8') as f:
                c_data = json.load(f)

            for item in c_data:
                cid = item['chapter_id']
                # Create chapter if missing
                ch = Chapter.query.get(cid)
                if not ch:
                    ch = Chapter(
                        id=cid,
                        title=item['title'],
                        character=item['character'],
                        crypto_type=item['crypto_type'],
                        difficulty=item['difficulty'],
                        summary=item['prompt']
                    )
                    db.session.add(ch)

                # Create challenge
                chal = Challenge.query.get(item['id'])
                if not chal:
                    chal = Challenge(
                        id=item['id'],
                        chapter_id=cid,
                        title=item['title'],
                        crypto_type=item['crypto_type'],
                        difficulty=item['difficulty'],
                        prompt=item['prompt'],
                        ciphertext=item['ciphertext'],
                        public_data_json=json.dumps(item.get('public_data', {})),
                        hints_json=json.dumps(item.get('hints', [])),
                        flag_hash=item['flag_hash'],
                        spell_name=item['spell_name'],
                        spell_desc=item['spell_desc']
                    )
                    db.session.add(chal)
            db.session.commit()
            print("Database seeded with 12 chapters and challenges successfully.")
    except Exception as e:
        print(f"Error seeding database: {e}")
