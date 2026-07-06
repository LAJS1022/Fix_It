"""
Run this once from your repo root to create/promote an admin user:
    python scripts/make_admin.py
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fixit import create_app
from database import db
from fixit.users.models import User

app = create_app('development')

EMAIL = 'luisssajs@gmail.com'
PASSWORD = 'ThisIsHereJustForAMoment'  

with app.app_context():
    user = User.query.filter_by(email=EMAIL).first()

    if user:
        user.is_admin = True
        db.session.commit()
        print(f'Existing user {EMAIL} promoted to admin.')
    else:
        user = User(
            first_name='Luis',
            last_name='Jimenez',
            email=EMAIL,
            password=PASSWORD,
            role='client',
            is_admin=True
        )
        user.save()
        print(f'Admin created: {EMAIL} / {PASSWORD}')
