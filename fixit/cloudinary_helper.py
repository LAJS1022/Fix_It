import cloudinary
import cloudinary.uploader
from flask import current_app

def configure_cloudinary():
    cloudinary.config(
        cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=current_app.config['CLOUDINARY_API_KEY'],
        api_secret=current_app.config['CLOUDINARY_API_SECRET']
    )

def upload_image(file, folder='fixit'):
    configure_cloudinary()
    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        allowed_formats=['jpg', 'jpeg', 'png', 'webp'],
        transformation=[
            {'quality': 'auto'},
            {'fetch_format': 'auto'}
        ]
    )
    return result['secure_url']

def delete_image(public_id):
    configure_cloudinary()
    cloudinary.uploader.destroy(public_id)
    
