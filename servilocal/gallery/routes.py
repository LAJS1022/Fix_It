from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from servilocal.gallery.models import Gallery
from servilocal.providers.models import Provider

ns = Namespace('gallery', description='Gallery operations')

gallery_model = ns.model('Gallery', {
    'image_url': fields.String(required=True),
    'service_id': fields.String(required=False),
    'caption': fields.String(required=False)
})

@ns.route('/')
class GalleryList(Resource):
    @jwt_required()
    @ns.expect(gallery_model)
    def post(self):
        current_user_id = get_jwt_identity()

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        if not provider:
            return {'error': 'You must have a provider profile to upload photos'}, 403

        data = request.json
        try:
            item = Gallery(
                provider_id=provider.id,
                image_url=data['image_url'],
                service_id=data.get('service_id'),
                caption=data.get('caption')
            )
            item.save()
            return item.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:gallery_id>')
class GalleryResource(Resource):
    def get(self, gallery_id):
        item = Gallery.query.get(gallery_id)
        if not item:
            return {'error': 'Gallery item not found'}, 404
        return item.to_dict(), 200

    @jwt_required()
    def delete(self, gallery_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        item = Gallery.query.get(gallery_id)
        if not item:
            return {'error': 'Gallery item not found'}, 404

        provider = Provider.query.filter_by(user_id=current_user_id).first()
        if not provider or item.provider_id != provider.id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        item.delete()
        return {'message': 'Gallery item deleted successfully'}, 200
