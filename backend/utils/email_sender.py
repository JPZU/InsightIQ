import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Any

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_alarm_email(table_name: str, alarms: List[Dict[str, Any]], triggered_data: Dict[str, Any] = None):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚨 ALARM TRIGGERED - Table '{table_name}'"
        msg['From'] = 'ruizsantiago836@gmail.com'
        msg['To'] = 'ruizsantiago836@gmail.com'

        # HTML template for the email
        html_template = """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #202124;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .alarm-container {
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 20px;
                    border: 1px solid #dadce0;
                }
                .alarm-header {
                    color: #d93025;
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #dadce0;
                }
                .alarm-description {
                    font-size: 16px;
                    color: #202124;
                    margin-bottom: 15px;
                }
                .alarm-details {
                    background-color: white;
                    border-radius: 4px;
                    padding: 15px;
                    margin-bottom: 15px;
                }
                .detail-row {
                    display: flex;
                    margin-bottom: 8px;
                    padding: 4px 0;
                }
                .detail-label {
                    font-weight: bold;
                    width: 150px;
                    color: #5f6368;
                }
                .detail-value {
                    flex: 1;
                    color: #202124;
                }
                .severity-high {
                    color: #d93025;
                }
                .severity-medium {
                    color: #f29900;
                }
                .severity-low {
                    color: #188038;
                }
            </style>
        </head>
        <body>
            <div class="alarm-container">
                <div class="alarm-header">
                    🚨 Alarm Triggered in {table_name}
                </div>
        """

        for alarm in alarms:
            severity_class = f"severity-{alarm.get('severity', 'medium').lower()}"
            
            html_template += f"""
                <div class="alarm-description">
                    {alarm['description']}
                </div>
                <div class="alarm-details">
                    <div class="detail-row">
                        <span class="detail-label">Alarm ID:</span>
                        <span class="detail-value">{alarm.get('alarm_id', 'N/A')}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Condition:</span>
                        <span class="detail-value">{alarm.get('condition', 'Not defined')}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Severity:</span>
                        <span class="detail-value {severity_class}">{alarm.get('severity', 'Medium')}</span>
                    </div>
            """

            if alarm.get('triggered_data'):
                data = alarm['triggered_data']
                html_template += """
                    <div style="margin-top: 15px; border-top: 1px solid #dadce0; padding-top: 15px;">
                        <div style="font-weight: bold; margin-bottom: 10px; color: #5f6368;">Triggered Data:</div>
                """
                
                for key, value in data.items():
                    formatted_key = key.replace('_', ' ').title()
                    html_template += f"""
                        <div class="detail-row">
                            <span class="detail-label">{formatted_key}:</span>
                            <span class="detail-value">{value}</span>
                        </div>
                    """
                
                html_template += "</div>"

            html_template += """
                </div>
            """

        html_template += """
            </div>
        </body>
        </html>
        """

        # Attach both plain text and HTML versions
        msg.attach(MIMEText(html_template.format(table_name=table_name), 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('ruizsantiago836@gmail.com', 'rczi zbyx yyxy tbkh')
            smtp.send_message(msg)
            
        logger.info(f"Alarm email sent successfully for table {table_name}")
        return True
    except Exception as e:
        logger.error(f"Error sending alarm email: {str(e)}")
        return False
