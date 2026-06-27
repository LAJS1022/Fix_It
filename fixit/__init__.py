from flask import Flask
from flask_restx import Api
from config import config
from database import db, bcrypt, jwt, cors

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter: Bearer <your_token>'
    }
}

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='Fix It API',
        description='Fix It REST API',
        authorizations=authorizations,
        security='Bearer',
        doc='/docs'
    )

    from fixit.auth.routes import ns as auth_ns
    from fixit.users.routes import ns as users_ns
    from fixit.providers.routes import ns as providers_ns
    from fixit.services.routes import ns as services_ns
    from fixit.categories.routes import ns as categories_ns
    from fixit.bookings.routes import ns as bookings_ns
    from fixit.reviews.routes import ns as reviews_ns
    from fixit.gallery.routes import ns as gallery_ns
    from fixit.search.routes import ns as search_ns
    from fixit.favorites.routes import ns as favorites_ns
    from fixit.notifications.routes import ns as notifications_ns
    from fixit.reports.routes import ns as reports_ns
    
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(providers_ns, path='/api/v1/providers')
    api.add_namespace(services_ns, path='/api/v1/services')
    api.add_namespace(categories_ns, path='/api/v1/categories')
    api.add_namespace(bookings_ns, path='/api/v1/bookings')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(gallery_ns, path='/api/v1/gallery')
    api.add_namespace(search_ns, path='/api/v1/search')
    api.add_namespace(favorites_ns, path='/api/v1/favorites')
    api.add_namespace(notifications_ns, path='/api/v1/notifications')
    api.add_namespace(reports_ns, path='/api/v1/reports')
    
    return app
