import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fixit import create_app
from database import db
from fixit.users.models import User
from fixit.categories.models import Category

app = create_app('development')

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email='admin@fixit.com').first():
        admin = User(
            first_name='Admin',
            last_name='ServiLocal',
            email='admin@fixit.com',
            password='admin1234',
            role='client',
            is_admin=True
        )
        admin.save()
        print('Admin created: admin@fixit.com / admin1234')
    else:
        print('Admin already exists')

    categories = [
        {'name': 'Plomeria', 'slug': 'plomeria', 'icon': 'wrench', 'description': 'Servicios de plomeria y fontaneria'},
        {'name': 'Electricidad', 'slug': 'electricidad', 'icon': 'zap', 'description': 'Servicios electricos'},
        {'name': 'Jardineria', 'slug': 'jardineria', 'icon': 'leaf', 'description': 'Servicios de jardineria y paisajismo'},
        {'name': 'Limpieza', 'slug': 'limpieza', 'icon': 'sparkles', 'description': 'Servicios de limpieza del hogar'},
        {'name': 'Pintura', 'slug': 'pintura', 'icon': 'paintbrush', 'description': 'Servicios de pintura interior y exterior'},
        {'name': 'Mudanzas', 'slug': 'mudanzas', 'icon': 'truck', 'description': 'Servicios de mudanza y carga'},
        {'name': 'Cuidado de mascotas', 'slug': 'mascotas', 'icon': 'paw', 'description': 'Servicios de cuidado y paseo de mascotas'},
        {'name': 'Reparaciones', 'slug': 'reparaciones', 'icon': 'hammer', 'description': 'Reparaciones generales del hogar'},
        {'name': 'Carpinteria', 'slug': 'carpinteria', 'icon': 'ruler', 'description': 'Servicios de carpinteria y ebanisteria'},
        {'name': 'Cerrajeria', 'slug': 'cerrajeria', 'icon': 'key', 'description': 'Servicios de cerrajeria'},
    ]

    for cat in categories:
        if not Category.query.filter_by(slug=cat['slug']).first():
            category = Category(
                name=cat['name'],
                slug=cat['slug'],
                icon=cat['icon'],
                description=cat['description']
            )
            category.save()
            print('Category created: ' + cat['name'])
        else:
            print('Category already exists: ' + cat['name'])

    print('Done!')
