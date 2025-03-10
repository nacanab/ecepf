import firebase_admin
from firebase_admin import credentials, messaging

# Charger la clé de service
cred = credentials.Certificate("static/js/ecep-f1dc4-firebase-adminsdk-fbsvc-a01da75ada.json")
firebase_admin.initialize_app(cred)

def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    return response