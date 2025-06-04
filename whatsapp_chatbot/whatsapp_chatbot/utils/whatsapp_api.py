import logging
from twilio.rest import Client
from django.conf import settings

logger = logging.getLogger(__name__)

class WhatsAppAPI:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_WHATSAPP_NUMBER

    def send_message(self, to, message):
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=f"whatsapp:{to}"
            )
            logger.info(f"Sent message SID: {msg.sid}")
            return {"status": "sent", "sid": msg.sid}
        except Exception as e:
            logger.error(f"Send message error: {str(e)}")
            raise  # Propagate error to webhook

    def process_incoming_message(self, payload):
        sender = payload.get('From', '').replace('whatsapp:', '')
        message_text = payload.get('Body', '')
        return sender, message_text