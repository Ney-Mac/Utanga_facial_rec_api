from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID") # id da conta twilio 
auth_token = os.getenv("TWILIO_AUTH_TOKEN") # token de verificaco de identidade 
twilio_number = os.getenv("TWILIO_NUMBER") # numero que envia a mensagem
number_to_send = os.getenv("NUMBER_TO_SEND") # numero que recebe

client = Client(account_sid, auth_token)

def enviar_mensagem(text):
    message = client.messages.create(
        body=text,
        from_=twilio_number,
        to=number_to_send
    )
    
    print(f"Mensagem enviada com SID: {message.sid}")
    
