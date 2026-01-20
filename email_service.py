import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

def send_email_with_attachment(recipient_email, df, weights, impacts):
    """
    Send TOPSIS results to the user via email
    
    Args:
        recipient_email (str): Email address to send results to
        df (pd.DataFrame): DataFrame containing TOPSIS results
        weights (str): Weights used in the calculation
        impacts (str): Impacts used in the calculation
    """
    
    # Get email configuration from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    
    if not sender_email or not sender_password:
        raise ValueError("SENDER_EMAIL or SENDER_PASSWORD not configured in .env file")
    
    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Your TOPSIS Analysis Results"
    
    # Email body
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; border-radius: 5px; }}
            .content {{ padding: 20px; }}
            .info {{ background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }}
            .footer {{ text-align: center; color: #888; margin-top: 20px; font-size: 12px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 TOPSIS Analysis Results</h1>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>Your TOPSIS analysis has been completed successfully. Please find the detailed results below:</p>
                
                <div class="info">
                    <strong>Analysis Configuration:</strong><br>
                    Weights: {weights}<br>
                    Impacts: {impacts}
                </div>
                
                <h3>Summary Statistics:</h3>
                <ul>
                    <li><strong>Best Score:</strong> {df['Topsis Score'].max():.4f}</li>
                    <li><strong>Worst Score:</strong> {df['Topsis Score'].min():.4f}</li>
                    <li><strong>Average Score:</strong> {df['Topsis Score'].mean():.4f}</li>
                    <li><strong>Total Alternatives:</strong> {len(df)}</li>
                </ul>
                
                <h3>Top 3 Alternatives:</h3>
                <table>
                    <tr>
                        <th>Rank</th>
                        <th>Alternative</th>
                        <th>Score</th>
                    </tr>
    """
    
    # Add top 3 alternatives to email
    top_3 = df.nsmallest(3, 'Rank')[['Alternative', 'Topsis Score', 'Rank']].sort_values('Rank')
    for idx, row in top_3.iterrows():
        body += f"""
                    <tr>
                        <td>#{int(row['Rank'])}</td>
                        <td>{row['Alternative']}</td>
                        <td>{row['Topsis Score']:.4f}</td>
                    </tr>
        """
    
    body += """
                </table>
                
                <p>The complete results are attached to this email as a CSV file.</p>
                
                <div class="info">
                    <strong>Next Steps:</strong><br>
                    - Download the attached CSV file for detailed results<br>
                    - Import the data into your preferred analysis tool<br>
                    - Use the rankings to support your decision-making process
                </div>
                
                <p>Thank you for using TOPSIS Decision Support Tool!</p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply directly to this message.</p>
                <p>For support, contact: aryan10767@gmail.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Attach the HTML body
    message.attach(MIMEText(body, "html"))
    
    # Create CSV attachment
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Attach CSV file
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(csv_buffer.getvalue().encode())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename="topsis_results.csv")
    message.attach(attachment)
    
    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  # Initial handshake
        server.starttls()  # Upgrade to TLS (REQUIRED for Gmail)
        server.ehlo()  # Handshake after TLS
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except smtplib.SMTPException as e:
        raise Exception(f"Failed to send email via SMTP: {str(e)}")
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")
