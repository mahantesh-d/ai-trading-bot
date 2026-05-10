from twilio.rest import Client
from .logging_setup import logger
from . import config

class WhatsAppNotifier:
    def __init__(self):
        try:
            self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            self.from_whatsapp_number = config.TWILIO_WHATSAPP_FROM
            self.to_whatsapp_number = config.TWILIO_WHATSAPP_TO
            logger.info("Twilio client initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Twilio client: {e}")
            self.client = None

    def send_message(self, message):
        """Sends a message to the configured WhatsApp number."""
        if not self.client:
            logger.error("Twilio client not initialized. Cannot send message.")
            return

        try:
            self.client.messages.create(
                body=message,
                from_=self.from_whatsapp_number,
                to=self.to_whatsapp_number,
            )
            logger.info(f"WhatsApp message sent: {message}")
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
