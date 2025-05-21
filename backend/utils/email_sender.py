from email.message import EmailMessage
import smtplib
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_alarm_email(table_name, alarms):
    msg = EmailMessage()
    msg['Subject'] = f"Alarmas activadas en la tabla '{table_name}'"
    msg['From'] = 'saramanrique2016@gmail.com'
    msg['To'] = 'saramanrique2016@gmail.com'

    cuerpo = f"Se activaron las siguientes alarmas en la tabla '{table_name}':\n\n"
    for alarm in alarms:
        cuerpo += f"- {alarm['description']} (condición: {alarm.get('condition', 'No definida')})\n"  # Cambio aquí

    msg.set_content(cuerpo)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('saramanrique2016@gmail.com', 'rtcc ybig ztty gavc')
        smtp.send_message(msg)
