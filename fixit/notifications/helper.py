from fixit.notifications.models import Notification
from database import db

def send_notification(user_id, type, message):
    notification = Notification(
        user_id=user_id,
        type=type,
        message=message
    )
    db.session.add(notification)
    db.session.commit()
