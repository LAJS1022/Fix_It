from flask import request
from flask_restx import Namespace, Resource
from fixit.providers.models import Provider
from fixit.services.models import Service
from fixit.categories.models import Category
from haversine import haversine, Unit

ns = Namespace('search', description='Search operations')

@ns.route('/')
class Search(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        city = request.args.get('city', '').lower()
        category_slug = request.args.get('category', '')
        min_rating = request.args.get('min_rating', 0, type=float)
        max_price = request.args.get('max_price', type=float)
        min_price = request.args.get('min_price', type=float)

        providers = Provider.query.all()
        results = []

        for provider in providers:
            if provider.user.is_banned:
                continue

            if city and provider.user.city and city not in provider.user.city.lower():
                continue

            if min_rating and provider.avg_rating < min_rating:
                continue

            if max_price and provider.price_max and provider.price_max > max_price:
                continue

            if min_price and provider.price_min and provider.price_min < min_price:
                continue

            if category_slug:
                category = Category.query.filter_by(slug=category_slug).first()
                if category:
                    has_category = Service.query.filter_by(
                        provider_id=provider.id,
                        category_id=category.id
                    ).first()
                    if not has_category:
                        continue

            if query:
                name = provider.user.first_name.lower() + ' ' + provider.user.last_name.lower()
                bio = (provider.bio or '').lower()
                zone = (provider.service_zone or '').lower()
                if query not in name and query not in bio and query not in zone:
                    continue

            results.append(provider.to_dict())

        return results, 200

@ns.route('/nearby')
class Nearby(Resource):
    def get(self):
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', 10, type=float)
        category_slug = request.args.get('category', '')

        if not lat or not lng:
            return {'error': 'lat and lng are required'}, 400

        providers = Provider.query.filter(
            Provider.latitude.isnot(None),
            Provider.longitude.isnot(None)
        ).all()

        results = []

        for provider in providers:
            if provider.user.is_banned:
                continue

            distance = haversine(
                (lat, lng),
                (provider.latitude, provider.longitude),
                unit=Unit.KILOMETERS
            )

            if distance > radius:
                continue

            if category_slug:
                category = Category.query.filter_by(slug=category_slug).first()
                if category:
                    has_category = Service.query.filter_by(
                        provider_id=provider.id,
                        category_id=category.id
                    ).first()
                    if not has_category:
                        continue

            provider_dict = provider.to_dict()
            provider_dict['distance_km'] = round(distance, 2)
            results.append(provider_dict)

        results.sort(key=lambda x: x['distance_km'])

        return results, 200
    
